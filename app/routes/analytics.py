# app.py (or your main Flask app file)
from flask import render_template, jsonify, request
from sqlalchemy import func, extract
from datetime import datetime, timedelta

from app import db
from app.models.userlog import UserLog
from . import analytic_bp

# Assuming UserLog and User models are defined as previously discussed

@analytic_bp.route('/api/user-activity')
def user_activity_data():
    # Dynamic filtering based on date range
    start_date = request.args.get('start_date', (datetime.utcnow() - timedelta(days=7)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.utcnow().strftime('%Y-%m-%d'))

    data = db.session.query(
        func.date(UserLog.timestamp).label('date'),
        func.count(UserLog.id).label('activity_count')
    ).filter(UserLog.timestamp >= start_date, UserLog.timestamp <= end_date).group_by(func.date(UserLog.timestamp)).all()

    labels = [str(d.date) for d in data]
    values = [d.activity_count for d in data]

    return jsonify({
        'labels': labels,
        'values': values
    })


@analytic_bp.route('/api/device-usage')
def device_usage_data():
    data = db.session.query(
        UserLog.device_type,
        func.count(UserLog.id).label('count')
    ).group_by(UserLog.device_type).all()

    labels = [d.device_type for d in data]
    values = [d.count for d in data]

    return jsonify({
        'labels': labels,
        'values': values
    })

@analytic_bp.route('/api/os-usage')
def os_usage_data():
    data = db.session.query(
        UserLog.device_os,
        func.count(UserLog.id).label('count')
    ).group_by(UserLog.device_os).all()

    labels = [d.device_os for d in data]
    values = [d.count for d in data]

    return jsonify({
        'labels': labels,
        'values': values
    })


@analytic_bp.route('/api/active-users')
def api_active_users():
    try:
        active_users_data = track_active_users()
        users = [{'date': str(daily.date), 'active_users': daily.active_users} for daily in active_users_data]
        return jsonify({'active_users_data': users})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def track_active_users():
    # Count unique active users per day
    active_users_daily = db.session.query(
        func.date(UserLog.timestamp).label('date'),
        func.count(func.distinct(UserLog.user_id)).label('active_users')
    ).group_by(func.date(UserLog.timestamp)).order_by(func.date(UserLog.timestamp)).all()

    return active_users_daily

@analytic_bp.route('/api/most-common-actions')
def api_most_common_actions():
    try:
        most_common_actions = determine_most_common_actions()
        actions = [{'action': action.action, 'count': action.action_count} for action in most_common_actions]
        return jsonify({'most_common_actions': actions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def determine_most_common_actions():
    # Count each action type
    most_common_actions = db.session.query(
        UserLog.action,
        func.count(UserLog.id).label('action_count')
    ).group_by(UserLog.action).order_by(func.count(UserLog.id).desc()).all()
    
    return most_common_actions

@analytic_bp.route('/api/action_summary')
def api_action_summary():
    top_n = 5  # Number of top actions to display
    action_summary = db.session.query(
        UserLog.action,
        func.count(UserLog.id).label('action_count')
    ).group_by(UserLog.action).order_by(func.count(UserLog.id).desc()).limit(top_n).all()

    results = {"labels": [action.action for action in action_summary],
               "values": [action.action_count for action in action_summary]}

    return jsonify(results)

# Route to render the analytics page
@analytic_bp.route('/analytics')
def analytics():
       
       
    return render_template('analytics/log_analytic.html')