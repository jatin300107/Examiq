from flaskquiz import db


class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(20) , unique = True, nullable = False)
    email = db.Column(db.String(40), unique = True , nullable = False)
    password = db.Column(db.String(40), unique = True, nullable = False)
    role_id = db.relationship(db.Integer, db.ForeignKey("role.id"), nullable = False)
    test_created = db.relationship("Test",backref = "creator", lazy = True)
    attempt = db.relationship("TestAttempt", backref = "user",lazy = True)

class Role(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(20),unique = True,nullable = False)

    users = db.relationship("User", backref = "role", lazy = True)