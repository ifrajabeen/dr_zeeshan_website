# from flask_mail import Message
# from app import mail

# def send_appointment_confirmation_email(patient_email, patient_name, appointment):
#     """
#     Appointment confirm hone par patient ko email bhejne ka function
#     """
#     try:
#         subject = "Appointment Confirmed - Dr. Zeeshan Clinic"
        
#         # HTML email template
#         html_body = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
#                 .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
#                 .header {{ background: #28a745; color: white; padding: 20px; text-align: center; }}
#                 .content {{ padding: 20px; background: #f9f9f9; }}
#                 .details {{ background: white; padding: 15px; border-radius: 5px; margin: 20px 0; }}
#                 .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h2>Appointment Confirmed!</h2>
#                 </div>
#                 <div class="content">
#                     <p>Dear {patient_name},</p>
#                     <p>Your appointment has been <strong style="color: #28a745;">confirmed</strong>.</p>
                    
#                     <div class="details">
#                         <h3>Appointment Details:</h3>
#                         <p><strong>Date:</strong> {appointment.appointment_date}</p>
#                         <p><strong>Time:</strong> {appointment.appointment_time}</p>
#                         <p><strong>Doctor:</strong> {appointment.doctor.name}</p>
#                     </div>
                    
#                     <p>Please arrive 10 minutes before your scheduled time.</p>
#                     <p>If you need to reschedule, please contact us.</p>
#                 </div>
#                 <div class="footer">
#                     <p>Dr. Zeeshan Clinic - Your Mental Wellness Partner</p>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
        
#         # Plain text version
#         text_body = f"""
#         Dear {patient_name},
        
#         Your appointment has been CONFIRMED.
        
#         Appointment Details:
#         Date: {appointment.appointment_date}
#         Time: {appointment.appointment_time}
#         Doctor: {appointment.doctor.name}
        
#         Please arrive 10 minutes before your scheduled time.
        
#         Dr. Zeeshan Clinic
#         """
        
#         msg = Message(
#             subject=subject,
#             recipients=[patient_email],
#             html=html_body,
#             body=text_body
#         )
        
#         mail.send(msg)
#         print(f"✅ Confirmation email sent to {patient_email}")
#         return True
        
#     except Exception as e:
#         print(f"❌ Failed to send confirmation email: {str(e)}")
#         return False

# def send_appointment_cancellation_email(patient_email, patient_name, appointment):
#     """
#     Appointment cancel hone par patient ko email bhejne ka function
#     """
#     try:
#         subject = "Appointment Cancelled - Dr. Zeeshan Clinic"
        
#         # HTML email template
#         html_body = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
#                 .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
#                 .header {{ background: #dc3545; color: white; padding: 20px; text-align: center; }}
#                 .content {{ padding: 20px; background: #f9f9f9; }}
#                 .details {{ background: white; padding: 15px; border-radius: 5px; margin: 20px 0; }}
#                 .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h2>Appointment Cancelled</h2>
#                 </div>
#                 <div class="content">
#                     <p>Dear {patient_name},</p>
#                     <p>Your appointment has been <strong style="color: #dc3545;">cancelled</strong>.</p>
                    
#                     <div class="details">
#                         <h3>Appointment Details:</h3>
#                         <p><strong>Date:</strong> {appointment.appointment_date}</p>
#                         <p><strong>Time:</strong> {appointment.appointment_time}</p>
#                         <p><strong>Doctor:</strong> {appointment.doctor.name}</p>
#                     </div>
                    
#                     <p>If you have any questions, please contact us.</p>
#                     <p>We apologize for any inconvenience caused.</p>
#                 </div>
#                 <div class="footer">
#                     <p>Dr. Zeeshan Clinic - Your Mental Wellness Partner</p>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
        
#         # Plain text version
#         text_body = f"""
#         Dear {patient_name},
        
#         Your appointment has been CANCELLED.
        
#         Appointment Details:
#         Date: {appointment.appointment_date}
#         Time: {appointment.appointment_time}
#         Doctor: {appointment.doctor.name}
        
#         If you have any questions, please contact us.
        
#         Dr. Zeeshan Clinic
#         """
        
#         msg = Message(
#             subject=subject,
#             recipients=[patient_email],
#             html=html_body,
#             body=text_body
#         )
        
#         mail.send(msg)
#         print(f"✅ Cancellation email sent to {patient_email}")
#         return True
        
#     except Exception as e:
#         print(f"❌ Failed to send cancellation email: {str(e)}")
#         return False

# def send_appointment_reminder_email(patient_email, patient_name, appointment):
#     """
#     Appointment se pehle reminder email bhejne ka function (optional)
#     """
#     try:
#         subject = "Appointment Reminder - Dr. Zeeshan Clinic"
        
#         html_body = f"""
#         <!DOCTYPE html>
#         <html>
#         <head>
#             <style>
#                 body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
#                 .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
#                 .header {{ background: #17a2b8; color: white; padding: 20px; text-align: center; }}
#                 .content {{ padding: 20px; background: #f9f9f9; }}
#                 .details {{ background: white; padding: 15px; border-radius: 5px; margin: 20px 0; }}
#                 .footer {{ text-align: center; padding: 20px; color: #666; font-size: 12px; }}
#             </style>
#         </head>
#         <body>
#             <div class="container">
#                 <div class="header">
#                     <h2>Appointment Reminder</h2>
#                 </div>
#                 <div class="content">
#                     <p>Dear {patient_name},</p>
#                     <p>This is a reminder for your upcoming appointment.</p>
                    
#                     <div class="details">
#                         <h3>Appointment Details:</h3>
#                         <p><strong>Date:</strong> {appointment.appointment_date}</p>
#                         <p><strong>Time:</strong> {appointment.appointment_time}</p>
#                         <p><strong>Doctor:</strong> {appointment.doctor.name}</p>
#                     </div>
                    
#                     <p>Please arrive 10 minutes before your scheduled time.</p>
#                 </div>
#                 <div class="footer">
#                     <p>Dr. Zeeshan Clinic - Your Mental Wellness Partner</p>
#                 </div>
#             </div>
#         </body>
#         </html>
#         """
        
#         msg = Message(
#             subject=subject,
#             recipients=[patient_email],
#             html=html_body
#         )
        
#         mail.send(msg)
#         print(f"✅ Reminder email sent to {patient_email}")
#         return True
        
#     except Exception as e:
#         print(f"❌ Failed to send reminder email: {str(e)}")
#         return False
# def send_appointment_cancellation_email(patient_email, patient_name, appointment):
#     try:
#         subject = "Appointment Cancelled - Dr. Zeeshan Clinic"
#         html_body = f"<h2>Appointment Cancelled</h2><p>Dear {patient_name},</p><p>Your appointment has been cancelled.</p>"
#         msg = Message(subject, recipients=[patient_email], html=html_body)
#         mail.send(msg)
#         return True
#     except:
#         return False

from flask_mail import Message
from app import mail

def send_confirmation_email(patient_email, patient_name, appointment):
    """Send appointment confirmation email"""
    subject = "✅ Appointment Confirmed - Dr. Zeeshan Clinic"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #2C7A7B, #4FD1C5); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px; }}
            .details {{ background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #2C7A7B; }}
            .footer {{ text-align: center; margin-top: 30px; color: #718096; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Dr. Zeeshan Clinic</h1>
            </div>
            <div class="content">
                <h2 style="color: #1A365D;">Appointment Confirmed!</h2>
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>Your appointment has been confirmed with Dr. Zeeshan Ahmed.</p>
                
                <div class="details">
                    <p><strong>📅 Date:</strong> {appointment.appointment_date}</p>
                    <p><strong>⏰ Time:</strong> {appointment.appointment_time}</p>
                    <p><strong>👨‍⚕️ Doctor:</strong> Dr. Zeeshan Ahmed</p>
                </div>
                
                <div style="background: #E2E8F0; padding: 20px; border-radius: 10px;">
                    <p><strong>📍 Location:</strong> 123 Wellness Street, Medical District</p>
                    <p><strong>📞 Contact:</strong> +1 (555) 123-4567</p>
                </div>
                
                <p style="color: #718096; font-size: 14px; margin-top: 20px;">
                    ⚠️ Please cancel at least 24 hours in advance.
                </p>
            </div>
            <div class="footer">
                <p>Dr. Zeeshan Ahmed - Clinical Psychologist</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = Message(
            subject=subject,
            recipients=[patient_email],
            html=html_template
        )
        mail.send(msg)
        print(f"✅ Confirmation email sent to {patient_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False


def send_completion_email(patient_email, patient_name, appointment):
    """Send appointment completion thank you email"""
    subject = "✨ Appointment Completed - Dr. Zeeshan Clinic"
    
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #1A365D, #2C7A7B); color: white; padding: 30px; text-align: center; border-radius: 10px 10px 0 0; }}
            .content {{ background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px; }}
            .footer {{ text-align: center; margin-top: 30px; color: #718096; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Dr. Zeeshan Clinic</h1>
            </div>
            <div class="content">
                <h2 style="color: #1A365D;">Thank You for Your Visit!</h2>
                <p>Dear <strong>{patient_name}</strong>,</p>
                <p>Your appointment on <strong>{appointment.appointment_date} at {appointment.appointment_time}</strong> has been completed.</p>
                
                <p>We hope you had a productive session. Your well-being is our priority.</p>
                
                <div style="text-align: center; margin: 30px 0;">
                    <p>Share your experience:</p>
                    <a href="http://localhost:5000/reviews" style="background: #2C7A7B; color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px;">
                        Leave a Review
                    </a>
                </div>
            </div>
            <div class="footer">
                <p>Dr. Zeeshan Ahmed - Clinical Psychologist</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    try:
        msg = Message(
            subject=subject,
            recipients=[patient_email],
            html=html_template
        )
        mail.send(msg)
        print(f"✅ Completion email sent to {patient_email}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False