# from flask_mail import Message
# from flask import current_app, render_template
# import logging
# import smtplib

# # Logging setup
# logging.basicConfig(level=logging.DEBUG)

# def send_appointment_confirmation_email(patient_email, patient_name, appointment):
#     """Appointment confirm hone par patient ko email bhejne ka function"""
    
#     print(f"📧 DEBUG: Sending confirmation email to patient: {patient_email}")
    
#     subject = "Your Appointment Confirmed - Dr. Zeeshan Clinic"
    
#     # HTML email body
#     html_body = f"""
#     <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
#         <div style="background: linear-gradient(135deg, #2C7A7B, #4FD1C5); padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
#             <h1 style="color: white; margin: 0;">Dr. Zeeshan Clinic</h1>
#         </div>
#         <div style="background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px;">
#             <h2 style="color: #1A365D;">Appointment Confirmed!</h2>
#             <p style="color: #2D3748;">Dear <strong>{patient_name}</strong>,</p>
#             <p style="color: #2D3748;">Your appointment has been confirmed with Dr. Zeeshan Ahmed.</p>
            
#             <div style="background: white; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #2C7A7B;">
#                 <p style="margin: 5px 0;"><strong>📅 Date:</strong> {appointment.appointment_date}</p>
#                 <p style="margin: 5px 0;"><strong>⏰ Time:</strong> {appointment.appointment_time}</p>
#                 <p style="margin: 5px 0;"><strong>👨‍⚕️ Doctor:</strong> Dr. Zeeshan Ahmed</p>
#             </div>
            
#             <div style="background: #E2E8F0; padding: 20px; border-radius: 10px; margin: 20px 0;">
#                 <p style="margin: 5px 0;"><strong>📍 Location:</strong> 123 Wellness Street, Medical District</p>
#                 <p style="margin: 5px 0;"><strong>📞 Phone:</strong> +1 (555) 123-4567</p>
#             </div>
            
#             <p style="color: #718096; font-size: 14px;">
#                 ⚠️ Please cancel at least 24 hours in advance if you need to reschedule.
#             </p>
            
#             <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 20px 0;">
            
#             <p style="color: #718096; text-align: center;">
#                 Dr. Zeeshan Ahmed - Clinical Psychologist<br>
#                 Helping you achieve mental wellness
#             </p>
#         </div>
#     </div>
#     """
    
#     # current_app se mail lo
#     from flask_mail import Mail
#     mail = Mail(current_app)
    
#     msg = Message(
#         subject=subject,
#         recipients=[patient_email],
#         html=html_body
#     )
    
#     try:
#         mail.send(msg)
#         print(f"✅ Email sent successfully to {patient_email}")
#         return True  #✅ YEH ADD KARO!
#     except Exception as e:
#         print(f"❌ Error sending email to {patient_email}: {e}")
#         return False

# def send_appointment_cancellation_email(patient_email, patient_name, appointment):
#     """Appointment cancel hone par patient ko email bhejne ka function"""
    
#     print(f"📧 DEBUG: Sending cancellation email to patient: {patient_email}")
    
#     subject = "Appointment Cancelled - Dr. Zeeshan Clinic"
    
#     html_body = f"""
#     <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
#         <div style="background: #EF4444; padding: 30px; text-align: center; border-radius: 10px 10px 0 0;">
#             <h1 style="color: white; margin: 0;">Dr. Zeeshan Clinic</h1>
#         </div>
#         <div style="background: #F7FAFC; padding: 30px; border-radius: 0 0 10px 10px;">
#             <h2 style="color: #1A365D;">Appointment Cancelled</h2>
#             <p style="color: #2D3748;">Dear <strong>{patient_name}</strong>,</p>
#             <p style="color: #2D3748;">Your appointment on <strong>{appointment.appointment_date} at {appointment.appointment_time}</strong> has been cancelled.</p>
            
#             <p style="color: #2D3748;">If you wish to reschedule, please book a new appointment on our website.</p>
            
#             <div style="text-align: center; margin: 30px 0;">
#                 <a href="http://localhost:5000/appointment" 
#                    style="background: #2C7A7B; color: white; padding: 12px 30px; text-decoration: none; border-radius: 50px;">
#                     Book New Appointment
#                 </a>
#             </div>
            
#             <hr style="border: none; border-top: 1px solid #E2E8F0; margin: 20px 0;">
            
#             <p style="color: #718096; text-align: center;">
#                 For any questions, call us at +1 (555) 123-4567
#             </p>
#         </div>
#     </div>
#     """
    
#     # current_app se mail lo
#     from flask_mail import Mail
#     mail = Mail(current_app)
    
#     msg = Message(
#         subject=subject,
#         recipients=[patient_email],
#         html=html_body
#     )
    
#     try:
#         logging.debug("Attempting to send cancellation email...")
#         mail.send(msg)
#         print(f"✅ Cancellation email sent successfully to {patient_email}")
#         return True
#     except Exception as e:
#         print(f"❌ Error sending cancellation email to {patient_email}: {e}")
#         return False


from flask_mail import Message
from flask import current_app

def send_appointment_confirmation_email(patient_email, patient_name, appointment):
    """Appointment confirm hone par patient ko email bhejo"""
    
    print(f"Sending email to: {patient_email}")
    
    subject = "Appointment Confirmed - Dr. Zeeshan Clinic"
    
    # Simple text email (HTML ki zaroorat nahi)
    body = f"""
    Dear {patient_name},
    
    Your appointment has been confirmed!
    
    Date: {appointment.appointment_date}
    Time: {appointment.appointment_time}
    Doctor: Dr. Zeeshan Ahmed
    
    Thanks,
    Dr. Zeeshan Clinic
    """
    
    # Mail object banao
    from flask_mail import Mail
    mail = Mail(current_app)
    
    msg = Message(subject, recipients=[patient_email], body=body)
    
    try:
        mail.send(msg)
        print(f"✅ Email sent to {patient_email}")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False