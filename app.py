import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv(override=True)

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Email configuration
    mail_server = os.getenv('MAIL_SERVER', 'smtp.gmail.com').strip()
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_use_tls = os.getenv('MAIL_USE_TLS', 'True').strip().lower() == 'true'
    mail_default_sender = os.getenv('MAIL_DEFAULT_SENDER', 'your-email@gmail.com').strip()
    mail_username = os.getenv('MAIL_USERNAME', '').strip()
    mail_password = os.getenv('MAIL_PASSWORD', '').strip()

    # Common placeholder usernames break SMTP login; fallback to sender email.
    placeholder_usernames = {'', 'your-email@gmail.com', 'aapka_brevo_email@example.com'}
    if mail_username in placeholder_usernames:
        mail_username = mail_default_sender

    app.config['MAIL_SERVER'] = mail_server
    app.config['MAIL_PORT'] = mail_port
    app.config['MAIL_USE_TLS'] = mail_use_tls
    app.config['MAIL_USERNAME'] = mail_username
    app.config['MAIL_PASSWORD'] = mail_password
    app.config['MAIL_DEFAULT_SENDER'] = mail_default_sender
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # ✅ CONTEXT PROCESSOR - Proper indentation
    @app.context_processor
    def inject_global_data():
        """Make data available to all templates"""
        # Import inside function to avoid circular imports
        from models.models import Doctor, Service, Setting
        
        # Get or create doctor - with app context
        with app.app_context():
            doctor = Doctor.get_doctor()
            services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
            settings = Setting.get_all_dict()
        
        # Settings dictionary
        settings = {
            'clinic_name': 'Dr. Zeeshan Ahmed',
            'footer_description': 'Providing compassionate, professional mental health care to help you achieve emotional wellness and balance.',
            'facebook_url': '#',
            'twitter_url': '#',
            'instagram_url': '#',
            'linkedin_url': '#',
            'clinic_phone': '+1 (555) 123-4567',
            'clinic_email': 'contact@drzeeshan.com',
            'clinic_address': '123 Wellness Street, Medical District'
        }
        
        # Services list
        services = [
            {'name': 'Individual Therapy', 'url': '#'},
            {'name': 'Couples Counseling', 'url': '#'},
            {'name': 'Anxiety Treatment', 'url': '#'},
            {'name': 'Depression Therapy', 'url': '#'},
            {'name': 'Stress Management', 'url': '#'},
        ]
        
        return dict(
            doctor=doctor,
            settings=settings,
            services=services,
            current_year=datetime.utcnow().year
        )
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.appointments import appointments_bp
    from routes.reviews import reviews_bp
    from routes.admin import admin_bp
    from routes.faq import faq_bp
    app.register_blueprint(faq_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(appointments_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(admin_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('page_not_found.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('server_error.html'), 500
    
    return app


# Create app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

