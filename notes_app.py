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

import data_api

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
    data_api.add_profile({
        'user':request.form.get("user"),
        'email':request.form.get("email"),
        'password':request.form.get("password")
    })
    # save the registration to the profile database
    # if we are successful
    if True:
        response =  make_response(redirect("/login"))
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
    profiles = data_api.get_profiles(user)
    if len(profiles) > 0:
        if profiles[0]['password'] == password:
            response =  make_response(redirect("/notes"))
            return response
    response =  make_response(redirect("/login"))
    _message = "User/password not found, please try again."
    return response

@app.route('/notes', methods=['GET'])
def get_notes():
    global _message
    key = request.cookies.get("session_key","none")   
    if os.path.exists(key + ".dat"):
        with open(key + ".dat", "r") as f:
            session = json.load(f)
    else:
        session = {

        }
    response = make_response(render_template("notes.html", message=_message, session=session))
    _message = None
    return response

@app.route('/notes', methods=['POST'])
def post_notes():
    user = request.form.get("user")
    email = request.form.get("email")
    zip   = request.form.get("zip")
    note = request.form.get("note")
    session_key = request.form.get("session_key")
    if note != None and note != "":
        data_api.add_note(str(user + ": " + note))
    response =  make_response(redirect("/notes"))
    key = str(random.randint(1000000000,1999999999))
    session = {
        "user": user,
        "email": email,
        "zip" : zip,
        "key" : session_key
    }
    with open(key + ".dat", "w") as f:
        json.dump(session,f)
    response.set_cookie("session_key",key)
    return response

@app.route('/logout', methods=['GET'])
def get_logout():
    key = request.cookies.get("session_key")
    response =  make_response(redirect("/notes"))
    session = {}
    with open(key + ".dat", "w") as f:
        json.dump(session,f)
    response.set_cookie("session_key",key)
    return response

# API ROUTES

@app.route("/content/")
@app.route("/content/<search>")
def get_content(search=None):
    items = data_api.get_notes(search)
    data = { "data": items }
    return jsonify(data)

@app.route("/remove/<int:id>")
def get_remove(id):
    data_api.delete_note(id)
    return redirect("/notes")
