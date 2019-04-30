#
# NOTES ROUTES
#

import time

from flask import request, render_template, make_response, redirect

import storage

from main import app

@app.route('/notes', methods=['GET'])
def get_notes():
    message = request.cookies.get("message")
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
    response = make_response(render_template("notes.html", message=message, session=session))
    storage.update_session(key, {"pages":(session.get("pages",0) + 1)})
    response.set_cookie("session_key", key, max_age=600)
    response.set_cookie("message","",expires=0)
    return response

@app.route('/notes', methods=['POST'])
def post_notes():
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
    # OK, we are logged in so process the form submission
    user = request.form.get("user")
    email = request.form.get("email")
    zip   = request.form.get("zip")
    note = request.form.get("note")
    if note != None and note != "":
        storage.add_note({'text': str(user + ": " + note)})
    response =  make_response(redirect("/notes"))
    response.set_cookie("session_key", key, max_age=600)
    response.set_cookie("message","",expires=0)
    return response
