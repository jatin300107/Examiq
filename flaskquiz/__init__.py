from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
mail = Mail()
 
    
   

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']= 'af8f9bacb0973a8d9d1bcbb77b89a26ee5008004d3be87202994a37ca2621a9f'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS']= True
    app.config['MAIL_USERNAME'] = 'jatin30jan2007@gamil.com'
    app.config['MAIL_PASSWORD'] = 'ltmg gill bpor emdx'
    app.config['MAIL_DEFAULT_SENDER'] = 'jatin30jan2007@gamil.com'
    mail.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    from flaskquiz.route import main 
    app.register_blueprint(main)

    return app