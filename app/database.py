from flask import current_app
from . import db
from app.models.users import User, Role
from werkzeug.security import generate_password_hash

def create_default_roles_and_users():
    with current_app.app_context():
        # Create roles if they don't exist
        admin_role = Role.query.filter_by(name='admin').first()
        if not admin_role:
            admin_role = Role(name='admin', description='Administrator')
            db.session.add(admin_role)

        # Create a default admin user if no users exist
        if not User.query.filter(User.roles.contains(admin_role)).first():
            default_admin = User(email='admin@admin.com', password=generate_password_hash('admin'), active=True)
            default_admin.roles.append(admin_role)
            import uuid
            default_admin.fs_uniquifier = uuid.uuid4()
            db.session.add(default_admin)

        db.session.commit()
