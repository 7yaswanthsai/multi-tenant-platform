from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    """Initialize database with Flask app"""
    # Apply engine options if they exist
    if hasattr(app.config, 'SQLALCHEMY_ENGINE_OPTIONS'):
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = app.config.SQLALCHEMY_ENGINE_OPTIONS
    
    db.init_app(app)
    
    with app.app_context():
        # Import all models to ensure they're registered with SQLAlchemy
        from app.models import admin, tenant, user, test
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create default admin if not exists
        create_default_admin()

def create_default_admin():
    """Create default admin user if not exists"""
    from app.models.admin import Admin
    from app.config import Config
    import bcrypt
    
    # Check if admin already exists
    existing_admin = Admin.query.filter_by(email=Config.ADMIN_EMAIL).first()
    
    if not existing_admin:
        # Hash the admin password
        hashed_password = bcrypt.hashpw(
            Config.ADMIN_PASSWORD.encode('utf-8'), 
            bcrypt.gensalt()
        ).decode('utf-8')
        
        # Create admin user
        admin = Admin(
            email=Config.ADMIN_EMAIL,
            password=hashed_password,
            name="System Administrator",
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        print(f"✅ Default admin created: {Config.ADMIN_EMAIL}")
    else:
        print(f"ℹ️  Admin already exists: {Config.ADMIN_EMAIL}")

