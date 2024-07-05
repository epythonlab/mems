from flask import request, abort, render_template, session, url_for, redirect, flash, jsonify
from flask_security import login_required, current_user
from app.models.inventory import Product, Batch, Category
from . import inventory_bp
from datetime import datetime, date, timezone

from app import db

@inventory_bp.route('/inventory')
@login_required
def inventory_list():
    filter_type = request.args.get('filter')
    prod_page = request.args.get('prod_page', 1, type=int)
    prod_rows_per_page = request.args.get('prod_rows_per_page', 5, type=int)
    cat_page = request.args.get('cat_page', 1, type=int)
    cat_rows_per_page = request.args.get('cat_rows_per_page', 5, type=int)

    company_id = current_user.company_id

    products_query = Product.query.filter_by(company_id=company_id)
    categories = Category.query.paginate(page=cat_page, per_page=cat_rows_per_page, error_out=False)

    if filter_type == 'expired':
        products_query = products_query.join(Batch).filter(
            Batch.expiration_date < datetime.now(tz=timezone.utc),
            Batch.company_id == company_id
        )
        session['filter_criteria'] = filter_type

    elif filter_type == 'low_stock':
        session['filter_criteria'] = filter_type
        products_query = products_query.filter(Product.stock <= 50)

    if filter_type == request.args.get('clearfilter'):
        session['filter_criteria'] = None

    products = products_query.order_by(Product.stock.desc()).paginate(
        page=prod_page, per_page=prod_rows_per_page, error_out=False
    )

    return render_template(
        'inventory/inventory.html', 
        products=products, 
        categories=categories, 
        prod_rows_per_page=prod_rows_per_page, 
        cat_rows_per_page=cat_rows_per_page, 
        prod_page=prod_page, 
        cat_page=cat_page
    )



@inventory_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        category_id = request.form['category_id']
        vendor = request.form['vendor']

        product = Product(name=name, category_id=category_id, company_id = current_user.company_id, vendor=vendor)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
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
        unit_price = request.form['unit_price']
        # Check if batch already exists for the product
        existing_batch = Batch.query.filter_by(product_id=product_id, batch_number=batch_number, ).first()

        # Check if the batch number is already associated with another product
        batch_associated_with_another_product = (
            db.session.query(Batch)
            .join(Product, Batch.product_id == Product.id)
            .filter(
                Batch.batch_number == batch_number,
                Product.company_id == current_user.company_id,
                Batch.product_id != product_id
            )
            .first()
        )
        if batch_associated_with_another_product:
            flash(f'Batch number "{batch_number}" is already associated with another product', 'danger')
            return redirect(url_for("inventory_bp.inventory_list"))

        if existing_batch:
            # Update existing batch
            existing_batch.expiration_date = expiration_date
            existing_batch.quantity = quantity
            existing_batch.unit_price = float(unit_price)
            existing_batch.updated_at =  datetime.now(tz=timezone.utc)
            existing_batch.update_months_left() # update days left of the expiration date
            flash_msg = f'Batch updated successfully to {product.name}'
        else:
            # Add new batch
            new_batch = Batch(batch_number=batch_number, 
                              expiration_date=expiration_date, 
                              quantity=int(quantity),
                              unit_price = float(unit_price),
                              product_id=product_id,
                              created_at =  datetime.now(tz=timezone.utc))
            
            new_batch.update_months_left() # update days left of the expiration date
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

@inventory_bp.route('/product_details')
def product_details():
    id_or_batch = request.args.get('id')  # Retrieve the ID from the query parameter
    product = Product.query.get(id_or_batch)
 
    if not product:
        batch = Batch.query.filter_by(batch_number=id_or_batch.strip()).first()
        if batch:
            product = batch.product
            product.batches = [batch]  # Ensure batches is a list containing the single batch
        else:
            abort(404)  # If neither product nor batch is found, raise a 404 error
    else:
        # Retrieve the filter criteria from session
        filter_criteria = session.get('filter_criteria')

        # Filter the batches based on the expiration criteria and quantity
        if filter_criteria == 'expired':
            product.batches = [batch for batch in product.batches if batch.expiration_date < date.today() and batch.quantity > 0]
        else:
            product.batches = [batch for batch in product.batches if batch.expiration_date > date.today() and batch.quantity > 0]

    # Pass the product data and filtered batches to the template
    return render_template('inventory/product_details.html', product=product)



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

@inventory_bp.route('/edit_product/<product_id>')
@login_required
def edit_product(product_id):
    categories = Category.query.all()
    product = Product.query.get_or_404(product_id)
    return render_template('inventory/edit_product.html', product=product, categories = categories)


@inventory_bp.route('/inventory-search-suggestions')
@login_required
def inventory_search_suggestions():
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    suggestions = db.session.query(
        Product.id, Product.name.label('product'), Category.name.label('category'), Batch.batch_number.label('batch_no')  # Correctly label batch_number as 'batch_no'
    ).join(Category, Product.category_id == Category.id
    ).join(Batch, Product.id == Batch.product_id
    ).filter(
        db.or_(
            Product.name.ilike(f'%{query}%'),
            Category.name.ilike(f'%{query}%'),
            Batch.batch_number.ilike(f'%{query}%')
        )
    ).all()

    suggestion_list = [
        {"id": item.id, "product": item.product, "category": item.category, "batch_no": item.batch_no}  # Use the correct label for batch_number
        for item in suggestions
    ]
    return jsonify(suggestion_list)



@inventory_bp.route('/inventory-search-results')
@login_required
def inventory_search_results():
    batch_no = request.args.get('batch_no')
    if not batch_no:
        return jsonify([])

    products = Product.query.filter_by(batch_no=batch_no).all()

    results = []
    for product in products:
        results.append({
            'id': product.id,
            'product': product.name,
            'vendor': product.vendor,
            'category': product.category.name,
            'quantity': product.stock  # Assuming stock represents quantity
        })

    return jsonify(results)
