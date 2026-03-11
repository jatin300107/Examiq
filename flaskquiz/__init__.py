from flask import Flask
from flaskquiz.extensions import db , login_manager

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'af8f9bacb0973a8d9d1bcbb77b89a26ee5008004d3be87202994a37ca2621a9f'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['INSTRUCTOR_KEY'] = 'i_am_instructor'
    
    
    db.init_app(app)
    login_manager.init_app(app)
    from flaskquiz.model import User
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    from .main import main 
    app.register_blueprint(main)
    from .auth import auth 
    app.register_blueprint(auth)

    return app