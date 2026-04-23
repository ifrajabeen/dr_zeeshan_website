from flask_mail import Message
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

def send_confirmation_email(patient_email, patient_name, appointment):
    """Send appointment confirmation email"""
    subject = "✅ Appointment Confirmed - Dr. Zeeshan Clinic"
    
    html_template = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #2C7A7B, #4FD1C5); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white;">Dr. Zeeshan Clinic</h1>
        </div>
        <div style="background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px;">
            <h2 style="color: #1A365D;">Appointment Confirmed!</h2>
            <p>Dear <strong>{patient_name}</strong>,</p>
            <p>Your appointment has been confirmed with Dr. Zeeshan Ahmed.</p>
            <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>📅 Date:</strong> {appointment.appointment_date}</p>
                <p><strong>⏰ Time:</strong> {appointment.appointment_time}</p>
                <p><strong>👨‍⚕️ Doctor:</strong> Dr. Zeeshan Ahmed</p>
            </div>
            <p><strong>📍 Location:</strong> 123 Wellness Street, Medical District</p>
            <p><strong>📞 Contact:</strong> +1 (555) 123-4567</p>
        </div>
    </div>
    """
    
    try:
        # ✅ HARDCODED CREDENTIALS - Direct SMTP
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASS')  # APKA 16-DIGIT APP PASSWORD
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = patient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_template, 'html'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Confirmation email sent to {patient_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def send_completion_email(patient_email, patient_name, appointment):
    """Send appointment completion email"""
    subject = "✨ Appointment Completed - Dr. Zeeshan Clinic"
    
    html_template = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #1A365D, #2C7A7B); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white;">Dr. Zeeshan Clinic</h1>
        </div>
        <div style="background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px;">
            <h2 style="color: #1A365D;">Thank You for Your Visit!</h2>
            <p>Dear <strong>{patient_name}</strong>,</p>
            <p>Your appointment on <strong>{appointment.appointment_date} at {appointment.appointment_time}</strong> has been completed.</p>
            <p>We hope you had a productive session with Dr. Zeeshan.</p>
            <div style="text-align: center; margin-top: 30px;">
                <a href="http://localhost:5000/reviews" style="background: #2C7A7B; color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px;">Leave a Review</a>
            </div>
        </div>
    </div>
    """
    
    try:
        # ✅ HARDCODED CREDENTIALS - Direct SMTP
        sender_email = os.getenv('EMAIL_USER')
        sender_password = os.getenv('EMAIL_PASS')  # APKA 16-DIGIT APP PASSWORD
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = patient_email
        msg['Subject'] = subject
        
        msg.attach(MIMEText(html_template, 'html'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Completion email sent to {patient_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

def send_appointment_booking_email(patient_email, patient_name, appointment):
    """Send appointment booking confirmation email (when patient books)"""
    subject = "📅 Appointment Request Received - Dr. Zeeshan Clinic"
    
    html_template = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <div style="background: linear-gradient(135deg, #2C7A7B, #4FD1C5); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
            <h1 style="color: white;">Dr. Zeeshan Clinic</h1>
        </div>
        <div style="background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px;">
            <h2>Appointment Request Received!</h2>
            <p>Dear <strong>{patient_name}</strong>,</p>
            <p>Your appointment request has been received.</p>
            <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
                <p><strong>📅 Date:</strong> {appointment.appointment_date}</p>
                <p><strong>⏰ Time:</strong> {appointment.appointment_time}</p>
            </div>
            <p>We will confirm your appointment soon.</p>
            <p>You will receive another email once confirmed.</p>
        </div>
    </div>
    """
    
    try:
        from flask_mail import Mail
        mail = Mail(current_app)
        
        msg = Message(subject, recipients=[patient_email], html=html_template)
        mail.send(msg)
        print(f"✅ Booking email sent to {patient_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False
    
def send_appointment_cancellation_email(patient_email, patient_name, appointment):
    """Send appointment cancellation email notification"""
    subject = "❌ Appointment Cancelled - Dr. Zeeshan Clinic"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #EF4444, #DC2626); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px; }}
            .details {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #EF4444; }}
            .footer {{ text-align: center; margin-top: 30px; color: #718096; font-size: 14px; }}
            .button {{ background: #2C7A7B; color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px; display: inline-block; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="color: white;">Dr. Zeeshan Clinic</h1>
            </div>
            <div class="content">
                <h2 style="color: #1A365D;">Appointment Cancelled</h2>
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>We regret to inform you that your appointment has been cancelled.</p>
                
                <div class="details">
                    <p><strong>📅 Date:</strong> {appointment.appointment_date}</p>
                    <p><strong>⏰ Time:</strong> {appointment.appointment_time}</p>
                    <p><strong>👨‍⚕️ Doctor:</strong> Dr. Zeeshan Ahmed</p>
                </div>
                
                <p>If you wish to reschedule, please book a new appointment on our website.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <a href="http://localhost:5000/appointment" class="button">Book New Appointment</a>
                </div>
                
                <p style="color: #718096;">We apologize for any inconvenience caused.</p>
            </div>
            <div class="footer">
                <p>Dr. Zeeshan Ahmed - Clinical Psychologist<br>Helping you achieve mental wellness</p>
                <p>📞 +1 (555) 123-4567 | 📧 contact@drzeeshanclinic.com</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        from flask_mail import Mail
        from flask_mail import Message
        from flask import current_app
        
        mail = Mail(current_app)
        msg = Message(subject, recipients=[patient_email], html=html_template)
        mail.send(msg)
        print(f"✅ Cancellation email sent to {patient_email}")
        return True
    except Exception as e:
        print(f"❌ Cancellation email failed: {e}")
        return False