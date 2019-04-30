from flask import Flask, redirect

app = Flask(__name__)

import hello_routes
import login_routes
import notes_routes
import api_routes

@app.route('/', methods=['GET'])
def get_index():
    return redirect("/login")
