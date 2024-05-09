from flask import render_template, request, redirect, url_for, flash
from flask_login.utils import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import user_bp
from app.models.users import User
from app.models.FileUpload import UploadFile


@user_bp.route('/users')
@login_required
def users():
    # Fetch users from the database
    users = User.query.all()
    
    return render_template('users/users.html', users = users)


