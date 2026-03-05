from app import app, db
from models.models import User

with app.app_context():
    # Check if admin already exists
    admin = User.query.filter_by(email='admin@drzeeshan.com').first()
    
    if not admin:
        admin = User(
            username='admin',
            email='admin@drzeeshan.com',
            first_name='Admin',
            last_name='User',
            role='admin'
        )
        admin.password = 'admin123'
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin account created successfully!")
        print("   Email: admin@drzeeshan.com")
        print("   Password: admin123")
    else:
        print("⚠️ Admin account already exists!")
        print("   Email: admin@drzeeshan.com")
        print("   Password: admin123")