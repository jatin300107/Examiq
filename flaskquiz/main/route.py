from flaskquiz import bcrypt
from flaskquiz import User , Role
from flaskquiz import db
from flask import  render_template , flash , url_for, Blueprint, redirect
from flask_login import login_required
from flaskquiz.lab import role_required
main = Blueprint('main',__name__)
@main.route("/")
@main.route("/home",methods = ['GET','POST'] )
def index():
    return render_template('home.html')
@main.route("/home")
def home():
    return render_template('home.html')
@main.route("/about")
def about():
    return "About Flask "

@main.route('/instructoraccount',methods = ['GET','POST'])
@login_required
@role_required('Instructor')
def instructoraccount():
    return render_template('instructoraccount.html')

@main.route('/learneraccount',methods = ['GET','POST'])
@login_required
@role_required('Learner')
def learneraccount():
    return render_template('learneraccount.html')



