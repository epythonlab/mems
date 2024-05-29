# Import necessary modules and classes
from flask import g, render_template, request, flash, redirect, url_for, jsonify
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.users import User, Role # Make sure to import your User model
from app.models.FileUpload import UploadFile
from app import db, login_manager
from app.log_user import log_user_activity, log_action
from . import auth_bp
from app.utils import generate_random_password
import uuid
# route to login
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    uname = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=uname).first()
    if not user or not check_password_hash(user.password, password):
        flash("Invalid email or password", "danger")
        return redirect(url_for('auth_bp.login'))
    
    if not user.roles:
        flash("Your account is not activated", "danger")
        return redirect(url_for('auth_bp.login'))
    
    login_user(user)
    log_action(user.id, 'User logged in', 'login', 'User logged in successfully')
    return redirect(url_for('index_bp.index'))

# Handle unauthorized_handdler
# Protect unauthorized access
@login_manager.unauthorized_handler
def unauthorized_callback():
    if current_user.is_authenticated:
        log_action(current_user.id, 'Unauthorized access attempt', 'unauthorized_access', 'User tried to access a protected route without sufficient permissions')
    return render_template('unauthorized.html'), 403

#  Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

# register new user
@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # Extract form data
        form_data = request.form
        email = form_data.get('email')

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            flash("Email already exists. Please use a different email.", "danger")
            return redirect(url_for('auth_bp.register'))

        # Generate random password
        password = generate_random_password()
        hashed_password = generate_password_hash(password, method='scrypt')

        # Process file uploads
        logo = UploadFile.save_picture(request.files.get('logo'))
        license = UploadFile.save_picture(request.files.get('license'))

        # Create new user object
        new_user = User(
            first_name=form_data.get('fname'),
            last_name=form_data.get('lname'),
            phone_number=form_data.get('phone'),
            email=email,
            password=hashed_password,
            country=form_data.get('country'),
            state=form_data.get('state'),
            sub_city=form_data.get('sub_city'),
            wereda=form_data.get('wereda'),
            kebele=form_data.get('kebele'),
            house_number=form_data.get('house_no'),
            company_name=form_data.get('company_name'),
            logo=logo,
            license=license,
            fs_uniquifier=str(uuid.uuid4()),  # Use str() to convert UUID to string
            active=0  # Assuming 0 represents inactive users
        )

        # Add user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('You are registered successfully.', 'success')
        return redirect(url_for('auth_bp.login'))

    return render_template('registration.html')
    
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
    log_action(current_user.id, 'User logged out', 'logout', 'User logged out successfully')
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200



"""Change an existing user's password."""
@auth_bp.route('/change_password')
@login_required
def change_password():
    # route to update the password
    return render_template('users/change_password.html')

@auth_bp.route('/update_password', methods=['POST', 'GET'])
@login_required
def update_password():
    try:
        if request.method == 'POST':
            user = User.query.get(current_user.id)

            if not check_password_hash(user.password, request.form.get('oldpassword')):
                flash("The old password is incorrect.", 'warning')
                return redirect(url_for('auth_bp.change_password'))

            new_password = request.form['new_password']

            # Validate new password (e.g., length, complexity)
            if len(new_password) < 8:
                flash("The new password must be at least 8 characters long.", 'warning')
                return redirect(url_for('auth_bp.change_password'))

            # Log the password change action
            log_action(user.id, 'Password changed', 'password_change', 'User changed their password')

            # Update user's password
            user.password = generate_password_hash(new_password, method='scrypt')
            db.session.commit()

            flash('Password changed successfully. Please log in with your new password.', 'success')
            return redirect(url_for('auth_bp.login'))

    except Exception as e:
        # Handle exceptions gracefully
        flash("An error occurred while updating your password. Please try again later.", 'danger')
        print("Error updating password:", e)
        return redirect(url_for('auth_bp.change_password'))

        
