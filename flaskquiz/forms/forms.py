from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , TextAreaField
from wtforms.validators import DataRequired, EqualTo, Length,Email
from flaskquiz.model import User
from flask_login import current_user
from .validators import InstructorKeyValidatir , Validate_difficulty , to_lower

class Register(FlaskForm):
    username = StringField('Username' , validators=[DataRequired(),Length(min = 2, max = 20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8)])
    check_password = PasswordField('Confirm Passsword', validators=[DataRequired(),EqualTo('password')])
    instructor_key = StringField('instructor_key' ,validators=[InstructorKeyValidatir])
    submit = SubmitField('Sign Up')
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user:
            raise ValidationError("Username already exists")
    
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError("email already exists")

class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password',validators=[DataRequired(), Length(min=8)])
    instructor_key = StringField('instructor_key' ,validators=[InstructorKeyValidatir])
    submit = SubmitField('Sign Up')

class Update_user(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),Length(min = 2, max = 20)])
    email = StringField('Email', validators=[DataRequired(),Email()])
    submit = SubmitField('Update')
    def validate_username(self,username):
        if username.data != current_user.username:
            user = User.query.filter_by(username = username.data).first()
            if user:
                raise ValidationError("Username already exists")
    
    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email = email.data).first()
            if user:
                raise ValidationError("email already exists")

class Created_Test(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    topic = StringField('Topic', validators=[DataRequired()])
    difficulty = StringField('Difficulty',  choices = ["easy", "Easy" , "Medium", "medium" , "Hard", "hard"] , coerce = to_lower , validators=[DataRequired() , Validate_difficulty])
    description = TextAreaField('Description')

        