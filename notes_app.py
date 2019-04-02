
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify
from flask import redirect

import json
import random
import os
import time

import storage

app = Flask(__name__)

_message=""

@app.route('/register', methods=['GET'])
def get_register():
    global _message
    response = make_response(render_template("register.html", message=_message))
    _message = None
    return response

@app.route('/register', methods=['POST'])
def post_register():
    global _message
    # save the registration to the profile database
    storage.add_profile({
        'user':request.form.get("user"),
        'email':request.form.get("email"),
        'password':request.form.get("password")     # <-- HORRIBLE
    })
    # if we are successful
    # -- PUT A CHECK HERE --
    if True:
        response =  make_response(redirect("/login"))
        _message = None
    else:
    # else if we are not successful
        response =  make_response(redirect("/register"))
        _message = "Error in registration, please try again."
    return response

@app.route('/')
@app.route('/login', methods=['GET'])
def get_login():
    global _message
    response = make_response(render_template("login.html", message=_message))
    _message = None
    return response

@app.route('/login', methods=['POST'])
def post_login():
    global _message
    user = request.form.get("user")
    password = request.form.get("password")
    profile = storage.get_profile(user)
    # create a rejection response
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    if not profile:
        _message = "User/password not found, please try again."
        return response
    if profile['password'] != password:
        # NEED TO HANDLE PASSWORDS CORRECTLY
        _message = "User/password not found, please try again."
        return response
    # create a success response
    response =  make_response(redirect("/notes"))
    # generate a (not really) random string 
    key = "session." + str(random.randint(1000000000,1999999999))
    # create a session based on that key
    storage.add_session({"key":key, "user":user, "login":int(time.time()), "pages":1})
    # store the key in a cookie
    response.set_cookie("session_key", key, max_age=600)
    _message = None
    return response

@app.route('/notes', methods=['GET'])
def get_notes():
    global _message
    key = request.cookies.get("session_key")
    # create a rejection response
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    if not key:
        _message = "User is not logged in."
        return response
    session = storage.get_session(key)
    if not session:
        _message = "User is not logged in."
        return response
    _message = None
    pages = session.get("pages",-999)
    pages=pages+1
    session["pages"] = pages
    storage.update_session(key, {"pages":pages})
    response = make_response(render_template("notes.html", message=_message, session=session))
    response.set_cookie("session_key", key, max_age=600)
    return response

@app.route('/notes', methods=['POST'])
def post_notes():
    key = request.cookies.get("session_key")
    # create a rejection response
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    _message = "User is not logged in."
    if not key:
        return response
    session = storage.get_session(key)
    if not session:
        return response
    # OK, we are logged in so process the form submission
    user = request.form.get("user")
    email = request.form.get("email")
    zip   = request.form.get("zip")
    note = request.form.get("note")
    if note != None and note != "":
        storage.add_note({'text': str(user + ": " + note)})
    response =  make_response(redirect("/notes"))
    response.set_cookie("session_key", key, max_age=600)
    _message = None
    return response

@app.route('/logout', methods=['GET'])
def get_logout():
    key = request.cookies.get("session_key")
    # create a rejection response
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    _message = "User is not logged in."
    if not key:
        return response
    session = storage.get_session(key)
    if not session:
        return response
    if key:
        storage.delete_session(key)
    response =  make_response(redirect("/login"))
    response.set_cookie("session_key", "", expires=0)
    _message = None
    return response

# API ROUTES

@app.route("/content/")
@app.route("/content/<search>")
def get_content(search=None):
    items = storage.get_notes(search)
    data = { "data": items }
    return jsonify(data)

@app.route("/remove/<int:id>")
def get_remove(id):
    storage.delete_note(id)
    return redirect("/notes")
