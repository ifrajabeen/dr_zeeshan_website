from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Import from app
from app import db, login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='patient')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='patient', lazy=True, foreign_keys='Appointment.patient_id')
    reviews = db.relationship('Review', backref='patient', lazy=True)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def __repr__(self):
        return f'<User {self.username}>'

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.Text, nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    specializations = db.Column(db.Text, nullable=False)  # Comma-separated
    email = db.Column(db.String(120), unique=True)
    phone = db.Column(db.String(20))
    image_url = db.Column(db.String(200), default='default-doctor.jpg')
    
    # Relationships
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    
    @staticmethod
    def get_doctor():
        # For simplicity, we assume there's only one doctor
        doctor = Doctor.query.first()
        if not doctor:
            doctor = Doctor(
                name='Dr. Zeeshan',
                title='Clinical Psychologist',
                qualifications='Ph.D. in Clinical Psychology, M.Sc. Counseling Psychology',
                experience='15+ years',
                biography='Dr. Zeeshan is a highly experienced clinical psychologist dedicated to helping individuals achieve mental wellness and emotional balance.',
                specializations='Anxiety Disorders, Depression, PTSD, Relationship Counseling, Stress Management',
                email='dr.zeeshan@clinic.com',
                phone='+1 (555) 123-4567'
            )
            db.session.add(doctor)
            db.session.commit()
        return doctor
    
    def update_details(self, **kwargs):
        """Update doctor details"""
        for key, value in kwargs.items():
            if hasattr(self, key) and value is not None:
                setattr(self, key, value)
        db.session.commit()
        return True
    
    @classmethod
    def get_or_create(cls):
        """Create doctor if doesn't exist"""
        doctor = cls.query.first()
        if not doctor:
            doctor = cls(
                name='Dr. Zeeshan',
                title='Clinical Psychologist',
                qualifications='Ph.D. in Clinical Psychology',
                experience='15+ years',
                biography='Experienced clinical psychologist...',
                specializations='Anxiety, Depression, PTSD',
                email='dr.zeeshan@clinic.com',
                phone='+1 (555) 123-4567'
            )
            db.session.add(doctor)
            db.session.commit()
        return doctor

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Appointment {self.id} - {self.appointment_date} {self.appointment_time}>'

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
    comment = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.id} - Rating: {self.rating}>'

# ✅ NEW: Settings model for dynamic content
class Setting(db.Model):
    __tablename__ = 'settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=True)
    value_type = db.Column(db.String(20), default='text')  # text, number, email, phone, image
    description = db.Column(db.String(200), nullable=True)  # Optional description for admin panel
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Setting {self.key}: {self.value}>'
    
    @classmethod
    def get(cls, key, default=None):
        """Get a setting value by key"""
        setting = cls.query.filter_by(key=key).first()
        return setting.value if setting else default
    
    @classmethod
    def set(cls, key, value, value_type='text', description=None):
        """Set a setting value"""
        setting = cls.query.filter_by(key=key).first()
        if setting:
            setting.value = value
            setting.value_type = value_type
            if description:
                setting.description = description
        else:
            setting = cls(key=key, value=value, value_type=value_type, description=description)
            db.session.add(setting)
        db.session.commit()
        return setting
    
    @classmethod
    def get_all_dict(cls):
        """Get all settings as a dictionary"""
        settings = {}
        for setting in cls.query.all():
            settings[setting.key] = setting.value
        return settings

# ✅ NEW: Service model for dynamic services
class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    icon = db.Column(db.String(50), default='fa-heartbeat')  # Font Awesome icon class
    order = db.Column(db.Integer, default=0)  # For ordering services
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Service {self.title}>'