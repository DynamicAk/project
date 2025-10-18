# 🕉️ Sangam Yoga Club - NIT Delhi

A comprehensive web application for managing yoga club activities, events, and community engagement at NIT Delhi.

## ✨ Features

### 🏠 **Public Features**
- **Modern Homepage** with hero section, about information, and upcoming events
- **Event Listings** with detailed information and registration capabilities
- **Gallery** showcasing yoga sessions and activities
- **Contact Form** for inquiries and feedback
- **Responsive Design** optimized for all devices

### 🔐 **Authentication System**
- **Google OAuth Integration** restricted to @nitdelhi.ac.in emails
- **Role-based Access Control** (Student, Professor, Admin)
- **Secure Session Management**

### 👤 **User Dashboard**
- **Personal Profile** with Google account integration
- **Event Registration Management** (register/unregister)
- **Event History** and upcoming events view
- **Notification Preferences**

### 🛠️ **Admin Panel**
- **Complete Event Management** (Create, Read, Update, Delete)
- **User Management** with role assignment
- **Registration Tracking** and analytics
- **Contact Message Management**
- **Gallery Management** for photos and media

### 📊 **Database Models**
- **Users** with roles and profile information
- **Events** with scheduling, capacity, and details
- **Registrations** with status tracking
- **Gallery** items with categorization
- **Contact Messages** for inquiries

## 🚀 Quick Start

### 1. **Prerequisites**
```bash
# Python 3.8+ required
python --version

# Install pip if not available
# Windows: python -m ensurepip --upgrade
# macOS/Linux: usually pre-installed
```

### 2. **Clone & Setup**
```bash
# Navigate to project directory
cd "a:\study\web development\yoga hub"

# Install dependencies
pip install -r requirements.txt
```

### 3. **Environment Configuration**
```bash
# Copy environment template
copy .env.example .env

# Edit .env file with your credentials
notepad .env
```

**Required Environment Variables:**
```env
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Google OAuth Credentials (Get from Google Console)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Database URL
DATABASE_URL=sqlite:///yoga_club.db
```

### 4. **Google OAuth Setup**
1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select existing one
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Add authorized redirect URIs:
   - `http://localhost:5000/auth/google/callback`
6. Add authorized JavaScript origins:
   - `http://localhost:5000`

### 5. **Initialize Database**
```bash
# Run setup script to create database and sample data
python setup.py
```

### 6. **Start Application**
```bash
# Development server
python app.py

# Production server (optional)
gunicorn --bind 0.0.0.0:5000 app:app
```

### 7. **Access Application**
- **Homepage**: http://localhost:5000
- **Login**: http://localhost:5000/login
- **Admin Panel**: http://localhost:5000/admin (admin users only)

## 👥 Default Test Accounts

The setup script creates these test accounts:
- **Admin**: `admin@nitdelhi.ac.in`
- **Professor**: `prof.rajesh@nitdelhi.ac.in`
- **Student**: `student1@nitdelhi.ac.in`

*Note: These are for development only. In production, use actual Google OAuth.*

## 📱 User Guide

### **For Students/Faculty:**
1. **Login** with your @nitdelhi.ac.in Google account
2. **Browse Events** on the homepage or events section
3. **Register** for events with one-click registration
4. **Manage Registrations** from your dashboard
5. **Contact** the club through the contact form

### **For Admins:**
1. **Access Admin Panel** after logging in as admin
2. **Manage Events**: Create, edit, delete yoga sessions
3. **User Management**: View users and assign roles
4. **Track Registrations**: Monitor event participation
5. **Handle Inquiries**: Respond to contact messages

## 🗄️ Database Schema

### **Users Table**
- `id`, `email`, `name`, `profile_picture`
- `role` (student/professor/admin)
- `notifications_enabled`, `created_at`

### **Events Table**
- `id`, `title`, `description`, `date`, `time`
- `location`, `instructor`, `max_participants`
- `category` (class/workshop/retreat)

### **Registrations Table**
- `id`, `user_id`, `event_id`
- `status` (registered/attended/cancelled)
- `created_at`

### **Additional Tables**
- **Gallery**: Event photos and media
- **ContactMessage**: User inquiries and feedback

## 🎨 Design System

### **Colors**
- **Primary Blue**: `#3A86FF` (Trust, Calm)
- **Primary Green**: `#4CAF50` (Health, Energy)
- **White**: `#FFFFFF` (Peace, Clarity)
- **Soft Gray**: `#F5F5F5` (Background)

### **Typography**
- **Headings**: Poppins (Clean, Modern)
- **Body Text**: Lato (Readable, Professional)

### **Visual Elements**
- **Gradients**: Blue → Green transitions
- **Cards**: Clean with subtle shadows
- **Icons**: Font Awesome for consistency
- **Animations**: Smooth transitions and hover effects

## 🔧 Development

### **Project Structure**
```
yoga hub/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── setup.py              # Database initialization
├── .env.example          # Environment template
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       └── main.js       # JavaScript functionality
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── dashboard.html    # User dashboard
│   └── admin/
│       ├── dashboard.html # Admin dashboard
│       ├── events.html   # Event management
│       ├── users.html    # User management
│       └── add_event.html # Event creation
└── yoga_club.db          # SQLite database (created automatically)
```

### **API Endpoints**
- `GET /api/events` - List all events
- `GET /api/events/<id>` - Event details
- `POST /api/register/<id>` - Register for event
- `POST /api/unregister/<id>` - Unregister from event
- `POST /api/contact` - Submit contact message

### **Admin Routes**
- `/admin` - Admin dashboard
- `/admin/events` - Event management
- `/admin/users` - User management
- `/admin/registrations` - Registration tracking

## 🚀 Deployment

### **Production Setup**
1. **Environment**: Set `FLASK_ENV=production`
2. **Database**: Use PostgreSQL instead of SQLite
3. **Web Server**: Use Gunicorn + Nginx
4. **HTTPS**: Required for Google OAuth in production
5. **Domain**: Update OAuth settings with production domain

### **Environment Variables (Production)**
```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@localhost/yoga_club_db
GOOGLE_CLIENT_ID=your-production-client-id
GOOGLE_CLIENT_SECRET=your-production-client-secret
```

## 🛡️ Security

- **OAuth Authentication**: Only @nitdelhi.ac.in emails allowed
- **Role-based Access**: Admins, Professors, Students have different permissions
- **CSRF Protection**: Built-in Flask security
- **Input Validation**: All forms validated on server-side
- **SQL Injection Protection**: SQLAlchemy ORM prevents attacks

## 🤝 Contributing

1. **Fork** the repository
2. **Create** feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** Pull Request

## 📝 License

This project is created for educational purposes as part of NIT Delhi's yoga club management system.

## 🆘 Support

For technical support or questions:
- **Email**: sangamyoga@nitdelhi.ac.in
- **GitHub Issues**: Create an issue for bugs or feature requests
- **Documentation**: Check this README for common questions

## 🎯 Future Enhancements

- **Email Notifications**: Automatic event reminders
- **Calendar Integration**: Sync with Google Calendar
- **Payment Integration**: For premium workshops
- **Mobile App**: React Native companion app
- **Analytics Dashboard**: Detailed participation metrics
- **Instructor Portal**: Separate interface for instructors

---

**Built with ❤️ for the NIT Delhi Community**

*Promoting wellness and mindfulness through technology*