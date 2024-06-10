# patch_flask_login.py
from werkzeug import parse_query_string

def patched_url_decode(*args, **kwargs):
    return parse_query_string(*args, **kwargs)

from flask_login.utils import url_decode
url_decode = patched_url_decode
