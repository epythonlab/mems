from flask import render_template, jsonify, redirect, url_for, flash
from flask_login.utils import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from . import index_bp
from app.models.orders import Order, Batch, OrderItem, Customer
from app.models.FileUpload import UploadFile

from app import db
from datetime import datetime, timedelta, timezone

@index_bp.route('/')
@login_required
def index():
    return render_template('index.html')

@index_bp.route('/order_analysis')
def get_order_analysis():
    try:
        # Assuming you have a way to get the current user's information
        # current_user = get_current_user()
        company_id = current_user.company_id
        # Define the base query for orders
        if current_user.has_role('user'):
            orders_query = Order.query.join(Customer).filter(Customer.company_id == company_id)
        else:
            orders_query = Order.query

        # Total Number of Orders
        total_orders = orders_query.count()

        # Calculate Total Revenue
        total_revenue = db.session.query(func.sum(Order.total_amount)).join(Customer)
        if current_user.has_role('user'):
            total_revenue = total_revenue.filter(Customer.company_id == company_id)
        total_revenue = total_revenue.scalar() or 0

        # Calculate Average Order Value (AOV)
        aov = total_revenue / total_orders if total_orders else 0

        # Orders by day for the past week
        last_week = datetime.now(tz=timezone.utc) - timedelta(weeks=1)
        daily_orders = db.session.query(
            func.date(Order.order_date),
            func.count(Order.id),
            func.sum(Order.total_amount)
        ).join(Customer).filter(
            Order.order_date >= last_week
        )
        if current_user.has_role('user'):
            daily_orders = daily_orders.filter(Customer.company_id == company_id)
        daily_orders = daily_orders.group_by(
            func.date(Order.order_date)
        ).all()
        daily_orders = [{'date': date.strftime('%Y-%m-%d'), 'count': count, 'revenue': revenue} for date, count, revenue in daily_orders]

        # Orders by month for the past year
        last_year = datetime.now(tz=timezone.utc) - timedelta(weeks=52)
        monthly_orders = db.session.query(
            func.date_format(Order.order_date, '%Y-%m'),
            func.count(Order.id),
            func.sum(Order.total_amount)
        ).join(Customer).filter(
            Order.order_date >= last_year
        )
        if current_user.has_role('user'):
            monthly_orders = monthly_orders.filter(Customer.company_id == company_id)
        monthly_orders = monthly_orders.group_by(
            func.date_format(Order.order_date, '%Y-%m')
        ).all()
        monthly_orders = [{'month': month, 'count': count, 'revenue': revenue} for month, count, revenue in monthly_orders]

        # Orders by year
        yearly_orders = db.session.query(
            func.date_format(Order.order_date, '%Y'),
            func.count(Order.id),
            func.sum(Order.total_amount)
        ).join(Customer)
        if current_user.has_role('user'):
            yearly_orders = yearly_orders.filter(Customer.company_id == company_id)
        yearly_orders = yearly_orders.group_by(
            func.date_format(Order.order_date, '%Y')
        ).all()
        yearly_orders = [{'year': year, 'count': count, 'revenue': revenue} for year, count, revenue in yearly_orders]

        # New vs. Returning Customers
        new_customers_query = db.session.query(Order.customer_id).join(Customer)
        if current_user.has_role('user'):
            new_customers_query = new_customers_query.filter(Customer.company_id == company_id)
        new_customers = new_customers_query.distinct(Order.customer_id).count()

        returning_customers = total_orders - new_customers
        new_customer_percentage = (new_customers / total_orders) * 100 if total_orders else 0
        returning_customer_percentage = 100 - new_customer_percentage

        # Customer Lifetime Value (CLV)
        total_customers_query = Customer.query
        if current_user.has_role('user'):
            total_customers_query = total_customers_query.filter(Customer.company_id == company_id)
        total_customers = total_customers_query.count()

        clv = total_revenue / total_customers if total_customers else 0

        # Create a dictionary with the fetched statistics
        order_analysis = {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "aov": aov,
            "daily_orders": daily_orders,
            "monthly_orders": monthly_orders,
            "yearly_orders": yearly_orders,
            "new_customer_percentage": new_customer_percentage,
            "returning_customer_percentage": returning_customer_percentage,
            "clv": clv
        }

        # Return the statistics as JSON
        return jsonify(order_analysis)

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

        
    # return render_template('anayltics/order_analysis.html', total_orders=total_orders, daily_orders=daily_orders, monthly_orders=monthly_orders, yearly_orders=yearly_orders)

@index_bp.route('/view_error_log')
@login_required
def view_error_log():
     # Define the absolute path to the error.log file
    error_log_path = 'error.log'  # Update with the actual absolute path to your error.log file
    
    # Read the contents of the error.log file
    with open(error_log_path, 'r') as file:
        error_log_contents = file.read()
    
    # Pass the contents to the template for rendering
    return render_template('error_log.html', error_log_contents=error_log_contents)


