# A very simple Flask Hello World app for you to get started with...

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import redirect

import notes_api

app = Flask(__name__)

_message=""

@app.route('/')
@app.route('/notes', methods=['GET'])
def get_notes():
    return render_template("notes.html", message=_message)

@app.route('/notes', methods=['POST'])
def post_notes():
    note = request.form.get("note")
    if note != None and note != "":
        notes_api.add_note(str(note))
    return redirect("/notes")

@app.route("/content/")
@app.route("/content/<search>")
def get_content(search=None):
    items = notes_api.get_notes(search)
    data = { "data": items }
    return jsonify(data)

@app.route("/remove/<int:id>")
def get_remove(id):
    notes_api.delete_note(id)
    return redirect("/notes")
