"""
Data models for app

"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A registered user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    fname = db.Column(db.String(30), nullable=False)
    lname = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.DateTime)
    home_address = db.Column(db.String(100))

    # activities = a list of Activity objects

   
    # repr: produces a string output so we review db entries
    def __repr__(self):
        """show info about user"""
        return f"<User user_id={self.user_id}, username={self.username}, email={self.email}>"


class Activity(db.Model):
    """Data model for running activity."""

    __tablename__ = "activities"

    running_activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id")) 
    date_of_activity = db.Column(db.Date)
    distance = db.Column(db.Float)
    time_in_min = db.Column(db.Integer)
    activity_name = db.Column(db.String(50))
    
    # One user many activities
    user = db.relationship("User", backref="activities")
    

    def __repr__(self):
        """show info about running activity"""
        return f"<Activity running_activity_id={self.running_activity_id}, activity_name={self.activity_name}, user_id={self.user_id}>"


def connect_to_db(flask_app, db_uri="postgresql:///Time2Run", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    # flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    connect_to_db(app)
