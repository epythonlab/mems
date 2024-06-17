from flask import jsonify, request, render_template, redirect, url_for
from app import db
from app.models.orders import Customer, Order, OrderItem
from app.models.inventory import Product, Batch
from datetime import datetime
from . import orders_bp
from sqlalchemy import and_

@orders_bp.route('/new_order')
def new_order():
    return render_template('orders/new_order.html')

@orders_bp.route('/check_customer', methods=['POST'])
def check_customer():
    tin = request.form.get('tin')
    customer = Customer.query.filter_by(tin=tin).first()
    if customer:
        return redirect(url_for('orders_bp.create_order', tin=tin))
    else:
        return redirect(url_for('orders_bp.new_customer', tin=tin))

@orders_bp.route('/get_products', methods=['GET'])
def get_products():
    products = Product.query.all()
    product_list = [{'id': product.id, 'name': product.name} for product in products if product.stock > 1]
    return jsonify(product_list)

@orders_bp.route('/get_batches/<int:product_id>', methods=['GET'])
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
def create_order():
    if request.method == 'POST':
        tin = request.form.get('tin')
        if not tin:
            return "TIN is required", 400

        customer = Customer.query.filter_by(tin=tin).first()

        if not customer:
            return redirect(url_for('orders_bp.new_customer', tin=tin))

        new_order = Order(customer_id=customer.id, order_date=datetime.now())
        db.session.add(new_order)
        db.session.flush()  # Ensure new_order.id is available

        items = request.form.to_dict(flat=False)
        print("Form items:", items)
        # # Form items: {'tin': ['0043994288'], 'items[0][product]': ['6'], 'items[0][batch_id]': ['19'], 'items[0][quantity]': ['34'], 
        # 'items[1][product]': ['7'], 'items[1][batch_id]': ['25'], 'items[1][quantity]': ['45']}

       # Extract indices of the items dynamically
        item_count = len([key for key in items.keys() if key.startswith('items[') and key.endswith('][batch_id]')])
        print(item_count)
        for index in range(item_count):
            batch_id = items.get(f'items[{index}][batch_id]')[0]
            quantity = items.get(f'items[{index}][quantity]')[0]
            print(batch_id, quantity)
            
            if batch_id and quantity:
                order_item = OrderItem(order_id=new_order.id, batch_id=batch_id, quantity=quantity)
                db.session.add(order_item)

        db.session.commit()
        return redirect(url_for('orders_bp.list_orders'))

    tin = request.args.get('tin', '')
    customer = Customer.query.filter_by(tin=tin).first() if tin else None
    return render_template('orders/create_order.html', customer=customer)

@orders_bp.route('/list_orders')
def list_orders():
    orders = Order.query.all()
    return render_template('orders/list_orders.html', orders=orders)
