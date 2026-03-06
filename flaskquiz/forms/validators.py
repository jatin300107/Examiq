from wtforms import ValidationError
from flask import current_app

def InstructorKeyValidatir(form,field):

    if not field.data:
        return
    if field.data == current_app.config['INSTRUCTOR_KEY']:
        return
    raise ValidationError('Instructor key is invalid')

def Validate_difficulty(form, field):
    field.data.lower()
    allowed_difficulty = {"easy" , "medium" , "hard"}
    if field.data not in allowed_difficulty:
        raise ValidationError("Invalid difficluty level")
    
def to_lower(value):
    return value.lower() if value else value