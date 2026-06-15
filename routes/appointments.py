from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.models import Appointment, Doctor
from forms.forms import AppointmentForm
from utils.email_helper import send_appointment_booking_email
from datetime import datetime, time, date
import re

appointments_bp = Blueprint('appointments', __name__)

TIME_SLOT_PATTERN = re.compile(r'^(0?\d|1\d|2[0-3]):[0-5]\d$')
ALLOWED_START = time(9, 0)
ALLOWED_END = time(17, 0)


@appointments_bp.route('/appointment', methods=['GET', 'POST'])
@login_required
def book_appointment():
    form = AppointmentForm()
    doctor = Doctor.get_doctor()

    if form.validate_on_submit():
        appointment_date = form.appointment_date.data
        appointment_time_text = (form.appointment_time.data or '').strip()

        if appointment_date < date.today():
            form.appointment_date.errors.append('Please choose today or a future date.')
            flash('Please choose today or a future date.', 'warning')
            return render_template('appointment.html', form=form, doctor=doctor, title='Book Appointment')

        if not TIME_SLOT_PATTERN.match(appointment_time_text):
            form.appointment_time.errors.append('Please enter a valid time like 09:00 or 14:30.')
            flash('Please enter a valid time like 09:00 or 14:30.', 'warning')
            return render_template('appointment.html', form=form, doctor=doctor, title='Book Appointment')

        parsed_time = datetime.strptime(appointment_time_text, '%H:%M').time()
        if parsed_time < ALLOWED_START or parsed_time > ALLOWED_END:
            form.appointment_time.errors.append('Please select a time between 09:00 and 17:00.')
            flash('Please select a time between 09:00 and 17:00.', 'warning')
            return render_template('appointment.html', form=form, doctor=doctor, title='Book Appointment')

        existing_appointment = Appointment.query.filter_by(
            doctor_id=doctor.id,
            appointment_date=appointment_date,
            appointment_time=appointment_time_text
        ).first()

        if existing_appointment:
            form.appointment_time.errors.append('This time slot is already booked. Please choose another slot.')
            flash('This time slot is already booked. Please choose another slot.', 'danger')
            return render_template('appointment.html', form=form, doctor=doctor, title='Book Appointment')

        appointment = Appointment(
            patient_id=current_user.id,
            doctor_id=doctor.id,
            appointment_date=appointment_date,
            appointment_time=appointment_time_text,
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

    elif form.is_submitted():
        flash('Please fix the highlighted appointment fields and try again.', 'danger')

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
