# app/routes/role_routes.py
from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required
from flask_security import roles_required
from app.models.users import User, Role
from app import db
from . import role_bp

@role_bp.route('/roles')
@login_required
@roles_required('admin')
def list_roles():
    roles = Role.query.all()
    return render_template('users/roles.html', roles=roles)

@role_bp.route('/add_role', methods=['POST'])
@login_required
@roles_required('admin')
def add_role():
    role_name = request.form.get('role_name')
    description = request.form.get('description')

    if Role.query.filter_by(name=role_name).first():
        flash('Role already exists', 'error')
    else:
        new_role = Role(name=role_name, description=description)
        db.session.add(new_role)
        db.session.commit()
        flash('Role added successfully', 'success')

    return redirect(url_for('role_bp.list_roles'))

@role_bp.route('/delete_role/<int:role_id>', methods=['POST'])
@login_required
@roles_required('admin')
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        db.session.delete(role)
        db.session.commit()
        flash('Role deleted successfully', 'success')
    else:
        flash('Role not found', 'error')

    return redirect(url_for('role_bp.list_roles'))

@role_bp.route('/modify_role', methods=['POST'])
@login_required
@roles_required('admin')
def modify_role():
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
@roles_required('admin')
def assign_role():
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
@roles_required('admin')
def remove_role():
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
