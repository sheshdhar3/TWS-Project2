import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'mysql+pymysql://root:test321@db:3306/mydatabase')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Model definition
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)

tables_created = False

def create_tables():
    try:
        global tables_created
        if not tables_created:
            app.logger.debug("Creating database tables...")
            db.create_all()
            if not User.query.first():
                app.logger.debug("Inserting initial data into the database...")
                db.session.add(User(name="This is first list in db---SheshDhar"))
                db.session.add(User(name="This is second list in db---Testusers"))
                db.session.commit()
            else:
                app.logger.debug("Database already has data.")
            tables_created = True
    except Exception as e:
        app.logger.error(f"Error creating tables: {str(e)}")

@app.before_request
def before_request_func():
    create_tables()

@app.route('/')
def hello():
    return "Hello, This is for Project2, For Two tier Applications"

@app.route('/Users')
def get_users():
    try:
        users = User.query.all()
        return jsonify([user.name for user in users])
    except Exception as e:
        app.logger.error(f"Error fetching users: {str(e)}")
        return f"Error fetching users: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=82)

