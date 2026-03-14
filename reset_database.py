from app import app, db
from models.models import User, Doctor, Service

with app.app_context():
    # Sab tables create karo
    db.create_all()
    
    # Doctor banao
    doctor = Doctor(
        name='Dr. Zeeshan Ahmed',
        title='Clinical Psychologist',
        qualifications='Ph.D. in Clinical Psychology',
        experience='15+ years',
        biography='Dr. Zeeshan is a highly experienced clinical psychologist...',
        specializations='Anxiety Disorders, Depression, PTSD',
        email='dr.zeeshan@clinic.com',
        phone='+1 (555) 123-4567'
    )
    db.session.add(doctor)
    
    # Admin banao
    admin = User(
        username='admin',
        email='admin@drzeeshan.com',
        first_name='Admin',
        last_name='User',
        role='admin'
    )
    admin.password = 'admin123'
    db.session.add(admin)
    
    # Services add karo
    services = [
        Service(name='Individual Therapy', description='One-on-one therapy sessions', icon='fas fa-user', order=1, is_active=True),
        Service(name='Couples Counseling', description='Relationship counseling', icon='fas fa-heart', order=2, is_active=True),
        Service(name='Anxiety Treatment', description='Anxiety management', icon='fas fa-brain', order=3, is_active=True),
        Service(name='Depression Therapy', description='Depression treatment', icon='fas fa-cloud', order=4, is_active=True),
        Service(name='Stress Management', description='Stress reduction', icon='fas fa-leaf', order=5, is_active=True),
    ]
    
    for service in services:
        db.session.add(service)
    
    db.session.commit()
    
    print("✅ Database reset successfully!")
    print(f"   Doctor: {doctor.name}")
    print(f"   Admin: admin@drzeeshan.com / admin123")
    print(f"   Services: {Service.query.count()}")