# Import necessary modules and classes
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.users import User, Role # Make sure to import your User model
from app.models.FileUpload import UploadFile
from flask_security import SQLAlchemyUserDatastore
from app import db, login_manager
from . import auth_bp
from app.utils import generate_random_password
# Initialize the SQLAlchemy data store and Flask-Security.
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# route to login
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        uname = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(email=uname).first()

        if not user:
            flash("Sorry! Incorrect email or password!", 'danger')
            return redirect(url_for('auth_bp.login'))
        elif not check_password_hash(user.password, password):
            flash("Sorry! Password is incorrect or Your account is disabled.", 'danger')
            return redirect(url_for('auth_bp.login'))

        login_user(user)  # Log in the user
        # Debugging messages
        print("User:", user)
        print("Logged in successfully!")

        # Redirect to the index page or any other desired page
        return redirect(url_for('index_bp.index'))


# Protect unauthorized access
@auth_bp.route('/unauthorized')
def unauthorized():
    flash("Login to access this page.")
    return redirect(url_for('auth_bp.login'))

# # Load user for Flask-Login

@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

# print(current_user.get_id())
@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Obtain the form values
        first_name = request.form['fname']
        last_name = request.form['lname']
        phone_number = request.form['phone']
        email = request.form['email']
        
        # Randomly generate password for new user and hash the password
        password = generate_random_password()
            
        password = generate_password_hash(password, method='scrypt')
        country = request.form['country']
        state = request.form['state']
        sub_city = request.form['sub_city']
        wereda = request.form['wereda']
        kebele = request.form['kebele']
        house_number = request.form['house_no']
        company_name = request.form['company_name']
        logo = UploadFile.save_picture(request.files['logo'])
        license = UploadFile.save_picture(request.files['license'])
        
        # Register the form values to the database table (user)
        import uuid
        new_user = User(first_name=first_name, last_name=last_name, phone_number=phone_number,
                        email=email, password=password, country=country, state=state,
                        sub_city=sub_city, wereda=wereda, kebele=kebele, house_number=house_number,
                        company_name=company_name, logo=logo, license=license,
                        fs_uniquifier=uuid.uuid4(), active=0)

        # # Assign role to new user
        # # Create roles if they don't exist
        # admin_role = Role.query.filter_by(name='owner').first()
        # if not admin_role:
        #     admin_role = Role(name='owner', description='Administrator')
        #     db.session.add(admin_role)
        #     db.session.commit()

        # # Retrieve the user object from the database using the email address
        # new_user = User.query.filter_by(email=email).first()

        # # Check if the user exists
        # if new_user:
        #     try:
        #         # Add the 'owner' role to the user
        #         user_datastore.add_role_to_user(new_user, 'owner')
        #         db.session.commit()  # Commit the changes to the database
        #     except Exception as e:
        #         print(f"An error occurred while adding role to user: {str(e)}")
        #         # Optionally, log the error or handle it in an appropriate way
        # else:
        #     print(f"User with email {email} does not exist.")

        # Add new user
        db.session.add(new_user)
        # Commit the changes
        db.session.commit()
        
        flash('You are registered successfully.', 'success')
        return redirect(url_for('auth_bp.login'))
    return render_template('login.html')  # Render the registration form for GET requests

    
# check email is already exist
@auth_bp.route('/check_email', methods=['GET'])
def check_email():
    email = request.args.get('email')
    user = User.query.filter_by(email=email).first()
    if user:
        # Email exists
        return jsonify({'exists': True})
    else:
        # Email does not exist
        return jsonify({'exists': False})
    

# # confirm email
# @auth_bp.route('/verify_email/<token>')
# def verify_email(token):
#     try:
#         # load token
#         email = s.loads(token, salt='email-confirmation', max_age=20)
#         return 'The token works'
#     except exc.SignatureExpired:
#         return 'Signature Expired!'
#     except exc.BadTimeSignature:
#         return 'Signature does not match!'


"""Logout- redirect to login page"""
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_bp.login'))

# """Handle unauthorized_handdler"""
# @login_manager.unauthorized_handler
# def unauthorized():
#     """Redirect unauthorized users to Login page."""
#     flash("Login to access this page.")
#     return redirect(url_for('auth_bp.login'))

"""Change an existing user's password."""

@auth_bp.route('/change_password')
@login_required
def change_password():
    
    # update the password
    return render_template('users/change_password.html')

@auth_bp.route('/update_password', methods=['POST', 'GET'])
@login_required
def update_password():
    try:
        if request.method == 'POST':
            # retreive the current user by id
            user = User.query.filter_by(id=current_user.id).first()
            
            # check that the old password is correct
            if not check_password_hash(user.password, request.form.get('oldpassword')):
                flash("Sorry! The old password is incorrect!", 'warning')
                return redirect(url_for('auth_bp.change_password'))
            else:
                user.password = generate_password_hash(request.form['new_password'], method='scrypt')
                # Create a new UserLog entry and store it in the database
                # user_log = UserLog(username=current_user.email, action='Password changed')
                # db.session.add(user_log)
                db.session.commit()
                flash('Password changed successfully.', 'success')
                return redirect(url_for('auth_bp.login'))

    except Exception as e:
        print(e)
        
