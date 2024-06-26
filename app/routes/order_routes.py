from flask import jsonify, request, render_template, redirect, url_for
from flask_login import login_required
from app import db
from app.models.orders import Customer, Order, OrderItem
from app.models.inventory import Product, Batch
from datetime import datetime
from . import orders_bp
from sqlalchemy import and_


@orders_bp.route('/new_order')
@login_required
def new_order():
    return render_template('orders/new_order.html')

@orders_bp.route('/check_customer', methods=['POST'])
@login_required
def check_customer():
    tin = request.form.get('tin')
    customer = Customer.query.filter_by(tin=tin).first()
    if customer:
        return redirect(url_for('orders_bp.create_order', tin=tin))
    else:
        return redirect(url_for('orders_bp.new_customer', tin=tin))

@orders_bp.route('/get_products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.all()
    product_list = [{'id': product.id, 'name': product.name} for product in products if product.stock > 1]
    return jsonify(product_list)

@orders_bp.route('/get_batches/<int:product_id>', methods=['GET'])
@login_required
def get_batches(product_id):
    batches = Batch.query.filter(
        and_(
            Batch.product_id == product_id,
            Batch.months_left >= 1,
            Batch.quantity > 0
        )
    ).all()
    batches_list = [{'id': batch.id, 'expiry_date': batch.months_left, 'quantity': batch.quantity} for batch in batches]
    return jsonify(batches_list)

@orders_bp.route('/new_customer/<tin>', methods=['GET', 'POST'])
@login_required
def new_customer(tin):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        new_customer = Customer(name=name, email=email, phone=phone, address=address, tin=tin)
        db.session.add(new_customer)
        db.session.commit()

        return redirect(url_for('orders_bp.create_order', tin=new_customer.tin))

    return render_template('orders/new_customer.html', tin=tin)


@orders_bp.route('/create_order', methods=['GET', 'POST'])
@login_required
def create_order():
    customer = None

    if request.method == 'POST':
        tin = request.form.get('tin')
        if not tin:
            return jsonify({'error': 'TIN is required'}), 400

        customer = Customer.query.filter_by(tin=tin).first()
        if not customer:
            return jsonify({'error': 'Customer not found', 'redirect': url_for('orders_bp.new_customer', tin=tin)}), 404

        try:
            new_order = Order(customer_id=customer.id, order_date=datetime.now())
            db.session.add(new_order)
            db.session.flush()  # Ensure new_order.id is available

            items = request.form.to_dict(flat=False)
            item_count = len([key for key in items.keys() if key.startswith('items[') and key.endswith('][batch_id]')])

            with db.session.no_autoflush:  # Prevent autoflush to avoid IntegrityError
                for index in range(item_count):
                    batch_id = items.get(f'items[{index}][batch_id]')[0]
                    quantity = items.get(f'items[{index}][quantity]')[0]
                    
                    if batch_id and quantity:
                        batch = Batch.query.get(batch_id)
                        if not batch:
                            raise ValueError(f"Batch with ID {batch_id} not found")
                        
                        if batch.quantity <= 0:
                            raise ValueError(f"Batch with ID {batch_id} has zero quantity")
                        
                        if batch.quantity < int(quantity):
                            raise ValueError(f"Batch with ID {batch_id} has insufficient quantity")
                        
                        order_item = OrderItem(order_id=new_order.id, batch_id=batch_id, quantity=int(quantity))
                        order_item.calculate_total_price()
                        order_item.update_batch_quantity()
                        
                        db.session.add(order_item)

            new_order.update_total_amount()  # Ensure the total amount is updated
            db.session.commit()

            return jsonify({'success': True, 'redirect': url_for('orders_bp.list_orders')})

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    tin = request.args.get('tin', '')
    if tin:
        customer = Customer.query.filter_by(tin=tin).first()

    return render_template('orders/create_order.html', customer=customer)

@orders_bp.route('/list_orders')
@login_required
def list_orders():
    orders = Order.query.all()
    return render_template('orders/list_orders.html', orders=orders)
