from flask import render_template, jsonify, redirect, url_for, flash
from flask_login.utils import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import func
from . import index_bp
from app.models.orders import Order, Batch, OrderItem
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
        # Total Number of Orders
        total_orders = Order.query.count()
        print(f"Total Orders: {total_orders}")

        # Calculate Total Revenue
        total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
        print(f"Total Revenue: {total_revenue}")

        # Calculate Average Order Value (AOV)
        aov = total_revenue / total_orders if total_orders else 0
        print(f"Average Order Value (AOV): {aov}")

        # Orders by day for the past week
        last_week = datetime.now(tz=timezone.utc) - timedelta(weeks=1)
        daily_orders = db.session.query(func.date(Order.order_date), func.count(Order.id), func.sum(Order.total_amount)) \
            .filter(Order.order_date >= last_week) \
            .group_by(func.date(Order.order_date)) \
            .all()
        daily_orders = [{'date': date.strftime('%Y-%m-%d'), 'count': count, 'revenue': revenue} for date, count, revenue in daily_orders]
        print(f"Daily Orders: {daily_orders}")

        # Orders by month for the past year
        last_year = datetime.now(tz=timezone.utc) - timedelta(weeks=52)
        monthly_orders = db.session.query(func.date_format(Order.order_date, '%Y-%m'), func.count(Order.id), func.sum(Order.total_amount)) \
            .filter(Order.order_date >= last_year) \
            .group_by(func.date_format(Order.order_date, '%Y-%m')) \
            .all()
        monthly_orders = [{'month': month, 'count': count, 'revenue': revenue} for month, count, revenue in monthly_orders]
        print(f"Monthly Orders: {monthly_orders}")

        # Orders by year
        yearly_orders = db.session.query(func.date_format(Order.order_date, '%Y'), func.count(Order.id), func.sum(Order.total_amount)) \
            .group_by(func.date_format(Order.order_date, '%Y')) \
            .all()
        yearly_orders = [{'year': year, 'count': count, 'revenue': revenue} for year, count, revenue in yearly_orders]
        print(f"Yearly Orders: {yearly_orders}")

        # Create a dictionary with the fetched statistics
        order_analysis = {
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "aov": aov,
            "daily_orders": daily_orders,
            "monthly_orders": monthly_orders,
            "yearly_orders": yearly_orders
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


