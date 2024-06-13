from flask import jsonify, request, render_template, redirect, url_for
from app import db
from app.models.orders import Customer, Order
from datetime import datetime
from . import orders_bp

@orders_bp.route('/new_order')
def new_order():
    return render_template('orders/new_order.html')

@orders_bp.route('/check_customer', methods=['POST'])
def check_customer():
    tin = request.form.get('tin')
    customer = Customer.query.filter_by(tin=tin).first()
    if customer:
        return redirect(url_for('orders_bp.create_order', customer_id=customer.id))
    else:
        return redirect(url_for('orders_bp.new_customer', tin=tin))

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

        return redirect(url_for('orders_bp.create_order', customer_id=new_customer))

    return render_template('orders/new_customer.html', tin=tin)


@orders_bp.route('/create_order', methods=['GET', 'POST'])
def create_order():
    if request.method == 'POST':
        tin = request.form['tin']
        customer = Customer.query.filter_by(tin=tin).first()

        if not customer:
            # If customer does not exist, redirect to new_customer form
            return redirect(url_for('orders.new_customer', tin=tin))

        # Create a new order
        # Example: Retrieve and process order items
        items = request.form.getlist('items')
        new_order = Order(customer_id=customer.id, order_date=datetime.now())

        for item in items:
            batch_id = item.get('batch_id')
            quantity = item.get('quantity')

            # Create OrderItem or handle as needed
            # Example: order_item = OrderItem(order_id=new_order.id, batch_id=batch_id, quantity=quantity)
            # db.session.add(order_item)

        db.session.add(new_order)
        db.session.commit()

        return redirect(url_for('orders.list_orders'))

    # Render the order creation form with customer information
    tin = request.args.get('tin', '')
    customer = Customer.query.filter_by(tin=tin).first()

    return render_template('orders/create_order.html', customer=customer)
