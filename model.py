import os
from  flask_sqlalchemy import SQLAlchemy 

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(255), nullable=False, unique=False)
    password = db.Column(db.String(255), nullable=False, unique=True)

    teams = db.relationship("Team", backref ="user", lazy = True)

def __init__(self, username, password):
        self.username = username
        self.password = password


class Team(db.Model):
    __tablename__ = "teams"
    
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    teamname = db.Column(db.String(255), nullable = False, unique = False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable = False)

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    projectname = db.Column(db.String(255), nullable = False, unique = True)
    description = db.Column(db.String(255), nullable = False, unique = True)
    completed = (db.Column(db.Boolean, default = False))
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), nullable = False)

def connect_to_db(app):

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URI"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    print(app.config["SQLALCHEMY_DATABASE_URI"]) 
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
   from flask import Flask
   app = Flask(__name__)
   connect_to_db(app)
   print("connected to database")

