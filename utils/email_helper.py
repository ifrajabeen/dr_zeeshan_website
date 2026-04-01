import smtplib

from flask import current_app
from flask_mail import Message

from app import mail


def _appointment_details(appointment):
    doctor_name = getattr(getattr(appointment, 'doctor', None), 'name', 'Dr. Zeeshan')
    return (
        f"Date: {appointment.appointment_date}\n"
        f"Time: {appointment.appointment_time}\n"
        f"Doctor: {doctor_name}"
    )


def _send_email(subject, patient_email, html_body, text_body):
    """Centralized email sender with consistent logging and error handling."""
    cfg = current_app.config
    mail_username = str(cfg.get('MAIL_USERNAME', '')).strip()
    mail_password = str(cfg.get('MAIL_PASSWORD', '')).strip()
    if not mail_username or not mail_password:
        current_app.logger.warning(
            "Email not sent to %s because SMTP config is incomplete (MAIL_USERNAME/MAIL_PASSWORD).",
            patient_email,
        )
        return False

    try:
        msg = Message(
            subject=subject,
            recipients=[patient_email],
            html=html_body,
            body=text_body,
        )
        mail.send(msg)
        return True
    except smtplib.SMTPAuthenticationError as exc:
        current_app.logger.error(
            "SMTP authentication failed for user '%s' while sending to %s: %s",
            mail_username,
            patient_email,
            exc,
        )
        return False
    except Exception as exc:
        current_app.logger.error("Failed to send email to %s: %s", patient_email, exc)
        return False


def send_appointment_booking_email(patient_email, patient_name, appointment):
    """Send acknowledgement immediately after booking request is created."""
    details = _appointment_details(appointment)
    html_body = (
        f"<h2>Appointment Request Received</h2>"
        f"<p>Dear {patient_name},</p>"
        "<p>We received your appointment request. Our team will review and confirm it shortly.</p>"
        f"<pre>{details}</pre>"
    )
    text_body = (
        f"Dear {patient_name},\n\n"
        "We received your appointment request. Our team will review and confirm it shortly.\n\n"
        f"{details}\n\n"
        "Dr. Zeeshan Clinic"
    )
    return _send_email(
        subject="Appointment Request Received - Dr. Zeeshan Clinic",
        patient_email=patient_email,
        html_body=html_body,
        text_body=text_body,
    )


def send_appointment_confirmation_email(patient_email, patient_name, appointment):
    """Send email when appointment is confirmed by admin."""
    details = _appointment_details(appointment)
    html_body = (
        f"<h2>Appointment Confirmed</h2>"
        f"<p>Dear {patient_name},</p>"
        "<p>Your appointment has been confirmed.</p>"
        f"<pre>{details}</pre>"
    )
    text_body = (
        f"Dear {patient_name},\n\n"
        "Your appointment has been confirmed.\n\n"
        f"{details}\n\n"
        "Please arrive 10 minutes before your time slot.\n\n"
        "Dr. Zeeshan Clinic"
    )
    return _send_email(
        subject="Appointment Confirmed - Dr. Zeeshan Clinic",
        patient_email=patient_email,
        html_body=html_body,
        text_body=text_body,
    )


def send_appointment_cancellation_email(patient_email, patient_name, appointment):
    """Send email when appointment is cancelled by admin."""
    details = _appointment_details(appointment)
    html_body = (
        f"<h2>Appointment Cancelled</h2>"
        f"<p>Dear {patient_name},</p>"
        "<p>Your appointment has been cancelled. Please contact the clinic for re-scheduling.</p>"
        f"<pre>{details}</pre>"
    )
    text_body = (
        f"Dear {patient_name},\n\n"
        "Your appointment has been cancelled. Please contact the clinic for re-scheduling.\n\n"
        f"{details}\n\n"
        "Dr. Zeeshan Clinic"
    )
    return _send_email(
        subject="Appointment Cancelled - Dr. Zeeshan Clinic",
        patient_email=patient_email,
        html_body=html_body,
        text_body=text_body,
    )