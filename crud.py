"""CRUD operations"""

from model import db, User, Activity, connect_to_db
from datetime import datetime, timedelta


def create_user(email, password, username, fname, lname):
    """create and return a new user"""
    user = User(email=email, password=password, username=username, fname=fname, lname=lname)
    db.session.add(user)
    db.session.commit()

    return user


def update_date_of_birth(user, date_of_birth):
    """Update users date of birth in user table"""

    for key, value in date_of_birth.items():
        if value is not "" or value is not None: 
            setattr(user, key, value)

        # db.session.add(user)
        db.session.commit() # persists updates in database

    return user



def get_user_by_id(user_id):
    """Return user object by id."""

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

    return User.query.options(db.joinedload("activities")).filter(User.username == username).first()
    
    
def get_activity_by_id(running_activity_id):
    """Return a running activity by primary key."""

    return Activity.query.get(running_activity_id)



def create_activity(user, activity_name, time_in_min, distance, date_of_activity):
    """Create and return new running activity"""

    activity = Activity(user=user, activity_name=activity_name, time_in_min=time_in_min, distance=distance, date_of_activity=date_of_activity)
    db.session.add(activity)
    db.session.commit()

    return activity



def calculate_total_distance(username):
    """Calculate the total distance by user."""
    
    user = get_user_by_username(username)

    total_distance = 0

    for activity in user.activities:
        if activity.distance:
            total_distance = total_distance + activity.distance
    
    return total_distance

def calculate_total_time(username):
    """Calculate the total time by user."""
    
    user = get_user_by_username(username)

    total_time = 0

    for activity in user.activities:
        if activity.distance:
            total_time = total_time + activity.time_in_min
    
    return total_time





# def get_activity_by_type_by_user(username):
#     """Return a user by username"""

#     return User.query.options(db.joinedload("activities")).filter(User.username == username).first()
#     return User.query.options(db.joinedload("activities")).filter(User.username == username, activity_name='Run').all()

    # return User.query.options(db.joinedload("activities")).filter_by(activity_name='Run').all() #works for all runs for all users

# activity = Activity.query.filter_by(activity_name='Run').all()




############################################################################################################################33

# def get_user_id(user_id, running_activity_id):
#     """Return primary key from User"""
#     user = User.query.filter(User.user_id==user_id, User.running_activity_id
# running_activity_id).first()
#     return user.running_activity_id    


# # trying below for user activities on Homepage
# def get_user_activities(user_id):
#     """Return all user's running activities"""
#     user = User.query.filter(User.user_id==user_id).one()
#     return user.activity


def seven_day_distance(username):

    user = User.query.filter(User.username == username).one()

    now = datetime.now()
    seven_days_ago = timedelta(days=-7) 
    seven_days_ago_from_today = now + seven_days_ago
    
    seven = Activity.query.filter(Activity.user_id == user.user_id,
                                Activity.date_of_activity < now, 
                                Activity.date_of_activity > seven_days_ago_from_today).all()
  
    # returns a list of activities over 7 day parameter
    return seven


def fourteen_day_distance(username):

    user = User.query.filter(User.username == username).one()
    
    now = datetime.now()
    fourteen_days_ago = timedelta(days=-14) 
    fourteen_days_ago_from_today = now + fourteen_days_ago
    
    fourteen = Activity.query.filter(Activity.user_id == user.user_id,
                                Activity.date_of_activity < now, 
                                Activity.date_of_activity > fourteen_days_ago_from_today).all()

    # returns a list of activities over 14 day parameter
    return fourteen
    

def thirty_day_distance(username):

    user = User.query.filter(User.username == username).one()

    now = datetime.now()
    thirty_days_ago = timedelta(days=-30) 
    thirty_days_ago_from_today = now + thirty_days_ago
    
    thirty = Activity.query.filter(Activity.user_id == user.user_id,
                                Activity.date_of_activity < now, 
                                Activity.date_of_activity > thirty_days_ago_from_today).all()

    # returns a list of activities over 30 day parameter
    return thirty




if __name__ == '__main__':
    from server import app
    connect_to_db(app)