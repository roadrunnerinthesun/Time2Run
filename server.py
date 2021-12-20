from flask import Flask, render_template, request, flash, redirect, session
# from flask module import Flask Class
from jinja2 import StrictUndefined
import os, requests, crud, model
from model import Activity


# create instance of a flask web application
app = Flask(__name__)
# Required to use Flask sessions
app.secret_key = "run"
# Causes an undefined variable in jinja to throw an error, 
# instead of failing without error
app.jinja_env.underfined = StrictUndefined

###############################################################################
#                        APP NAVIGATION ROUTES                                #
###############################################################################


# @app.route('/homepage')
# def homepage():
#     """Show homepage."""

#     return render_template('homepage.html', values=Activity.query.all())


@app.route('/homepage')
def homepage():
    """Show homepage."""

    user = crud.get_user_by_username(session.get('username'))

    # print(' ')
    # print(user)
    # print(Activity.query.all())
    # print(user.activities)
    # print(' ')

    return render_template('homepage.html', values=Activity.query.all())





# @app.route("/<user_id>-homepage")
# def display_profile(user_id):
#     """Display a student profile"""

#     user = User.query.filter(User.user_id == user_id).first()

#     return render_template("homepage.html", user=user)

    # # user = session.get('email')
    # user = crud.get_user_by_username(session.get('username'))
    # print (">>>>>>hello>>>>>>>>>>>>", user.activity)

    # return render_template('homepage.html', activity=user.activity)



# @app.route('/homepage')
# def homepage():
#     """Show homepage."""

#     return render_template('homepage.html', values=Activity.query.all())



###############################################################

# @app.route('/homepage')
# def homepage():
#     """Show homepage."""

#     # session['email'] = user.email
#     email = session['email']
#     user_activities = crud.get_user_activities(email)
    
#     return render_template('homepage.html', get_user_activities=user_activities)
    
    
    
    ##################################
    
    # return render_template('homepage.html', values=Activity.query.filter_by(user=user).all())
    # return render_template('homepage.html', 
    #                         values=Activity.query.filter(user=user).all())




@app.route('/registration')
def registration():
    return render_template('new_user.html')


@app.route('/profile')
def show_profile():
    """Shows the profile of the user that is currently in session"""
    user = crud.get_user_by_username(session.get('username'))

    return render_template('profile.html', user=user)



@app.route('/record_run')
def record_run():
    """Record a running activity"""
    return render_template('record_run.html')


@app.route('/run_activity', methods=['POST'])
def run_activity():
    """Record a running activity"""

    activity_name = request.form.get('activity name')
    time_in_min = request.form.get('time_in_mins')
    distance = request.form.get('distance')
    date_of_activity = request.form.get('date of activity')

    logged_in_email = session.get('email')

    if logged_in_email is None:
        flash("Log in to record activity")
        return redirect('/')
    else:
        user = crud.get_user_by_email(logged_in_email)

        print('--> User in server run activity')
        # print(user)

        crud.create_activity(user, activity_name, time_in_min, distance, date_of_activity)
        print('--> crud: create_activity')
        # print(user)
    
    return redirect('/homepage')



@app.route('/view_stats')
def view_stats():
    """View results of users running activity."""

    # Need to use join for user & activity tables

    return render_template('view_stats.html')


###############################################################################
#                      USER AUTHENTICATION ROUTES                             #
###############################################################################

@app.route('/')
def login():
    """Landing Page and Login page"""
    return render_template('login.html')


@app.route('/user_login', methods = ['POST'])
def user_login():
    """Landing Page and Login an existing User"""

    # Get form values from login form and verifying email/password
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.verify_password(email, password)
    
    if not user:
        flash('Login details are incorrect, please try again')
        return redirect('/')

    session['email'] = user.email
    session['username'] = user.username
    return redirect('/homepage')



@app.route('/new_user', methods=['POST'])
def create_new_user():
    """create a new user"""

    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    fname = request.form.get('fname').title()
    lname = request.form.get('lname').title()

    user = crud.get_user_by_email(email)
    
    if user:
        flash ('Email already registered, please log in')
    elif crud.get_user_by_username(username):
        flash('Username already is use, please choose another')
        return render_template ('new_user.html')
    else:
        crud.create_user(email, password, username, fname, lname)
        flash (f"{username} Your Account has been created, please log in")
        return render_template('login.html')
        
    
    return render_template('login.html')


@app.route('/logout')
def logout():
    """create a new user"""
    session.clear()
    flash ('You\'ve been logged out')
    return redirect("/")


###############################################################################
#                                 RUN APP                                     #
###############################################################################

if __name__ == '__main__':
    app.debug = True # allow us to not have to rerun server everytime we make a change
    model.connect_to_db(app)
    app.run(host='0.0.0.0')