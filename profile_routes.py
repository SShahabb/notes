#
# PROFILE ROUTES
#

import hashlib
import random
import string
import time

from flask import request, render_template, make_response, redirect

import storage

from main import app
from main import verify_login

@app.route('/profile', methods=['GET'])
def get_profile():
    response = verify_login(request)
    if response:
        return response
    message = request.cookies.get("message")
    key = request.cookies.get("session_key")
    session = storage.get_session(key)
    user = session.get("user")
    profile = storage.get_profile(user)
    response = make_response(render_template("profile.html", message=message, session=session, profile=profile))
    response.set_cookie("session_key", key, max_age=600)
    response.set_cookie("message","",expires=0)
    return response

@app.route('/profile', methods=['POST'])
def post_profile():
    response = verify_login(request)
    if response:
        return response
    message = request.cookies.get("message")
    key = request.cookies.get("session_key")
    session = storage.get_session(key)
    user = session.get("user")
    email = request.form.get("email")
    zipcode = request.form.get("zipcode")
    storage.update_profile(user,{"email":email, "zipcode":zipcode})
    response =  make_response(redirect("/notes"))
    response.set_cookie("session_key", key, max_age=600)
    response.set_cookie("message","",expires=0)

    return response
