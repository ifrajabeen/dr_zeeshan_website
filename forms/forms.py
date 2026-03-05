from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField, SelectField, DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange, Optional
from wtforms.widgets import TextArea
from datetime import datetime, date, timedelta

class DoctorProfileForm(FlaskForm):
    """Doctor details update form"""
    name = StringField('Doctor Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    qualifications = TextAreaField('Qualifications', validators=[DataRequired()])
    experience = StringField('Experience (e.g., 15+ years)', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    specializations = TextAreaField('Specializations (comma separated)', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(), Optional()])
    phone = StringField('Phone Number')
    submit = SubmitField('Update Doctor Profile')

class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AppointmentForm(FlaskForm):
    appointment_date = DateField('Preferred Date', validators=[DataRequired()], format='%Y-%m-%d')
    appointment_time = SelectField('Preferred Time', validators=[DataRequired()], choices=[
        ('09:00', '09:00 AM'),
        ('10:00', '10:00 AM'),
        ('11:00', '11:00 AM'),
        ('12:00', '12:00 PM'),
        ('14:00', '02:00 PM'),
        ('15:00', '03:00 PM'),
        ('16:00', '04:00 PM'),
        ('17:00', '05:00 PM')
    ])
    description = TextAreaField('Reason for Visit', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Book Appointment')
    
    def validate_appointment_date(self, field):
        if field.data < date.today():
            raise ValidationError('Appointment date cannot be in the past.')
        if field.data > date.today() + timedelta(days=60):
            raise ValidationError('Appointment cannot be booked more than 60 days in advance.')

class ReviewForm(FlaskForm):
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    comment = TextAreaField('Your Review', validators=[DataRequired(), Length(min=10, max=500)])
    submit = SubmitField('Submit Review')

class UpdateAppointmentStatusForm(FlaskForm):
    status = SelectField('Status', validators=[DataRequired()], choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ])
    submit = SubmitField('Update Status')
class AdminRegistrationForm(FlaskForm):
    """Admin signup ke liye alag form"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    admin_code = StringField('Admin Secret Code', validators=[DataRequired()])  # Secret code for security
    submit = SubmitField('Register as Admin')
class AdminProfileForm(FlaskForm):
    """Admin apni profile update karne ke liye"""
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    current_password = PasswordField('Current Password')
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[EqualTo('new_password')])
    submit = SubmitField('Update Profile')