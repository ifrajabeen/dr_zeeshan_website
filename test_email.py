import os
from dotenv import load_dotenv

load_dotenv()

email = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASS').replace(' ', '')

print(f"📧 Testing from: {email}")
print(f"🔑 Password length: {len(password)} digits")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    # Connect to Gmail
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = 'ifrazahoor244@gmail.com'
    msg['Subject'] = 'Test Email from Dr. Zeeshan Clinic'
    
    body = "If you receive this, email is working!"
    msg.attach(MIMEText(body, 'plain'))
    
    # Send
    server.send_message(msg)
    server.quit()
    
    print("✅ SUCCESS! Test email sent!")
    
except Exception as e:
    print(f"❌ FAILED: {e}")