from flask import request, render_template, url_for, redirect, flash
from flask_security import login_required
from app.models.inventory import InventoryItem
from . import inventory_bp
from datetime import datetime
from app import db

@inventory_bp.route('/inventory')
@login_required
def inventory_list():
    inventory = InventoryItem.query.all()
    return render_template('inventory/inventory.html', inventory=inventory)

@inventory_bp.route('/addInventoryItem', methods=['GET', 'POST'])
@login_required
def add_inventory_item():
    if request.method == 'POST':
        try:
            new_item = InventoryItem(
                name=request.form['name'],
                quantity=int(request.form['quantity']),
                reorder_point=int(request.form['reorder_point']),
                expiry_date=datetime.strptime(request.form['expiry_date'], '%Y-%m-%d'),
                category=request.form['category'],
                manufacturer=request.form['manufacturer']
            )
            db.session.add(new_item)
            db.session.commit()
            flash('Item added successfully!', 'success')
            return redirect(url_for('inventory_bp.inventory_list'))
        except Exception as e:
            flash('Failed to add item: ' + str(e), 'error')
            return redirect(url_for('inventory_bp.add_inventory_item'))
    return render_template('inventory/add_item.html')

@inventory_bp.route('/updateInventoryItem', methods=['POST'])
@login_required
def update_inventory_item():
    if request.method == 'POST':
        try:
            item_id = request.form['item_id']
            item = InventoryItem.query.get_or_404(item_id)
            item.name = request.form['name']
            item.quantity = int(request.form['quantity'])
            item.reorder_point = int(request.form['reorder_point'])
            item.expiry_date = datetime.strptime(request.form['expiry_date'], '%Y-%m-%d')
            item.category = request.form['category']
            item.manufacturer = request.form['manufacturer']
            db.session.commit()
            flash('Item updated successfully!', 'success')
            return redirect(url_for('inventory_bp.inventory_list'))
        except Exception as e:
            flash('Failed to update item: ' + str(e), 'error')
            return redirect(url_for('inventory_bp.inventory_list'))

@inventory_bp.route('/deleteInventoryItem/<int:item_id>', methods=['POST'])
@login_required
def delete_inventory_item(item_id):
    try:
        item = InventoryItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except Exception as e:
        flash('Failed to delete item: ' + str(e), 'error')
    return redirect(url_for('inventory_bp.inventory_list'))

@inventory_bp.route('/add_modal')
@login_required
def add_modal():
    return render_template('inventory/add_item.html')

@inventory_bp.route('/edit_modal/<item_id>')
@login_required
def edit_modal(item_id):
    item = InventoryItem.query.get_or_404(item_id)
    return render_template('inventory/edit_item.html', item=item)