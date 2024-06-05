from flask import request, render_template, url_for, redirect, flash, jsonify
from flask_security import login_required
from app.models.inventory import Product, Batch, Category
from . import inventory_bp
from datetime import datetime
from app import db

@inventory_bp.route('/inventory')
@login_required
def inventory_list():
    # Get the selected number of rows per page from the dropdown menus
    prod_rows_per_page = int(request.args.get('prod_rows_per_page', 5))  # Default to 5 rows per page for products
    cat_rows_per_page = int(request.args.get('cat_rows_per_page', 5))    # Default to 5 rows per page for categories
    
    # Get the current page number from the query parameters for both tables
    prod_page = request.args.get('prod_page', 1, type=int)
    cat_page = request.args.get('cat_page', 1, type=int)
    
    # Paginate products and categories separately
    products = Product.query.order_by(Product.stock.desc()).paginate(page=prod_page, per_page=prod_rows_per_page, error_out=False)
    categories = Category.query.order_by(Category.id.desc()).paginate(page=cat_page, per_page=cat_rows_per_page, error_out=False)
    
    # Render the template with products and categories
    return render_template('inventory/inventory.html', products=products, categories=categories, prod_rows_per_page=prod_rows_per_page, cat_rows_per_page=cat_rows_per_page, prod_page=prod_page, cat_page=cat_page)
@inventory_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        vendor = request.form['vendor']

        product = Product(name=name, category_id=category_id, vendor=vendor)
        db.session.add(product)
        db.session.commit()

        return redirect(url_for('inventory_bp.inventory_list'))
    
    categories = Category.query.all()
    return render_template('inventory/add_product.html', categories=categories)

@inventory_bp.route('/manage_batch/<int:product_id>', methods=['GET', 'POST'])
@login_required
def manage_batch(product_id):
    
    product = Product.query.get_or_404(product_id)

    if request.method == 'POST':
        batch_number = request.form['batchNumber']
        expiration_date = request.form['expirationDate']
        quantity = request.form['quantity']

        # Check if batch already exists for the product
        existing_batch = Batch.query.filter_by(product_id=product_id, batch_number=batch_number).first()

        # Check if the batch number is already associated with another product
        batch_associated_with_another_product = Batch.query.filter_by(batch_number=batch_number).filter(Batch.product_id != product_id).first()

        if batch_associated_with_another_product:
            flash(f'Batch number "{batch_number}" is already associated with another product', 'danger')
            return redirect(url_for("inventory_bp.inventory_list"))

        if existing_batch:
            # Update existing batch
            existing_batch.expiration_date = expiration_date
            existing_batch.quantity = quantity
            existing_batch.updated_at = datetime.utcnow()
            flash_msg = f'Batch updated successfully to {product.name}'
        else:
            # Add new batch
            new_batch = Batch(batch_number=batch_number, 
                              expiration_date=expiration_date, 
                              quantity=quantity, 
                              product_id=product_id,
                              created_at = datetime.utcnow())
            db.session.add(new_batch)
            flash_msg = f'Batch added successfully to {product.name}'
            
        # update stock level of the product based on batch and quantity
        product.update_stock()
        db.session.commit()
        flash(flash_msg, 'success')
        
    return redirect(url_for("inventory_bp.inventory_list"))

@inventory_bp.route('/manage_batches/<product_id>', methods=['GET', 'POST'])
@login_required
def manage_batches(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        # Logic to manage batches (e.g., update batch details)
        return redirect(url_for('inventory_bp.manage_batches', product_id=product_id))
    return render_template('inventory/manage_batches.html', product=product)

@inventory_bp.route('/add_category', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        category_names = request.form.getlist('name[]')
        for name in category_names:
            if name:  # Ensure the name is not empty
                category = Category(name=name)
                db.session.add(category)
        db.session.commit()
        flash("Categories added successfully.", 'success')
        return redirect(url_for('inventory_bp.inventory_list'))
    
    return render_template('inventory/add_category.html')

@inventory_bp.route('/update_product/<int:product_id>', methods=['POST'])
@login_required
def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    product.name = request.form['name']
    product.category_id = request.form['category_id']
    product.vendor = request.form['vendor']

    # You can add more fields to update if needed

    try:
        db.session.commit()
        flash('Product updated successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating product: {str(e)}', 'danger')

    return redirect(url_for('inventory_bp.inventory_list'))

@inventory_bp.route('/update_category/<int:category_id>', methods=['POST'])
@login_required
def update_category(category_id):
    data = request.get_json()
    new_name = data.get('name')
    
    if not new_name:
        return jsonify(success=False, message="Name cannot be empty"), 400
    
    category = Category.query.get_or_404(category_id)
    category.name = new_name
    db.session.commit()
    
    return jsonify(success=True)

@inventory_bp.route('/deleteProduct/<int:item_id>', methods=['POST'])
@login_required
def delete_inventory_item(item_id):
    try:
        item = Product.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        flash('Item deleted successfully!', 'success')
    except Exception as e:
        flash('Failed to delete item: ' + str(e), 'error')
    return redirect(url_for('inventory_bp.inventory_list'))

@inventory_bp.route('/add_modal')
@login_required
def add_modal():
    return render_template('inventory/add_product.html')

@inventory_bp.route('/edit_product/<product_id>')
@login_required
def edit_product(product_id):
    categories = Category.query.all()
    product = Product.query.get_or_404(product_id)
    return render_template('inventory/edit_product.html', product=product, categories = categories)
