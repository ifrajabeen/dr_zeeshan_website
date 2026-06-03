from app import app
from extensions import db

# ✅ IMPORTANT: import models so tables are registered
from models.models import *

# ✅ Create tables before app runs
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)