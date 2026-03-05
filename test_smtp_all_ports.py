import smtplib
import socket
from dotenv import load_dotenv
import os

load_dotenv()

email = os.getenv('EMAIL_USER')
password = os.getenv('EMAIL_PASS').replace(' ', '')

# Different ports to test
ports = [25, 465, 587, 2525]

print("=" * 60)
print(f"📧 Testing SMTP connections from: {email}")
print("=" * 60)

# First test basic network connectivity
def test_network(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

# Test Gmail connectivity
print("\n🔍 Testing network connectivity to Gmail...")
if test_network('smtp.gmail.com', 587):
    print("✅ Can reach smtp.gmail.com:587")
else:
    print("❌ Cannot reach smtp.gmail.com:587")

# Test different ports
for port in ports:
    print(f"\n🔍 Testing port {port}...")
    try:
        if port == 465:
            server = smtplib.SMTP_SSL('smtp.gmail.com', port, timeout=10)
        else:
            server = smtplib.SMTP('smtp.gmail.com', port, timeout=10)
            server.starttls()
        
        server.login(email, password)
        print(f"✅ SUCCESS on port {port}!")
        server.quit()
    except Exception as e:
        print(f"❌ Failed on port {port}: {type(e).__name__} - {e}")

print("\n" + "=" * 60)