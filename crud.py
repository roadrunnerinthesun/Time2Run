"""CRUD operations"""

from model import db, User, Activity, connect_to_db


def create_user(email, password, username, fname, lname):
    """create and return a new user"""
    user = User(email=email, password=password, username=username, fname=fname, lname=lname)
    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_email(email):
    return User.query.filter(User.email==email).first()



def verify_password(email, password):
    user = User.query.filter(User.email == email).first()
    if user is None:
        return False
    else:
        return user.password == password


def create_activity(activity_name, time_in_min, distance, date_of_activity):
    """create new running activity"""
    activity = Activity(activity_name=activity_name, time_in_min=time_in_min, distance=distance, date_of_activity=date_of_activity)
    db.session.add(activity)
    db.session.commit()

# Do I need to create a CRUD function for my view stats? ---> yes





if __name__ == '__main__':
    from server import app
    connect_to_db(app)