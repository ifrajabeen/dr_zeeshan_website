from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, PasswordField, DateField, TimeField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, URL, ValidationError
from flask_wtf.file import FileField, FileAllowed

# ========== LOGIN FORM ==========
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

# ========== REGISTRATION FORM ==========
class RegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

# ========== ADMIN REGISTRATION FORM ==========
class AdminRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    admin_code = StringField('Admin Code', validators=[DataRequired()])
    submit = SubmitField('Register as Admin')

# ========== APPOINTMENT FORM ==========
class AppointmentForm(FlaskForm):
    appointment_date = DateField('Appointment Date', validators=[DataRequired()])
    appointment_time = StringField('Appointment Time', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    submit = SubmitField('Book Appointment')

# ========== REVIEW FORM ==========
class ReviewForm(FlaskForm):
    rating = SelectField('Rating', choices=[(5, '5 Stars'), (4, '4 Stars'), (3, '3 Stars'), (2, '2 Stars'), (1, '1 Star')], coerce=int)
    comment = TextAreaField('Your Review', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Submit Review')

# ========== DOCTOR PROFILE FORM ==========
class DoctorProfileForm(FlaskForm):
    name = StringField('Doctor Name', validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    qualifications = TextAreaField('Qualifications', validators=[DataRequired()])
    experience = StringField('Experience', validators=[DataRequired()])
    biography = TextAreaField('Biography', validators=[DataRequired()])
    specializations = TextAreaField('Specializations', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    image = FileField('Profile Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    submit = SubmitField('Update Profile')

# ========== UPDATE APPOINTMENT STATUS FORM ==========
class UpdateAppointmentStatusForm(FlaskForm):
    status = SelectField('Status', choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], validators=[DataRequired()])
    submit = SubmitField('Update Status')

# ========== ADMIN PROFILE FORM ==========
class AdminProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional()])
    current_password = PasswordField('Current Password', validators=[Optional()])
    new_password = PasswordField('New Password', validators=[Optional(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[Optional(), EqualTo('new_password')])
    submit = SubmitField('Update Profile')

# ========== SETTINGS FORM ==========
class SettingForm(FlaskForm):
    clinic_name = StringField('Clinic Name', validators=[Optional()])
    phone_primary = StringField('Primary Phone', validators=[Optional()])
    phone_secondary = StringField('Secondary Phone', validators=[Optional()])
    email_contact = StringField('Contact Email', validators=[Optional(), Email()])
    address = TextAreaField('Address', validators=[Optional()])
    working_hours = StringField('Working Hours', validators=[Optional()])
    consultation_fee = StringField('Consultation Fee', validators=[Optional()])
    facebook_url = StringField('Facebook URL', validators=[Optional(), URL()])
    twitter_url = StringField('Twitter URL', validators=[Optional(), URL()])
    instagram_url = StringField('Instagram URL', validators=[Optional(), URL()])
    linkedin_url = StringField('LinkedIn URL', validators=[Optional(), URL()])
    footer_description = TextAreaField('Footer Description', validators=[Optional()])
    submit = SubmitField('Save Settings')

# ========== SERVICE FORM ==========
class ServiceForm(FlaskForm):
    title = StringField('Service Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    icon = StringField('Icon Class', validators=[DataRequired()])
    order = IntegerField('Display Order', default=0)
    is_active = SelectField('Status', choices=[('True', 'Active'), ('False', 'Inactive')], default='True')
    submit = SubmitField('Save Service')
    
    def validate_icon(self, field):
        if not field.data.startswith('fa-'):
            raise ValidationError('Icon class "fa-" se shuru hona chahiye')

# ========== FORGOT PASSWORD FORM ==========
class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password')

# ========== RESET PASSWORD FORM ==========
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')