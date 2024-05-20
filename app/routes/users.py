from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login.utils import login_required, current_user
from flask_security import Security, SQLAlchemyUserDatastore, roles_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_

from . import user_bp
from app import db
from app.models.users import User, Role
from app.models.FileUpload import UploadFile
from app.utils import generate_random_password

# Route to users bp
@user_bp.route('/users')
@login_required
@roles_required('admin')
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
    if current_user.has_role('admin'):
        
        row_id = request.args.get('id') # Retrieve the ID from the query parameter
        # Use the ID to fetch details from your database or any other source
        user = User.query.filter_by(id = row_id).first()
        return render_template('users/user_detail.html', user=user)
    else:
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('auth_bp.login'))


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


@user_bp.route('/search-suggestions')
def search_suggestions():
    if current_user.has_role('admin'):
        
        query = request.args.get('q', '').lower()
        if not query:
            return jsonify([])
        # Query User table
        users = User.query.filter(or_(
            User.first_name.ilike(f'%{query}%'),
            User.last_name.ilike(f'%{query}%'),
            User.email.ilike(f'%{query}%')
        )).all()
        
        results = []

        # Format the results
        for user in users:
            results.append({
                'name': f'{user.first_name} {user.last_name}',
                'description': user.email,
                'category': 'User'
            })
            
        return jsonify(results)
    else:
        
        flash('You are not authorized to access this page.', 'danger')
        return redirect(url_for('auth_bp.login'))

# update user status - approve or disapprove user
# assign user role if approved
# generate user password if approved
@user_bp.route('/update_user_status', methods=['POST'])
def update_user_status():
    if current_user.has_role('admin'):
        
        user_id = request.form.get('id')
        action = request.form.get('action')

        if not user_id or not action:
            print('Invalid data', 'error')
            return redirect(url_for('user_bp.users'))  # Replace with the function that renders your view
        
        user = User.query.get(user_id)
        try:
            if action == 'approve':
                user.active = True
                password = generate_random_password()
                user.password = generate_password_hash(password, method='scrypt')
                print(password)
            elif action == 'disapprove':
                user.active = False
        
            db.session.commit()
            flash('User status and role updated successfully', 'success')
        except Exception as e:
            
            flash('Failed to update user status and role', 'error')
            print(f"Error: {e}")
            
        return redirect(url_for('user_bp.users'))  # Replace with the function that renders your view
    else:
        flash('You are not authorized to access this page.', 'danger')

