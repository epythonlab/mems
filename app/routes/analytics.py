# app.py (or your main Flask app file)
from flask import render_template, jsonify, request
from sqlalchemy import func, extract
from datetime import datetime, timedelta, timezone

from app import db
from app.models.userlog import UserLog
from . import analytic_bp

# Assuming UserLog and User models are defined as previously discussed

@analytic_bp.route('/api/user-activity')
def user_activity_data():
    # Dynamic filtering based on date range
    start_date = request.args.get('start_date', ( datetime.now(tz=timezone.utc) - timedelta(days=7)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date',  datetime.now(tz=timezone.utc).strftime('%Y-%m-%d'))

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


@analytic_bp.route('/api/browser-usage')
def browser_usage_data():
    data = db.session.query(
        UserLog.browser_type,
        func.count(UserLog.id).label('count')
    ).group_by(UserLog.browser_type).all()

    labels = [d.browser_type for d in data]
    values = [d.count for d in data]

    return jsonify({
        'labels': labels,
        'values': values
    })


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

@analytic_bp.route('/api/active_users_daily')
def active_users_daily():
    active_users_daily = db.session.query(
        func.date(UserLog.timestamp).label('date'),
        func.count(func.distinct(UserLog.user_id)).label('active_users')
    ).group_by(func.date(UserLog.timestamp)).order_by(func.date(UserLog.timestamp)).all()

    results = {"dates": [str(record.date) for record in active_users_daily],
               "active_users": [record.active_users for record in active_users_daily]}

    return jsonify(results)

@analytic_bp.route('/api/user_retention')
def user_retention():
    retention_data = []
    for current_week in range(20, 24):  # Example weeks
        previous_week = current_week - 1

        current_week_users = db.session.query(
            UserLog.user_id
        ).filter(extract('week', UserLog.timestamp) == current_week).distinct().subquery()

        previous_week_users = db.session.query(
            UserLog.user_id
        ).filter(extract('week', UserLog.timestamp) == previous_week).distinct().subquery()

        retained_users_count = db.session.query(
            func.count(current_week_users.c.user_id)
        ).filter(current_week_users.c.user_id.in_(
            db.session.query(previous_week_users.c.user_id)
        )).scalar()

        previous_week_users_count = db.session.query(
            func.count(previous_week_users.c.user_id)
        ).scalar()

        if previous_week_users_count == 0:
            retention_rate = 0
        else:
            retention_rate = retained_users_count / previous_week_users_count

        retention_data.append({
            "current_week": current_week,
            "previous_week": previous_week,
            "retention_rate": retention_rate
        })

    return jsonify(retention_data)

# Route to render the analytics page
@analytic_bp.route('/analytics')
def analytics():
       
    return render_template('analytics/log_analytic.html')