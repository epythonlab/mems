from flask import render_template, request, redirect, url_for
from flask_login.utils import login_required, current_user
from . import index_bp
from app.models.users import User

@index_bp.route('/')
@login_required
def index():
    return render_template('index.html')

# @index_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username in users and users[username] == password:
#             # In a real application, you'd probably set a session variable here
#             return redirect(url_for('dashboard'))
#         else:
#             return render_template('login.html', message='Invalid username or password')
#     return render_template('login.html', message='')

@index_bp.route('/profile')
def profile():
    # In a real application, you'd probably use session variables to check if the user is logged in
    # retreive the current user profile based on the current login id
    user = User.query.filter_by(id=current_user.id).first()
    
    return render_template('users/profile.html', user = user)

@index_bp.route('/change_password')
def change_password():
    
    # retreive the current user profile based on the current login id
    user = User.query.filter_by(id=current_user.id).first()
    # update the password
    return render_template('users/change_password.html', user = user)