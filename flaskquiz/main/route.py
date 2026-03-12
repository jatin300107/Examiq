from flaskquiz.extensions import db
from flaskquiz.model import User , Role ,Question , Option , Test, TestAttempt , AttemptAnswer
from flaskquiz.services.services import Createtest , calculatescore
from flask import  render_template , flash , url_for, redirect , request
from flask_login import login_required , current_user
from .decorators import role_required
from flaskquiz.forms.forms import Update_user , CreateQuestion , Created_Test
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


@main.route("/createquestion",methods = ['GET','POST'])
@login_required
@role_required('Instructor')
def createquestion():
    form = CreateQuestion()
    if form.validate_on_submit():
        question = Question(text = form.questiontext.data ,topic = form.topic.data , difficulty = form.difficulty.data)
        db.session.add(question)
        db.session.commit()
        option1 = Option(option_text = form.option1.data , is_correct = False , question = question)
        option2 = Option(option_text = form.option2.data , is_correct = False , question = question)
        option3 = Option(option_text = form.option3.data , is_correct = False , question = question)
        option4 = Option(option_text = form.option4.data , is_correct = False , question = question)
        
        correct_map = {'option 1' : form.option1.data ,
            'option 2' : form.option2.data,
            'option 3' : form.option3.data ,
            'option 4' : form.option4.data}
        options = [option1 , option2 , option3 , option4]
        db.session.add_all(options)
        db.session.commit()
        correct_text = correct_map[form.correct_option.data]
        for option in options:
            if correct_text == option.option_text:
                option.is_correct = True
                db.session.commit()
        
        
        return redirect(url_for('main.instructoraccount'))
    return render_template('createquestion.html' , form = form)
    

@main.route('/createtest',methods = ['GET','POST'])
@login_required
@role_required('Instructor')
def createtest():
    form = Created_Test()
    if form.validate_on_submit():
        Createtest(topic = form.topic.data , difficulty = form.difficulty.data , description = form.description.data, title = form.title.data, no_of_question = form.no_of_question.data)
        return redirect(url_for('main.instructoraccount'))
    return render_template('createtest.html', form = form)


@main.route('/starttest/<int:test_id>',methods = ['GET','POST'])
@login_required
@role_required('Learner')
def starttest(test_id):
    attempt = TestAttempt(user_id = current_user.id ,score = 0, test_id = test_id )
    db.session.add(attempt)
    db.session.commit()
    return redirect(url_for('main.attempt' , test_id = test_id, attempt_id = attempt.id, page = 1))
@main.route('/attempt/<int:attempt_id>/',methods = ['GET','POST'])
@login_required
def attempt(attempt_id):
    page = request.args.get("page",1,type = int)
    attempt = TestAttempt.query.get(attempt_id)
    questions = attempt.test.questions
    total = len(questions)
    question = questions[page-1]

    if request.method == "POST":
        answer = AttemptAnswer.query.filter_by(attemptt_id=attempt.id).first()
        option_id = request.form.get("option")
        if not answer:
            
            answer = AttemptAnswer(attemptt_id =attempt.id , question_id = question.id , selected_option_id = option_id)
            db.session.add(answer)
            db.session.commit()
        else:
            answer.selected_option_id = option_id
            db.session.commit()

    
        if page >= total:
            return redirect(url_for("main.submittest" , attempt_id = attempt.id , page = page))
        return redirect(url_for("main.attempt" , attempt_id = attempt.id , page = page+1))
    return render_template('attempt.html' ,question=question, page=page, attempt=attempt)

@main.route('/submittest/<attempt_id>/<page>/',methods = ['GET','POST'])
@login_required
def submittest(attempt_id, page):
    score = calculatescore(attempt_id = attempt_id)
    attempt = TestAttempt.query.get(attempt_id)
    attempt.score = score
    db.session.commit()
    return redirect(url_for('main.result' , attempt_id = attempt.id ))

@main.route('/result/<attempt_id>/',methods = ['GET','POST'])
@login_required
def result(attempt_id ):
    attempt = TestAttempt.query.get(attempt_id)
    percentage = attempt.score /(4 * len(attempt.test.questions)) * 100
    return render_template('result.html' , attempt = attempt , score=attempt.score , percentagee = percentage)

@main.route('/showtests',methods = ['GET','POST'])
@login_required
def showtest():
    page = request.args.get("page" , 1, type = int)
    tests = Test.query.paginate(page = page , per_page = 5)
    if request.method == "POST":
        test_id = int(request.form.get("test_id"))
        return redirect(url_for('main.starttest', test_id = test_id))
    return render_template('viewtests.html', tests = tests)

@main.route('/myattemptedtest',methods = ['GET','POST'])
@login_required
@role_required('Learner')
def attemtedtest():
    page = request.args.get("page" , 1, type = int)
    query = TestAttempt.query.filter_by(user_id = current_user.id)
    attempted_test = query.paginate(page=page , per_page=5)
    return render_template('attemptedtest.html', attempted_test = attempted_test) 

@main.route('/mycreatedtests',methods = ['GET','POST'])
@login_required
@role_required('Instructor')
def mycreatedtests():
    page = request.args.get("page" , 1, type = int)
    query = Test.query.filter_by(created_by = current_user.id)
    created_test = query.paginate(page=page , per_page=5)  
    return render_template('createdtests.html', created_test = created_test)




