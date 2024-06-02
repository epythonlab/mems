from flask import Blueprint

index_bp = Blueprint('index_bp', __name__)
# Create the auth blueprint
auth_bp = Blueprint(
    'auth_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
user_bp = Blueprint(
    'user_bp', __name__,
    template_folder='templates',
    static_folder='static'
)
role_bp = Blueprint('role_bp', __name__)
analytic_bp = Blueprint('analytic_bp', __name__)

inventory_bp = Blueprint("inventory_bp", __name__)


from . import index
from . import auth
from . import users
from . import role_routes
from . import analytics
from . import inventory_routes


