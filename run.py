from flaskquiz import create_app
from flaskquiz.extensions import db


app = create_app()

with app.app_context():
    db.create_all()