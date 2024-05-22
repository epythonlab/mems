# app/routes/role_routes.py
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user

from app.models.users import User, Role, roles_users


from app import db
from . import role_bp

@role_bp.route('/roles')
@login_required
def list_roles():
    roles = Role.query.all()
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

    users = User.query.filter(~User.id.in_(subquery))
        
    is_permitted = any(role.name in ['admin', 'root'] for role in current_user.roles)
    return render_template('users/roles.html', roles=roles, users=users, is_permitted=is_permitted)

@role_bp.route('/add_role', methods=['POST'])
@login_required
def add_role():
    if not any(role.name == 'root' for role in current_user.roles):
        flash('You do not have permission to add roles.', 'danger')
        return redirect(url_for('role_bp.list_roles'))
    
    role_name = request.form.get('role_name')
    description = request.form.get('description')
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        new_role = Role(name=role_name, description=description)
        db.session.add(new_role)
        db.session.commit()
        flash('Role added successfully!', 'success')
    else:
        flash(f'Duplicate entry {role_name}.', 'danger')

    return redirect(url_for('role_bp.list_roles'))

@role_bp.route('/delete_role/<int:role_id>', methods=['POST'])
@login_required
def delete_role(role_id):
    if not any(role.name == 'root' for role in current_user.roles):
        flash('You do not have permission to delete roles.', 'danger')
        return redirect(url_for('role_bp.list_roles'))

    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        flash('Role deleted successfully!', 'success')
    else:
        flash('Role not found.', 'danger')

    return redirect(url_for('role_bp.list_roles'))

@role_bp.route('/modify_role', methods=['POST'])
@login_required
def modify_role():
    if not any(role.name == 'root' for role in current_user.roles):
        flash('You do not have permission to assign roles.', 'danger')
        return redirect(url_for('role_bp.list_roles'))
    
    role_id = request.form.get('role_id')
    new_name = request.form.get('new_name')
    new_description = request.form.get('new_description')

    role = Role.query.get(role_id)
    if role:
        role.name = new_name
        role.description = new_description
        db.session.commit()
        flash('Role modified successfully', 'success')
    else:
        flash('Role not found', 'error')

    return redirect(url_for('role_bp.list_roles'))

@role_bp.route('/assign_role', methods=['POST'])
@login_required
def assign_role():
    if not any(role.name in ['admin', 'root'] for role in current_user.roles):
        flash('You do not have permission to assign roles.', 'danger')
        return redirect(url_for('role_bp.list_roles'))
    
    user_id = request.form.get('user_id')
    role_name = request.form.get('role')

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('role_bp.list_roles'))

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        flash('Role not found', 'error')
        return redirect(url_for('role_bp.list_roles'))

    if role not in user.roles:
        user.roles.append(role)
        db.session.commit()
        flash('Role assigned successfully', 'success')
    else:
        flash('User already has this role', 'info')

    return redirect(url_for('role_bp.list_roles'))

@role_bp.route('/remove_role', methods=['POST'])
@login_required
def remove_role():
    if not any(role.name in ['root', 'admin'] for role in current_user.roles):
        flash('You do not have permission to remove roles.', 'danger')
        return redirect(url_for('role_bp.list_roles'))
    
    user_id = request.form.get('user_id')
    role_name = request.form.get('role')

    user = User.query.get(user_id)
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('role_bp.list_roles'))

    role = Role.query.filter_by(name=role_name).first()
    if not role:
        flash('Role not found', 'error')
        return redirect(url_for('role_bp.list_roles'))

    if role in user.roles:
        user.roles.remove(role)
        db.session.commit()
        flash('Role removed successfully', 'success')
    else:
        flash('User does not have this role', 'info')

    return redirect(url_for('role_bp.list_roles'))
