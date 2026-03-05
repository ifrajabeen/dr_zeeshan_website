# from datetime import datetime
# from flask_login import UserMixin
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager
# # from app import db, login_manager

# db = SQLAlchemy()
# login_manager = LoginManager()
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# class User(UserMixin, db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     phone = db.Column(db.String(20), nullable=True)
#     password_hash = db.Column(db.String(200), nullable=False)
#     role = db.Column(db.String(20), nullable=False, default='patient')
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     is_active = db.Column(db.Boolean, default=True)
    
#     # Relationships
#     appointments = db.relationship('Appointment', backref='patient', lazy=True, foreign_keys='Appointment.patient_id')
#     reviews = db.relationship('Review', backref='patient', lazy=True)
    
#     @property
#     def password(self):
#         raise AttributeError('password is not a readable attribute')
    
#     @password.setter
#     def password(self, password):
#         self.password_hash = generate_password_hash(password)
    
#     def verify_password(self, password):
#         return check_password_hash(self.password_hash, password)
    
#     def is_admin(self):
#         return self.role == 'admin'
    
#     def __repr__(self):
#         return f'<User {self.username}>'

# class Doctor(db.Model):
#     __tablename__ = 'doctors'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     title = db.Column(db.String(100), nullable=False)
#     qualifications = db.Column(db.Text, nullable=False)
#     experience = db.Column(db.String(50), nullable=False)
#     biography = db.Column(db.Text, nullable=False)
#     specializations = db.Column(db.Text, nullable=False)  # Comma-separated
#     email = db.Column(db.String(120), unique=True)
#     phone = db.Column(db.String(20))
#     image_url = db.Column(db.String(200), default='default-doctor.jpg')
    
#     # Relationships
#     appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    
#     @staticmethod
#     def get_doctor():
#         # For simplicity, we assume there's only one doctor
#         doctor = Doctor.query.first()
#         if not doctor:
#             doctor = Doctor(
#                 name='Dr. Zeeshan',
#                 title='Clinical Psychologist',
#                 qualifications='Ph.D. in Clinical Psychology, M.Sc. Counseling Psychology',
#                 experience='15+ years',
#                 biography='Dr. Zeeshan is a highly experienced clinical psychologist dedicated to helping individuals achieve mental wellness and emotional balance.',
#                 specializations='Anxiety Disorders, Depression, PTSD, Relationship Counseling, Stress Management'
#             )
#             db.session.add(doctor)
#             db.session.commit()
#         return doctor
#     def update_details(self, **kwargs):
#         """Doctor ki details update karne ka method"""
#         for key, value in kwargs.items():
#             if hasattr(self, key) and value is not None:
#                 setattr(self, key, value)
#         db.session.commit()
#         return True
    
#     @classmethod
#     def get_or_create(cls):
#         """Doctor record exist na ho to create karo"""
#         doctor = cls.query.first()
#         if not doctor:
#             doctor = cls(
#                 name='Dr. Zeeshan',
#                 title='Clinical Psychologist',
#                 qualifications='Ph.D. in Clinical Psychology',
#                 experience='15+ years',
#                 biography='Experienced clinical psychologist...',
#                 specializations='Anxiety, Depression, PTSD',
#                 email='dr.zeeshan@clinic.com',
#                 phone='+1 (555) 123-4567'
#             )
#             db.session.add(doctor)
#             db.session.commit()
#         return doctor

# class Appointment(db.Model):
#     __tablename__ = 'appointments'
    
#     id = db.Column(db.Integer, primary_key=True)
#     patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
#     appointment_date = db.Column(db.Date, nullable=False)
#     appointment_time = db.Column(db.String(10), nullable=False)
#     description = db.Column(db.Text, nullable=True)
#     status = db.Column(db.String(20), default='pending')  # pending, confirmed, completed, cancelled
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
#     def __repr__(self):
#         return f'<Appointment {self.id} - {self.appointment_date} {self.appointment_time}>'

# class Review(db.Model):
#     __tablename__ = 'reviews'
    
#     id = db.Column(db.Integer, primary_key=True)
#     patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     rating = db.Column(db.Integer, nullable=False)  # 1-5 stars
#     comment = db.Column(db.Text, nullable=False)
#     is_approved = db.Column(db.Boolean, default=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     def __repr__(self):
#         return f'<Review {self.id} - Rating: {self.rating}>'

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# ✅ Yahan par import karo app se, na ke naye objects banao
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

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    qualifications = db.Column(db.Text, nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    biography = db.Column(db.Text, nullable=False)
    specializations = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    image_url = db.Column(db.String(200), default='default-doctor.jpg')
    
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)
    
    @staticmethod
    def get_doctor():
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

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.String(10), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)