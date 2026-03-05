import os
from flask import Flask, render_template  # ✅ render_template import karna mat bhoolna
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv

load_dotenv()

# ✅ Yahan par objects banao
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinic.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['WTF_CSRF_ENABLED'] = True
    
    # ✅ Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # ✅ Models import karo
    from models.models import Doctor
    
    # Import and register blueprints
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
    
    # ✅ ERROR HANDLERS - YAHAN ADD KARO (function ke ANDAR)
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('page_not_found.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()  # ✅ db yahan available hai
        return render_template('server_error.html'), 500
    
    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)