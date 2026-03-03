from wtforms import ValidationError
from flask import current_app
from functools import wraps
from flask import abort
from flask_login import current_user

def InstructorKeyValidatir(form,field):

    if not field.data:
        return
    if field.data == current_app.config['INSTRUCTOR_KEY']:
        return
    raise ValidationError('Instructor key is invalid')

def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role.name != role_name:
                abort(403)
            return f(*args,**kwargs)
        return wrapped
    return decorator    
