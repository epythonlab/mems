# utils.py

import random
import string

def generate_random_password(length=12):
    # Define the characters to use for generating the password
    characters = string.ascii_letters + string.digits + string.punctuation
    
    # Generate the random password
    password = ''.join(random.choice(characters) for _ in range(length))
    
    return password
    
# Define the roles_required decorator
from functools import wraps
from flask import abort
from flask_login import current_user

def roles_required(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(403)
            if not any(role.name in roles for role in current_user.roles):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return wrapper