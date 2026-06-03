from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# Centralized extension instances to avoid circular imports.
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
mail = Mail()
