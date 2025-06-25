import flask_restful as restful
from functools import wraps
from .Flask_app import app, app_logger

def role_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class Resource(restful.Resource):
    method_decorators = [role_decorator]
