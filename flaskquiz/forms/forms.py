from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField , TextAreaField , RadioField , IntegerField , SelectField
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
    difficulty = SelectField('Difficulty',  choices = ["easy",   "medium" , "hard"] , coerce = to_lower , validators=[DataRequired() , Validate_difficulty])
    description = TextAreaField('Description')
    no_of_question = IntegerField("no of questions")
    submit = SubmitField('Create test')

class CreateQuestion(FlaskForm):
    questiontext = TextAreaField("Question", validators=[DataRequired()])
    topic = StringField('Topic' , validators=[DataRequired()])
    difficulty = SelectField('Difficulty' ,  choices = ["easy",   "medium" ,  "hard"] ,
                              coerce = to_lower , validators=[DataRequired() , Validate_difficulty])
    option1 = StringField('option 1' , validators=[DataRequired()])
    option2 = StringField('option 2' , validators=[DataRequired()])
    option3 = StringField('option 3' , validators=[DataRequired()])
    option4 = StringField('option 4' , validators=[DataRequired()])
    correct_option = RadioField("correct option" , choices = [("option 1" , "Option 1" ),
                                                              ("option 2", "Option 2"),("option 3" , "Option 3") , ("option 4" ,"Option 4")])
    submit = SubmitField('Create Question')

