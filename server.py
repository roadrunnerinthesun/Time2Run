from flask import Flask, render_template, request, flash, redirect, session
# from flask module import Flask Class
from jinja2 import StrictUndefined
import os, requests, crud, model
from model import Activity
import re
from datetime import datetime, timedelta
import random


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

RANDOM_RUN = [
    "Run | <b>Life is short. Running makes it seem longer</b>.",
    "Sprint | <b>Most people never run far enough on their first wind to find out they've got a second</b>.",
    "Fast Walk | <b>All truly great thoughts are conceived while walking</b>.",
    "Light Jog | <b>Jogging is very beneficial. It's good for your legs and your feet. It's also very good for the ground. It makes it feel needed</b>.",
]

@app.route('/homepage')
def homepage():
    """Show homepage"""

    user = crud.get_user_by_username(session.get('username'))
    if user is None:
        flash('Please log in to view your homepage')
        return redirect('/')
    
    return render_template("homepage.html", user=user)


@app.route('/random_run')
def fortune():
    """Return a Random_Run as a text string on users homepage"""

    return random.choice(RANDOM_RUN)
    

@app.route('/registration')
def registration():
    """Show registration page"""
    
    return render_template('new_user.html')


@app.route('/profile', methods=['GET', 'POST'])
def show_profile():
    """Shows the profile of the user that is currently in session"""

    user = crud.get_user_by_username(session.get('username'))

    if user is None:
        flash('Please log in to view your profile')
        return redirect('/')


    if request.method == 'POST':
        
        date_of_birth = {
            'date_of_birth': request.form.get('date_of_birth')
        }
        updated_date_of_birth = crud.update_date_of_birth(user, date_of_birth) 
        flash('Your settings have been updated!')

        return render_template('profile.html', user=updated_date_of_birth)

    return render_template('profile.html', user=user)


@app.route('/record_run')
def record_run():
    """Record a running activity"""

    user = crud.get_user_by_username(session.get('username'))
    
    if user is None:
        flash('Please log in to record your run')
        return redirect('/')

    return render_template('record_run.html', user=user)



@app.route('/run_activity', methods=['POST'])
def run_activity():
    """Record a running activity"""

    activity_name = request.form.get('activity name')
    time_in_min = request.form.get('time in min')
    distance = request.form.get('distance')
    date_of_activity = request.form.get('date of activity')

    logged_in_email = session.get('email')

    if logged_in_email is None:
        flash('Please log in to record activity')
        return redirect('/')
    else:
        user = crud.get_user_by_email(logged_in_email)

        crud.create_activity(user, activity_name, time_in_min, distance, date_of_activity)
    
    return redirect('/homepage')



# Helper function required to obtain total for distance from list of activities
def get_total_distance(activity_list):
    total = 0
    for activity in activity_list:
        total = total+activity.distance
    return total


@app.route('/view_stats')
def view_stats():
    """View results of users running activity."""

    user = crud.get_user_by_username(session.get('username'))

    if user is None:
        flash('Please log in to view your stats')
        return redirect('/')

    else:
        total_distance = crud.calculate_total_distance(session.get('username'))
        total_time = crud.calculate_total_time(session.get('username'))

        
        
        one_week = get_total_distance(crud.seven_day_distance(session.get('username')))
        two_weeks = get_total_distance(crud.fourteen_day_distance(session.get('username')))
        four_weeks = get_total_distance(crud.thirty_day_distance(session.get('username')))

    return render_template('view_stats.html', user=user, 
                                              total_distance=total_distance,
                                              total_time=total_time,
                                              one_week=one_week,
                                              two_weeks=two_weeks,
                                              four_weeks=four_weeks)


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