from flask import render_template, request, redirect, url_for, flash
from flask_login.utils import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import index_bp
from app.models.users import User
from app.models.FileUpload import UploadFile
from app import db
import os

@index_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@index_bp.route('/view_error_log')
@login_required
def view_error_log():
     # Define the absolute path to the error.log file
    error_log_path = 'error.log'  # Update with the actual absolute path to your error.log file
    
    # Read the contents of the error.log file
    with open(error_log_path, 'r') as file:
        error_log_contents = file.read()
    
    # Pass the contents to the template for rendering
    return render_template('error_log.html', error_log_contents=error_log_contents)

@index_bp.route('/profile')
def profile():
    # In a real application, you'd probably use session variables to check if the user is logged in
    # retreive the current user profile based on the current login id
    user = User.query.filter_by(id=current_user.id).first()
    
    return render_template('users/profile.html', user = user)
