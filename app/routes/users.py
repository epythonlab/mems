from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login.utils import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import user_bp
from app.models.users import User
from app.models.FileUpload import UploadFile

# route to users bp
# Route to users bp
@user_bp.route('/users')
@login_required
def users():
    # Get the selected number of rows per page from the dropdown menu
    per_page = int(request.args.get('rows_per_page', 5))  # Default to 10 rows per page if not selected

    # Get the current page number from the query parameters
    page = request.args.get('page', 1, type=int)

    # Check if filtering parameters are present in the request
    filter_email = request.args.get('email')

    # Fetch users from the database
    if filter_email:
        users = User.query.filter(User.email.like(f'%{filter_email}%')).order_by(User.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    else:
        users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=per_page, error_out=False)

    return render_template('users/users.html', users=users, rows_per_page=per_page)

@user_bp.route('/user_detail', methods=['GET'])
def user_detail():
    row_id = request.args.get('id') # Retrieve the ID from the query parameter
    # Use the ID to fetch details from your database or any other source
    user = User.query.filter_by(id = row_id).first()
    return render_template('users/user_detail.html', user=user)

# get user stats
@user_bp.route('/stats')
def get_stats():
    # Query user data and count users based on status
    # Count users with status 1
    active_users = User.query.filter_by(active=1).count()
    # Count users with status 0
    inactive_users = User.query.filter_by(active=0).count()

    # Create a dictionary with the fetched statistics
    stats = {
        "total_users": active_users + inactive_users ,
        "active_users": active_users,
        "inactive_users": inactive_users
    }

    # Return the statistics as JSON
    return jsonify(stats)