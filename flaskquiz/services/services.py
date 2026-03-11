from flaskquiz.model import Test, Option , Question , TestAttempt , AttemptAnswer
from flaskquiz.extensions import db
from flask_login import current_user
import random 
def Createtest( topic , difficulty , description, title , no_of_question ):
    test = Test(title = title , topic = topic , difficulty = difficulty , description = description , created_by = current_user.id)
    db.session.add(test)

    questions = Question.query.filter_by(topic = topic , difficulty = difficulty).all()
    random.shuffle(questions)
    selected_questions = questions[:no_of_question]
    for q in selected_questions:

        
        test.questions.append(q)
    db.session.commit()

def calculatescore( attempt_id):
    score=0
    answers = AttemptAnswer.query.filter_by(attemptt_id = attempt_id).all()
    for ans in answers:
    
        option = Option.query.get(ans.selected_option_id)
   
        if option.is_correct == True:
            score += 4
        else:
            score -= 1
    return score
