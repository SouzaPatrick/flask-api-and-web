from functools import wraps
from flask import abort
from flask import g
from app.models.tables import Permission

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if g.current_user != None:
                
                if not g.current_user.can(permission):
                    abort(403)
            else:
                    abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMIN)(f)
