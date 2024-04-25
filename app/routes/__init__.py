from flask import Blueprint

index_bp = Blueprint('index_bp', __name__)
# Create the auth blueprint
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)

from . import index
from . import auth


