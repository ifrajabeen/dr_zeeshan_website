from flask import Blueprint, render_template
from models.models import Doctor, Review, Service  # ✅ Sirf models import karo

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # ✅ get_doctor() use karo, get_or_create() nahi
    doctor = Doctor.get_doctor()
    services = Service.query.filter_by(is_active=True).order_by(Service.order).all()    
    recent_reviews = Review.query.filter_by(is_approved=True).order_by(Review.created_at.desc()).limit(3).all()
    
    return render_template('index.html', doctor=doctor, reviews=recent_reviews, services=services, title='Home')
     
@main_bp.route('/about')
def about():
    doctor = Doctor.get_doctor()
    
    # Specializations ko list mein convert karo
    if isinstance(doctor.specializations, str):
        specializations_list = [s.strip() for s in doctor.specializations.split(',')]
    else:
        specializations_list = doctor.specializations
    
    return render_template('about.html', doctor=doctor, specializations=specializations_list, title='About')

@main_bp.route('/faqs')
def faqs():
    from models.models import FAQ
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.order).all()
    return render_template('faqs.html', faqs=faqs, title='FAQs')