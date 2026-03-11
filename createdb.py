from flaskquiz import create_app
from flaskquiz.extensions import db
from flaskquiz.model import Role


app = create_app()

with app.app_context():
    db.create_all()

    if not Role.query.all():
        db.session.add_all([
            Role(name='Instructor'),
            Role(name='Learner')

        ])
        db.session.commit()
        print("Roles created")