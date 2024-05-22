from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login.utils import login_required, current_user
from flask_security import Security, SQLAlchemyUserDatastore, roles_required
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import or_
import uuid

from . import user_bp
from app import db
from app.models.users import User, Role, roles_users
from app.models.FileUpload import UploadFile
from app.utils import generate_random_password

# Route to users bp
@user_bp.route('/users')
@login_required
def users():
    
   # Check if the current user has either 'root' or 'admin' role
    if not any(role.name in ['root', 'admin'] for role in current_user.roles):
        flash('You do not have permission to manage users.', 'danger')
        return redirect(url_for('user_bp.users'))

    # Get the selected number of rows per page from the dropdown menu
    per_page = int(request.args.get('rows_per_page', 5))  # Default to 5 rows per page if not selected

    # Get the current page number from the query parameters
    page = request.args.get('page', 1, type=int)

    # Check if filtering parameters are present in the request
    filter_email = request.args.get('email')

    # Fetch 'admin' and 'root' role IDs
    admin_role = Role.query.filter_by(name='admin').first()
    root_role = Role.query.filter_by(name='root').first()

    # Base query excluding users with 'admin' or 'root' roles for 'admin' users and only 'root' roles for 'root' users
    if current_user.has_role('admin'):
        excluded_roles = [admin_role.id, root_role.id]
    else:
        excluded_roles = [root_role.id]

    subquery = db.session.query(roles_users.c.user_id).filter(
        roles_users.c.role_id.in_(excluded_roles)
    ).subquery()

    query = User.query.filter(~User.id.in_(subquery))

    # Filter users by email if filter_email is present
    if filter_email:
        query = query.filter(User.email.like(f'%{filter_email}%'))

    users = query.order_by(User.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
    roles = Role.query.all()

    return render_template('users/users.html', users=users, roles=roles, rows_per_page=per_page)

@user_bp.route('/user_detail', methods=['GET'])
def user_detail():
    if any(role.name in ['admin', 'root'] for role in current_user.roles):
        
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
    if any(role.name in ['admin', 'root'] for role in current_user.roles):
        
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
    if any(role.name in ['admin', 'root'] for role in current_user.roles):

        user_id = request.form.get('id')
        action = request.form.get('action')

        if not user_id or not action:
            flash('Invalid data', 'error')
            return redirect(url_for('user_bp.users'))  # Replace with the function that renders your view
        
        user = User.query.get(user_id)
        try:
            if action == 'approve':
                user.active = True
                password = generate_random_password()
                user.password = generate_password_hash(password, method='scrypt')
                message = "User status approved successfully. Please assing role to this user."
                print(password)
            elif action == 'disapprove':
                user.active = False
                message = "User status disapproved successfully. Please remove role of this user."
        
            db.session.commit()
            flash(message, 'success')
        except Exception as e:
            
            flash('Failed to update user status.', 'error')
            print(f"Error: {e}")
            
        return redirect(url_for('user_bp.users'))  # Replace with the function that renders your view
    else:
        flash('You are not authorized to access this page.', 'danger')
        redirect(url_for('auth_bp.login'))

@user_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        password = generate_password_hash(request.form['password'])
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        
        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            fs_uniquifier=uuid.uuid4(),
            active=0
        )
        db.session.add(new_user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('user_bp.users'))
    
    return render_template('users/users.html')
