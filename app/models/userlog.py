from datetime import datetime
from app import db

class UserLog(db.Model):
    __tablename__ = 'user_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(100), index=True, nullable=False)
    user_ip = db.Column(db.String(200), nullable=False)
    device_type = db.Column(db.String(100), nullable=False)
    device_os = db.Column(db.String(100), nullable=False)
    action = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, user_id, user_ip, device_type, device_os, action):
        self.user_id = user_id
        self.user_ip = user_ip
        self.device_type = device_type
        self.device_os = device_os
        self.action = action

    def __repr__(self):
        return f"<UserLog {self.id} - {self.user_id} - {self.action} - {self.timestamp}>"
