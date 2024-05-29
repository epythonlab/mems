from functools import wraps
from flask import request
from flask_login import current_user
from app import db
from app.models.userlog import UserLog
import user_agents

def get_device_type(user_agent_string):
    ua = user_agents.parse(user_agent_string)
    if ua.is_mobile:
        return 'Mobile'
    elif ua.is_tablet:
        return 'Tablet'
    elif ua.is_pc:
        return 'Desktop'
    else:
        return 'Other'

def get_device_os(user_agent_string):
    ua = user_agents.parse(user_agent_string)
    os_name = ua.os.family
    os_architecture = '64-bit' if 'x86_64' in user_agent_string or 'Win64' in user_agent_string else '32-bit'
    return f"{os_name} {os_architecture}"

def log_user_activity(action, action_type, description, additional_data=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            response = f(*args, **kwargs)  # Call the actual route function
            if current_user.is_authenticated:
                log_action(current_user.id, action, action_type, description, additional_data)
            return response
        return decorated_function
    return decorator

def log_action(user_id, action, action_type, description, additional_data=None):
    user_ip = request.remote_addr
    device_type = get_device_type(request.user_agent.string)
    device_os = get_device_os(request.user_agent.string)
    
    user_log = UserLog(
        user_id=user_id,
        user_ip=user_ip,
        device_type=device_type,
        device_os=device_os,
        action=action,
        action_type=action_type,
        description=description,
        additional_data=additional_data
    )
    
    db.session.add(user_log)
    db.session.commit()
