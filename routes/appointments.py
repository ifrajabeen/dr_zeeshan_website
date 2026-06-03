from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.models import Appointment, Doctor
from forms.forms import AppointmentForm
from utils.email_helper import send_appointment_booking_email

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

        booking_email_sent = send_appointment_booking_email(
            patient_email=current_user.email,
            patient_name=current_user.first_name,
            appointment=appointment,
        )

        if booking_email_sent:
            flash('Appointment booked successfully! A confirmation email has been sent.', 'success')
        else:
            flash('Appointment booked successfully, but confirmation email could not be sent.', 'warning')
        return redirect(url_for('main.index'))

    return render_template('appointment.html', form=form, doctor=doctor, title='Book Appointment')


@appointments_bp.route('/dashboard')
@login_required
def dashboard():
    appointments = Appointment.query.filter_by(patient_id=current_user.id).order_by(
        Appointment.appointment_date.desc()
    ).all()

    return render_template(
        'dashboard.html',
        appointments=appointments,
        title='My Dashboard'
    )
