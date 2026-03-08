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

def send_appointment_confirmation_email(patient_email, patient_name, appointment):
    """Appointment confirm hone par email"""
    try:
        msg = Message(
            subject="Appointment Confirmed - Dr. Zeeshan Clinic",
            recipients=[patient_email],
            html=f"<h2>Appointment Confirmed!</h2><p>Dear {patient_name},</p><p>Your appointment has been confirmed.</p>"
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

def send_appointment_cancellation_email(patient_email, patient_name, appointment):
    """Appointment cancel hone par email"""
    try:
        msg = Message(
            subject="Appointment Cancelled - Dr. Zeeshan Clinic",
            recipients=[patient_email],
            html=f"<h2>Appointment Cancelled</h2><p>Dear {patient_name},</p><p>Your appointment has been cancelled.</p>"
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False