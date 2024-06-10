# tests/test_models.py

from app import db, create_app
from app.models.users import User, Company, Role
import uuid
# Set up the testing environment
def setup_module():
    app = create_app('config.TestConfig')
    app_context = app.app_context()
    app_context.push()
    db.create_all()

# Tear down the testing environment
def teardown_module():
    db.session.remove()
    db.drop_all()

# Test User model
def test_create_user():
    user = User(email='test@example.com', password='password', fs_uniquifier=str(uuid.uuid4()))
    db.session.add(user)
    db.session.commit()
    assert user.id is not None

def test_get_user_by_email():
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None

# Test Company model
def test_create_company():
    company = Company(name='Test Company')
    db.session.add(company)
    db.session.commit()
    assert company.id is not None

def test_get_company_by_name():
    company = Company.query.filter_by(name='Test Company').first()
    assert company is not None

# Test Role model
def test_create_role():
    role = Role(name='Admin', description='Administrator role')
    db.session.add(role)
    db.session.commit()
    assert role.id is not None

def test_get_role_by_name():
    role = Role.query.filter_by(name='Admin').first()
    assert role is not None
