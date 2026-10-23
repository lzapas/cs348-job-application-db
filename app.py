import os

from dotenv import load_dotenv
from flask import Flask, render_template

from models import db

load_dotenv()

app = Flask(__name__)

# Secrets come from .env (see .env.example); the fallback is for local dev only
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-only-change-me')
# Relative SQLite paths resolve to the instance/ folder in Flask-SQLAlchemy 3
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///job_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def hello():
    return render_template('index.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, host='0.0.0.0', port=5000)
