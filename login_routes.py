#
# LOGIN ROUTES
#

import hashlib
import random
import string
import time

from flask import request, render_template, make_response, redirect

import storage

from main import app

def random_string(n):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for i in range(n))

def encrypt(password, salt):
    return hashlib.sha256((password+salt).encode()).hexdigest()

@app.route('/login', methods=['GET'])
def get_login():
    message = request.cookies.get("message")
    response = make_response(render_template("login.html", message=message, session=None))
    response.set_cookie("message","",expires=0)
    return response

@app.route('/login', methods=['POST'])
def post_login():
    user = request.form.get("user")
    password = request.form.get("password")
    profile = storage.get_profile(user)
    # create a rejection response
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    if not profile:
        response.set_cookie("message","User/password not found, please try again.")
        return response
    if profile['password'] != encrypt(password, profile['salt']):
        # NEED TO HANDLE PASSWORDS CORRECTLY
        response.set_cookie("message","User/password not found, please try again.")
        return response
    # create a success response
    response =  make_response(redirect("/notes"))
    # generate a (not really) random string 
    key = "session." + random_string(32)
    # create a session based on that key
    storage.add_session({"key":key, "user":user, "login":int(time.time()), "pages":1})
    # store the key in a cookie
    response.set_cookie("session_key", key, max_age=600)
    return response

@app.route('/logout', methods=['GET'])
def get_logout():
    key = request.cookies.get("session_key")
    # create a rejection response
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    if not key:
        response.set_cookie("message","User is not logged in.")
        return response
    session = storage.get_session(key)
    if not session:
        response.set_cookie("message","User is not logged in.")
        return response
    if key:
        storage.delete_session(key)
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    response.set_cookie("message","",expires=0)
    return response

@app.route('/register', methods=['GET'])
def get_register():
    message = request.cookies.get("message")
    response = make_response(render_template("register.html", message=message, session=None))
    response.set_cookie("message","",expires=0)
    return response

@app.route('/register', methods=['POST'])
def post_register():
    salt = random_string(32)
    print("SALT = ",salt)
    # save the registration to the profile database
    print(request.form)
    storage.add_profile({
        'user':request.form.get("user"),
        'email':request.form.get("email"),
        'salt':salt,
        'password':encrypt(request.form.get("password"), salt)
    })
    # if we are successful
    # -- PUT A CHECK HERE --
    if True:
        response =  make_response(redirect("/login"))
        response.set_cookie("message","",expires=0)
    else:
    # else if we are not successful
        response =  make_response(redirect("/register"))
        response.set_cookie("message","Error in registration, please try again.")
    return response

