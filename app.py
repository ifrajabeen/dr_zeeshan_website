import os
from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_mail import Mail

load_dotenv()

# ✅ Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()  # ✅ Mail object yahan bhi initialize karo

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME', 'your-email@gmail.com')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD', 'your-app-password')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER', 'your-email@gmail.com')
    
    # ✅ Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)  # ✅ Mail ko bhi initialize karo
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # ✅ IMPORTANT: Context Processor - Add this BEFORE registering blueprints
    @app.context_processor
    def inject_global_data():
        """Make settings and other global data available to all templates"""
        # Import models inside the function to avoid circular imports
        from models.models import Setting, Service, Doctor
        
        # Get or create doctor first
        doctor = Doctor.get_doctor()
        
        # Get all settings as dictionary
        settings = Setting.get_all_dict()
        
        # Get active services ordered by display order
        services = Service.query.filter_by(is_active=True).order_by(Service.order).all()
        
        return dict(
            settings=settings,
            services=services,
            doctor=doctor,
            current_year=datetime.utcnow().year
        )
    
    # ✅ Register blueprints
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
    
    # ✅ Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('page_not_found.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('server_error.html'), 500
    
    return app

# ✅ Create app instance
app = create_app()

# ✅ Mail object ko globally accessible banane ke liye
mail = app.extensions['mail']  # ✅ Better way to access mail

if __name__ == '__main__':
    app.run(debug=True)