from flaskquiz.extensions import db
from flaskquiz.model import User , Role

from flask import  render_template , flash , url_for, redirect
from flask_login import login_required , current_user
from .decorators import role_required
from flaskquiz.forms import Update_user
from . import main as main_blueprint
main = main_blueprint
@main.route("/")
@main.route("/home",methods = ['GET','POST'])
def index():
    return render_template('home.html')

@main.route("/about")
def about():
    return "About Flask "

@main.route('/update',methods = ['GET','POST'])
def update_account():
    form = Update_user()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('auth.login'))
    else:
        flash("Updation unsucessful")
    
    return render_template('update.html', form = form)

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



