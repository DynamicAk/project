from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from authlib.integrations.flask_client import OAuth
from datetime import datetime, timedelta
import os
from functools import wraps
import secrets

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///yoga_club.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Google OAuth Configuration
app.config['GOOGLE_CLIENT_ID'] = os.environ.get('GOOGLE_CLIENT_ID')
app.config['GOOGLE_CLIENT_SECRET'] = os.environ.get('GOOGLE_CLIENT_SECRET')

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'
oauth = OAuth(app)

# Configure Google OAuth
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

# Models need to be defined here since we're using db from this file
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    profile_picture = db.Column(db.String(200))
    role = db.Column(db.String(20), default='student')  # student, professor, admin
    notifications_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    registrations = db.relationship('Registration', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.email}>'
    
    def is_admin(self):
        return self.role == 'admin'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, default=30)
    category = db.Column(db.String(50), default='class')  # class, workshop, retreat
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'
    
    def is_full(self):
        return len(self.registrations) >= self.max_participants
    
    def available_spots(self):
        return self.max_participants - len(self.registrations)

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate registrations
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='unique_user_event'),)

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='general')  # workshops, retreats, daily_practice, general
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create tables
with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TEMPORARY BYPASS FOR TESTING - REMOVE IN PRODUCTION
        bypass_param = request.args.get('bypass')
        if bypass_param == 'admin123':
            # Create a temporary admin user session for testing
            admin_user = User.query.filter_by(role='admin').first()
            if admin_user:
                login_user(admin_user)
                return f(*args, **kwargs)
        
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def nit_email_required(email):
    """Check if email belongs to NIT Delhi domain"""
    return email.endswith('@nitdelhi.ac.in')

# Routes
@app.route('/')
def index():
    # Get recent events
    upcoming_events = Event.query.filter(Event.date >= datetime.now()).order_by(Event.date).limit(3).all()
    return render_template('index.html', upcoming_events=upcoming_events)

# TEMPORARY TESTING ROUTE - REMOVE IN PRODUCTION
@app.route('/test-admin')
def test_admin():
    """Bypass route for testing admin panel"""
    admin_user = User.query.filter_by(role='admin').first()
    if admin_user:
        login_user(admin_user)
        flash('Logged in as admin for testing!', 'success')
        return redirect(url_for('admin_dashboard'))
    else:
        flash('No admin user found in database.', 'error')
        return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/auth/google')
def google_auth():
    redirect_uri = url_for('google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def google_callback():
    try:
        token = google.authorize_access_token()
        user_info = token.get('userinfo')
        
        if not user_info:
            flash('Failed to get user information from Google.', 'error')
            return redirect(url_for('login'))
        
        email = user_info.get('email')
        
        # Check if email is from NIT Delhi
        if not nit_email_required(email):
            flash('Only NIT Delhi email addresses (@nitdelhi.ac.in) are allowed.', 'error')
            return redirect(url_for('login'))
        
        # Check if user exists
        user = User.query.filter_by(email=email).first()
        
        if not user:
            # Create new user
            user = User(
                email=email,
                name=user_info.get('name', ''),
                profile_picture=user_info.get('picture', ''),
                role='student'  # Default role
            )
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
        
        login_user(user)
        
        # Redirect admin users to admin panel
        if user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        
        return redirect(url_for('user_dashboard'))
        
    except Exception as e:
        flash('Authentication failed. Please try again.', 'error')
        app.logger.error(f'OAuth error: {str(e)}')
        return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def user_dashboard():
    # Get user's registered events
    user_registrations = Registration.query.filter_by(user_id=current_user.id).all()
    registered_events = [reg.event for reg in user_registrations]
    
    # Get upcoming events not registered
    upcoming_events = Event.query.filter(
        Event.date >= datetime.now(),
        ~Event.id.in_([event.id for event in registered_events])
    ).order_by(Event.date).limit(5).all()
    
    return render_template('dashboard.html', 
                         registered_events=registered_events,
                         upcoming_events=upcoming_events)

@app.route('/admin')
@admin_required
def admin_dashboard():
    # Get statistics
    total_events = Event.query.count()
    upcoming_events = Event.query.filter(Event.date >= datetime.now()).count()
    total_registrations = Registration.query.count()
    total_users = User.query.count()
    
    # Get recent registrations
    recent_registrations = Registration.query.order_by(Registration.created_at.desc()).limit(5).all()
    
    stats = {
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'total_registrations': total_registrations,
        'total_users': total_users
    }
    
    return render_template('admin/dashboard.html', 
                         stats=stats,
                         recent_registrations=recent_registrations)

# API Routes
@app.route('/api/events')
def api_events():
    events = Event.query.filter(Event.date >= datetime.now()).order_by(Event.date).all()
    return jsonify([{
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.isoformat(),
        'time': event.time.strftime('%H:%M'),
        'location': event.location,
        'instructor': event.instructor,
        'max_participants': event.max_participants,
        'registered_count': len(event.registrations)
    } for event in events])

@app.route('/api/events/<int:event_id>')
def api_event_detail(event_id):
    event = Event.query.get_or_404(event_id)
    return jsonify({
        'id': event.id,
        'title': event.title,
        'description': event.description,
        'date': event.date.isoformat(),
        'time': event.time.strftime('%H:%M'),
        'location': event.location,
        'instructor': event.instructor,
        'max_participants': event.max_participants,
        'registered_count': len(event.registrations),
        'is_registered': current_user.is_authenticated and 
                        Registration.query.filter_by(user_id=current_user.id, event_id=event.id).first() is not None
    })

@app.route('/api/register/<int:event_id>', methods=['POST'])
@login_required
def register_for_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Check if already registered
    existing_registration = Registration.query.filter_by(
        user_id=current_user.id, 
        event_id=event_id
    ).first()
    
    if existing_registration:
        return jsonify({'error': 'Already registered for this event'}), 400
    
    # Check if event is full
    if len(event.registrations) >= event.max_participants:
        return jsonify({'error': 'Event is full'}), 400
    
    # Create registration
    registration = Registration(user_id=current_user.id, event_id=event_id)
    db.session.add(registration)
    db.session.commit()
    
    return jsonify({'message': 'Successfully registered for event'})

@app.route('/api/unregister/<int:event_id>', methods=['POST'])
@login_required
def unregister_from_event(event_id):
    registration = Registration.query.filter_by(
        user_id=current_user.id, 
        event_id=event_id
    ).first()
    
    if not registration:
        return jsonify({'error': 'Not registered for this event'}), 400
    
    db.session.delete(registration)
    db.session.commit()
    
    return jsonify({'message': 'Successfully unregistered from event'})

# Admin API Routes
@app.route('/admin/events')
@admin_required
def admin_events():
    events = Event.query.order_by(Event.date.desc()).all()
    return render_template('admin/events.html', events=events)

@app.route('/admin/events/add', methods=['GET', 'POST'])
@admin_required
def admin_add_event():
    if request.method == 'POST':
        event = Event(
            title=request.form['title'],
            description=request.form['description'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            time=datetime.strptime(request.form['time'], '%H:%M').time(),
            location=request.form['location'],
            instructor=request.form['instructor'],
            max_participants=int(request.form['max_participants'])
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
        return redirect(url_for('admin_events'))
    
    return render_template('admin/add_event.html')

@app.route('/admin/events/<int:event_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if request.method == 'POST':
        event.title = request.form['title']
        event.description = request.form['description']
        event.date = datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        event.time = datetime.strptime(request.form['time'], '%H:%M').time()
        event.location = request.form['location']
        event.instructor = request.form['instructor']
        event.max_participants = int(request.form['max_participants'])
        
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin_events'))
    
    return render_template('admin/edit_event.html', event=event)

@app.route('/admin/events/<int:event_id>/delete', methods=['POST'])
@admin_required
def admin_delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    # Delete all registrations first
    Registration.query.filter_by(event_id=event_id).delete()
    
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully!', 'success')
    return redirect(url_for('admin_events'))

@app.route('/admin/users')
@admin_required
def admin_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/<int:user_id>/role', methods=['POST'])
@admin_required
def admin_change_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.json.get('role')
    
    if new_role in ['student', 'professor', 'admin']:
        user.role = new_role
        db.session.commit()
        return jsonify({'message': 'User role updated successfully'})
    
    return jsonify({'error': 'Invalid role'}), 400

@app.route('/admin/registrations')
@admin_required
def admin_registrations():
    registrations = Registration.query.join(Event).join(User).order_by(Registration.created_at.desc()).all()
    return render_template('admin/registrations.html', registrations=registrations)

@app.route('/api/contact', methods=['POST'])
def api_contact():
    try:
        data = request.get_json() if request.is_json else request.form
        
        contact_message = ContactMessage(
            name=data.get('name'),
            email=data.get('email'),
            message=data.get('message')
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        return jsonify({'message': 'Message sent successfully!'})
    except Exception as e:
        return jsonify({'error': 'Failed to send message'}), 500

# Add moment filter for templates
@app.template_filter('moment')
def moment_filter(dt):
    return datetime.now()

# Initialize first admin user
def create_admin_user():
    admin = User.query.filter_by(role='admin').first()
    if not admin:
        # This would be called manually or through a setup script
        pass

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)