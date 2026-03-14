import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

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
    
    # Email Configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('EMAIL_USER')
    app.config['MAIL_PASSWORD'] = os.getenv('EMAIL_PASS')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('EMAIL_USER')
    
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
        from models.models import Doctor
        
        # Get or create doctor - with app context
        with app.app_context():
            doctor = Doctor.get_doctor()
        
        # Settings dictionary
        settings = {
            'clinic_name': 'Dr. Zeeshan Ahmed',
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