from flaskquiz.extensions import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20) , unique = True, nullable = False)
    email = db.Column(db.String(40), unique = True , nullable = False)
    password = db.Column(db.String(40), unique = True, nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable = False)
    test_created = db.relationship("Test",backref = "creator", lazy = True)
    attempt = db.relationship("TestAttempt", backref = "user",lazy = True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20),unique = True,nullable = False)

    users = db.relationship("User", backref = "role", lazy = True)


test_question = db.Table("test_question",db.Column("test_id" , db.ForeignKey("test.id") , primary_key = True) , db.Column("question_id", db.ForeignKey("question.id"), primary_key = True))

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String,nullable = False)
    topic = db.Column(db.String  , nullable = False)
    difficulty = db.Column(db.String(10) , nullable = False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    questions = db.relationship("Question" , secondary = test_question , backref = "test")
    attempt = db.relationship('TestAttempt' ,backref= 'test', lazy = True)
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.Text , nullable = False)
    difficulty = db.Column(db.String(10) , nullable = False)
    topic = db.Column(db.String(20), nullable = False)
    options = db.relationship("Option" , backref = "question", lazy = True)

class Option(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer , db.ForeignKey("question.id") , nullable = False)
    option_text = db.Column(db.String(200))
    is_correct = db.Column(db.Boolean)


class TestAttempt(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer,db.ForeignKey("user.id"),nullable = False)
   
    score = db.Column(db.Integer, nullable = False)
    test_id = db.Column(db.Integer , db.ForeignKey("test.id") , nullable = False)

class AttemptAnswer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer , db.ForeignKey("question.id"), nullable = False)
    attemptt_id = db.Column(db.Integer, db.ForeignKey("test.id"), nullable = False)
    selected_option_id = db.Column(db.Integer , db.ForeignKey("option.id"), nullable = False)
    attempted_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())


