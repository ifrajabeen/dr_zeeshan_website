import smtplib
import os
from dotenv import load_dotenv

# .env file se credentials load karo
load_dotenv()

# Credentials lo
email = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASS')

# Spaces remove karo agar hain to
if password:
    password = password.replace(' ', '')

print("=" * 50)
print("📧 EMAIL CONFIGURATION TEST")
print("=" * 50)
print(f"📧 Email: {email}")
print(f"🔑 Password: {'*' * len(password) if password else 'NOT FOUND'}")
print(f"🔑 Password Length: {len(password) if password else 0} digits")
print("=" * 50)

# Test email address (khud ko hi bhejenge)
test_email = email  # Apne email pe hi test bhejo

try:
    print("🔄 Connecting to Gmail SMTP server...")
    # Gmail SMTP server se connect karo
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()  # Encryption start karo
    print("✅ Connected to server")
    
    print("🔄 Attempting login...")
    # Login karo
    server.login(email, password)
    print("✅ LOGIN SUCCESSFUL! ✅")
    
    # Test email bhejo
    print("🔄 Sending test email...")
    message = f"""Subject: Test Email from Dr. Zeeshan Clinic

    Hello!

    This is a test email to confirm that your email configuration is working correctly.

    If you receive this, your SMTP settings are perfect!

    Best regards,
    Dr. Zeeshan Clinic Team
    """
    
    server.sendmail(email, test_email, message)
    print("✅ TEST EMAIL SENT SUCCESSFULLY! ✅")
    print(f"📨 Check your inbox: {email}")
    
    server.quit()
    print("✅ Server connection closed")
    
except smtplib.SMTPAuthenticationError as e:
    print("❌ AUTHENTICATION FAILED!")
    print("❌ Error:", e)
    print("\n💡 Solutions:")
    print("   1. App password sahi hai?")
    print("   2. 2-Step Verification ON hai?")
    print("   3. Naya app password banao")
    
except smtplib.SMTPException as e:
    print("❌ SMTP ERROR:")
    print("❌ Error:", e)
    
except Exception as e:
    print("❌ GENERAL ERROR:")
    print("❌ Error:", e)
    print("\n💡 Check:")
    print("   - Internet connection")
    print("   - Email address in .env file")
    print("   - App password in .env file")

print("=" * 50)