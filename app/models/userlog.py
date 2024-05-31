from datetime import datetime
from app import db

class UserLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_ip = db.Column(db.String(200))
    device_type = db.Column(db.String(100))
    device_os = db.Column(db.String(100))
    browser_type = db.Column(db.String(100))
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Additional fields to capture more details
    action_type = db.Column(db.String(100))  # e.g., 'login', 'data_modification', 'error'
    description = db.Column(db.String(500))  # Description of the action
    additional_data = db.Column(db.JSON)  # Any additional data in JSON format

    # Relationship to the User model
    user = db.relationship('User', backref=db.backref('logs', lazy=True))

    def __init__(self, user_id, user_ip, device_type, device_os, browser_type, action, action_type, description, additional_data=None):
        self.user_id = user_id
        self.user_ip = user_ip
        self.device_type = device_type
        self.device_os = device_os
        self.browser_type = browser_type
        self.action = action
        self.action_type = action_type
        self.description = description
        self.additional_data = additional_data
        
    def __repr__(self):
        return f"<UserLog {self.id} - {self.user_id} - {self.action} - {self.timestamp}>"

# Example usage:
# user_log = UserLog(
#     user_id=current_user.id,
#     user_ip=request.remote_addr,
#     device_type=get_device_type(request.user_agent.string),
#     device_os=get_device_os(request.user_agent.string),
#     action='Logged in',
#     action_type='login',
#     description='User logged in successfully',
#     metadata={'additional_info': 'Any additional data'}
# )
# db.session.add(user_log)
# db.session.commit()


   
