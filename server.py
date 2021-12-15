from flask import Flask, render_template, request, flash, redirect, session
# from flask module import Flask Class
from jinja2 import StrictUndefined
import os, requests, crud, model


# create instance of a flask web application
app = Flask(__name__)
# Required to use Flask sessions
app.secret_key = "run"
# Causes an undefined variable in jinja to throw an error, instead of failing without error
app.jinja_env.underfined = StrictUndefined

###############################################################################
#                        APP NAVIGATION ROUTES                                #
###############################################################################

@app.route('/homepage')
def homepage():
    """Show homepage."""
    return render_template('homepage.html')


@app.route('/registration')
def registration():
    return render_template ('new_user.html')


@app.route('/profile')
def profile_page():
    """Show User Profile Page"""
    return render_template('profile.html')


@app.route('/record_run')
def record_run():
    """Record a running activity"""
    return render_template('record_run.html')



@app.route('/run_activity')
def run_activity():
    """Record a running activity"""

    activity_name = request.form.get('activity name')
    time_in_min = request.form.get('password')
    distance = request.form.get('time in mins')
    date_of_activity = request.form.get('date of activity')

    crud.create_activity(activity_name, time_in_min, distance, date_of_activity)
    
    return render_template('record_run.html')


@app.route('/view_stats')
def view_stats():
    """View the results of the route search."""
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
        flash("Your login details are incorrect, please try again")
        return redirect('/')


    session["email"] = user.email
    session["username"] = user.username
    # flash("Logged in.")
    return redirect("/homepage")


# @app.route('/')
# def login():
#     """Landing Page and Login an existing User"""

#     # Get form values from login form and verifying email/password
 
#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = crud.verify_password(email, password)

#     if user:
#         # Save logged user to session
#         session['email'] = email
#         flash (f"{email} Welcome Back!")
#         return render_template('homepage.html')
#     else:
#         return render_template('login.html')


# @app.route('/', methods=['POST'])
# def login():
#     """Landing Page and Login an existing User"""
#     # Get form values from login form and verifying email
#     email = request.form.get('email')
#     password = request.form.get('password')

#     user = crud.get_user_by_email(email)

#     if not user or user.password!= password:
#         flash("Your e-mail or password was incorrect, please try again.")
#     else:
#         # Store users login in session
#         session['email'] = user.email
#         flash(f"Hi, {user.email}!")
#     return redirect("/")


@app.route('/new_user', methods=['POST'])
def create_new_user():
    """create a new user"""

    email = request.form.get('email')
    password = request.form.get('password')
    username = request.form.get('username')
    fname = request.form.get('fname')
    lname = request.form.get('lname')

    user = crud.get_user_by_email(email)
    
    if user:
        flash ('Email already registered, please log in')
    else:
        crud.create_user(email, password, username, fname, lname)
        flash (f"{username} Welcome! Your Account has been created")
        return render_template('homepage.html')
    
    return render_template('login.html')


@app.route("/logout")
def logout():
    """create a new user"""
    session.clear()
    flash ("You're are now logged out")
    return redirect("/")


###############################################################################
#                                 RUN APP                                     #
###############################################################################

if __name__ == '__main__':
    app.debug = True # allow us to not have to rerun server everytime we make a change
    model.connect_to_db(app)
    app.run(host='0.0.0.0')