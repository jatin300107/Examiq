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

class Test(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String,unique = True,nullable = False)
    test = db.Column(db.String , unique = True , nullable = False)
    description = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default=datetime.utcnow())
    
