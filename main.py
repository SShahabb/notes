from flask import Flask, redirect, make_response

import storage

app = Flask(__name__)

def verify_login(request):
    key = request.cookies.get("session_key")
    if not key or not storage.get_session(key):
        response =  make_response(redirect("/login"))
        response.set_cookie("session_key", "", expires=0)
        response.set_cookie("message","User is not logged in.")
        return response
    return None

@app.route('/', methods=['GET'])
def get_index():
    return redirect("/login")

import hello_routes
import login_routes
import notes_routes
import profile_routes
import api_routes

