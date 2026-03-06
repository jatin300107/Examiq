from flaskquiz.model import Test, Option , Question
from flaskquiz.extensions import db
from flask_login import current_user
import random 
def Createtest(self , topic , difficulty , description, title , no_of_question ):
    test = Test(title = title , topic = topic , difficulty = difficulty , description = description , created_by = current_user.username)
    db.session.add(test)

    questions = Question.query.filter_by(topic = topic , difficulty = difficulty).all()
    random.shuffle(questions)
    selected_questions = questions[:no_of_question]
    for q in selected_questions:
        test.questions.append(q)
    db.session.commit()

