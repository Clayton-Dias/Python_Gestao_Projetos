from flask import abort
from flask_login import current_user
from functools import wraps

def permission_required(permissions):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if current_user.is_authenticated and current_user.permissao in permissions:
                return func(*args, **kwargs)
            abort(403)  # Proibido
        return wrapper
    return decorator
