from flask import Flask
from flask import render_template
from flask import request

import notes

app = Flask(__name__)

@app.route('/')
@app.route('/notes', methods=['GET'])
def get_notes():
    message = ""
    my_notes = notes.get_notes()
    return render_template("notes.html", message=message, notes=my_notes)

@app.route('/notes', methods=['POST'])
def post_notes():
    message = "Note = '" + request.form.get("note") + "'"
    note = request.form.get("note")
    if note != None and note != "":
        notes.add_note(str(note))
    my_notes = notes.get_notes()
    return render_template("notes.html", message=message, notes=my_notes)
