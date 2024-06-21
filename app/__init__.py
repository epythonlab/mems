import uuid  # Import uuid module

# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore
from sqlalchemy.exc import OperationalError, InvalidRequestError, NoForeignKeysError
import logging
from werkzeug.security import generate_password_hash
from flask_login import LoginManager

# Initialize SQLAlchemy
db = SQLAlchemy()
# Initialize LoginManager
login_manager = LoginManager()

def create_app(config_class=None):
    app = Flask(__name__)
    @app.template_filter('currency')
    def currency_filter(value):
        """Format a value as currency."""
        return f"${value:,.2f}"

    app.jinja_env.filters['currency'] = currency_filter
    
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_object("config.Config")

    # Initialize Plugins
    db.init_app(app)

    # Set up logging configuration
    logging.basicConfig(level=logging.ERROR, filename='error.log',
                        filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
    # Ensure that exceptions during logging are propagated
    logging.getLogger().propagate = True

    # init login_manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth_bp.login'
    login_manager.login_message = "Please enter valid email and password!"
    login_manager.login_message_category = "info"

    # Import blueprints
    from app.routes import index_bp
    from app.routes import auth_bp
    from app.routes import user_bp
    from app.routes import role_bp
    from app.routes import analytic_bp
    from app.routes import inventory_bp
    from app.routes import orders_bp
    # Register blueprints
    app.register_blueprint(index_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(role_bp)
    app.register_blueprint(analytic_bp)
    app.register_blueprint(inventory_bp)
    app.register_blueprint(orders_bp)
    
    # Create database tables within application context
    with app.app_context():
        from app.models.users import Role, User, Company
        try:
            # Create database tables
            db.create_all()

            # Create roles if they don't exist
            user_datastore = SQLAlchemyUserDatastore(db, User, Role)
            security = Security(app, user_datastore)
            root_role = Role.query.filter_by(name='root').first()
            if not root_role:
                root_role = Role(name='root', description='Super administrator')
                db.session.add(root_role)

            # Create a default admin user if no users exist
            if not User.query.filter(User.roles.contains(root_role)).first():
                company = Company(name='Medicine and Equipment Management Software')
                
                db.session.add(company) # update changes to company
                db.session.commit()  # Commit to persist the company and get the id
             
                default_admin = User(
                    email='root@superuser.com', password=generate_password_hash('root'), active=True, company_id=company.id)
                default_admin.roles.append(root_role)
                # Assign a unique identifier using a UUID
                default_admin.fs_uniquifier = str(uuid.uuid4())  # Convert UUID to string
                db.session.add(default_admin)

            db.session.commit()

        except (InvalidRequestError, NoForeignKeysError):
            # Handle database creation error
            app.logger.error("Failed to create database tables")
            raise
        except OperationalError as e:
            # Handle connection error
            error_msg = "Error connecting to MySQL server: %s" % str(e)
            print(error_msg)
            print("Make sure your MySQL server is running and the connection details are correct.")
            raise
    
    return app
