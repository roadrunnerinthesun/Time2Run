"""CRUD operations"""

from model import db, User, Activity, connect_to_db


def create_user(email, password, username, fname, lname):
    """create and return a new user"""
    user = User(email=email, password=password, username=username, fname=fname, lname=lname)
    db.session.add(user)
    db.session.commit()

    return user

def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email"""

    return User.query.filter(User.email == email).first()
    


def verify_password(email, password):
    """Verify user by email and password"""

    verified = User.query.filter(User.email == email).one()
    if verified.password == password:
        return verified
    else:
        return None


def get_user_by_username(username):
    """Return a user by username"""

    return User.query.filter(User.username == username).first()
    

def get_activity_by_id(running_activity_id):
    """Return a running activity by primary key."""

    return Activity.query.get(running_activity_id)


def create_activity(user, activity_name, time_in_min, distance, date_of_activity):
    """Create and return new running activity"""
    print('--> User in create_activity')
    print(user)
    activity = Activity(user=user, activity_name=activity_name, time_in_min=time_in_min, distance=distance, date_of_activity=date_of_activity)
    db.session.add(activity)
    db.session.commit()

    return activity

# def user_profile(username, fname, lname):
#     user_profile = Activity.query.options(db.joinedload("user")).order_by(User.fname).all()

############################################################################################################################33

# def get_user_id(user_id, running_activity_id):
#     """Return primary key from User"""
#     user = User.query.filter(User.user_id==user_id, User.running_activity_id==running_activity_id).first()
#     return user.running_activity_id    


# # trying below for user activities on Homepage
# def get_user_activities(user_id):
#     """Return all user's running activities"""
#     user = User.query.filter(User.user_id==user_id).one()
#     return user.activity





if __name__ == '__main__':
    from server import app
    connect_to_db(app)