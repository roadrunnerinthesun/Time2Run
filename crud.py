"""CRUD operations"""

from model import db, User, Activity, connect_to_db


def create_user(email, password, username, fname, lname):
    """create and return a new user"""
    user = User(email=email, password=password, username=username, fname=fname, lname=lname)
    db.session.add(user)
    db.session.commit()

    return user


def get_user_by_email(email):
    """Return a user by email"""
    user = User.query.filter(User.email==email).first()
    return user


def verify_password(email, password):
    """Verify user by email and password"""
    user = User.query.filter(User.email == email).one()
    if user.password == password:
        return user
    else:
        return None


def get_user_by_username(username):
    """Return a user by username"""

    user = User.query.filter(User.username == username).first()
    return user


def create_activity(activity_name, time_in_min, distance, date_of_activity):
    """Create and return new running activity"""
    activity = Activity(activity_name=activity_name, time_in_min=time_in_min, distance=distance, date_of_activity=date_of_activity)
    db.session.add(activity)
    db.session.commit()

    return activity



if __name__ == '__main__':
    from server import app
    connect_to_db(app)