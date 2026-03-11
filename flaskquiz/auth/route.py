 
from flaskquiz.model import User , Role

from flask import  render_template , flash , url_for, Blueprint, redirect
from flask_login import current_user, logout_user, login_user
from flaskquiz.forms.forms import Register, Login
from flaskquiz.extensions import login_manager, bcrypt , db
from flask_login import login_required
from . import auth
@auth.route('/login', methods = ['GET','POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        if current_user.role.name == 'Instructor':
            return redirect(url_for('main.instructoraccount'))
        elif current_user.role.name == 'Learner':
                
            return redirect(url_for('main.learneraccount'))
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            if user.role.name == 'Instructor':
                login_user(user,remember=True)
                flash("Login successful")
                return redirect(url_for('main.instructoraccount'))
            elif user.role.name == 'Learner':
                login_user(user,remember=True)
                flash("Login successful")
                return redirect(url_for('main.learneraccount'))
        else:
            flash('Login unsuccessful')

    return render_template('login.html', form = form)

@auth.route('/register', methods = ['GET','POST'])
def register():
    form = Register()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash("profile already exists")
            return redirect(url_for('auth.register'))
        else:  
            instructor_role = Role.query.filter_by(name = 'Instructor').first()
            learner_role  = Role.query.filter_by(name = 'Learner').first()
            if form.instructor_key.data:
                assigned_role = instructor_role
            else:
                assigned_role = learner_role     
            user = User(username = form.username.data, password = hashed_pass,email = form.email.data, role = assigned_role )
            db.session.add(user)
            db.session.commit()
            flash('Registration Sucesfull')
            return redirect(url_for('auth.login'))
    else:
        print(form.errors)
    return render_template('register.html',form = form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))



