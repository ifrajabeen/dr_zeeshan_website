import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASS').replace(' ', '')

# ✅ PATIENT KA EMAIL - YAHI TEST KARNA HAI
patient_email = "hafsanooor3342@gmail.com"

print(f"📧 Sending test email to: {patient_email}")
print(f"📧 From: {email}")

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    
    message = f"""Subject: Test Email from Dr. Zeeshan Clinic

    Hello!

    This is a test email to check if you receive emails from our clinic.

    Best regards,
    Dr. Zeeshan Clinic Team
    """
    
    server.sendmail(email, patient_email, message)
    print(f"✅ Email sent successfully to {patient_email}")
    server.quit()
    
except Exception as e:
    print(f"❌ Failed: {e}")

print("Done!")