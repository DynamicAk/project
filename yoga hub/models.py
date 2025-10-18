from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

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
    
    def is_professor(self):
        return self.role == 'professor'

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(200), nullable=False)
    instructor = db.Column(db.String(100), nullable=False)
    max_participants = db.Column(db.Integer, default=30)
    banner_image = db.Column(db.String(200))
    category = db.Column(db.String(50), default='class')  # class, workshop, retreat
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    registrations = db.relationship('Registration', backref='event', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Event {self.title}>'
    
    def is_full(self):
        return len(self.registrations) >= self.max_participants
    
    def available_spots(self):
        return self.max_participants - len(self.registrations)
    
    def is_upcoming(self):
        return self.date >= datetime.now().date()

class Registration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    status = db.Column(db.String(20), default='registered')  # registered, attended, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Unique constraint to prevent duplicate registrations
    __table_args__ = (db.UniqueConstraint('user_id', 'event_id', name='unique_user_event'),)
    
    def __repr__(self):
        return f'<Registration {self.user.email} -> {self.event.title}>'

class Gallery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), default='general')  # workshops, retreats, daily_practice, general
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Gallery {self.title}>'

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), default='info')  # info, reminder, announcement
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.title}>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    replied = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage from {self.email}>'