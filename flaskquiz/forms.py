from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length,Email
from flaskquiz.model import User
from flask_login import current_user
from flaskquiz.lab import InstructorKeyValidatir

class Register(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min = 2, max = 20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8)])
    check_password = PasswordField('Confirm Passsword', validators=[DataRequired(),EqualTo('password')])
    instructor_key = StringField('instructor_key' ,validators=[InstructorKeyValidatir])
    submit = SubmitField('Sign Up')
    

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8)])
    instructor_key = StringField('instructor_key' ,validators=[InstructorKeyValidatir])
    submit = SubmitField('Sign Up')