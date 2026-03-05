from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from models.models import Appointment, Doctor
from forms.forms import AppointmentForm
# from datetime import datetime

appointments_bp = Blueprint('appointments', __name__)

@appointments_bp.route('/appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    doctor = Doctor.get_doctor()
    
    if form.validate_on_submit():
        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor.id,
            appointment_date=form.appointment_date.data,
            appointment_time=form.appointment_time.data,
            description=form.description.data,
            status='pending'
        )
        db.session.add(appointment)
        db.session.commit()
        
        flash('Appointment booked successfully! We will confirm it shortly.', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('appointment.html', form=form, doctor=doctor, title='Book Appointment')

@appointments_bp.route('/dashboard')
@login_required
def dashboard():
    doctor = Doctor.get_doctor()
    
    # Patient ke appointments
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(
        Appointment.appointment_date.desc()
    ).all()
    
#  Admin
    stats = {}
    if current_user.is_admin():
        from models.models import User, Review
        stats = {
            'total_appointments': Appointment.query.count(),
            'pending_appointments': Appointment.query.filter_by(status='pending').count(),
            'total_patients': User.query.filter_by(role='patient').count(),
            'pending_reviews': Review.query.filter_by(is_approved=False).count()
        }
    
    # ✅ STATS template
    return render_template('dashboard.html', 
                         appointments=appointments, 
                         doctor=doctor,
                         stats=stats,  # ✅ YEH IMPORTANT HAI
                         title='My Dashboard')