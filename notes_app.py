from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

notes = []

@app.route('/')
@app.route('/notes', methods=['GET'])
def get_notes():
    global notes
    message = ""
    return render_template("notes.html", message=message, notes=notes)

@app.route('/notes', methods=['POST'])
def post_notes():
    global notes
    message = "Note = '" + request.form.get("note") + "'"
    note = request.form.get("note")
    if note != None and note != "" and not (note in notes):
        notes.append(note)
    return render_template("notes.html", message=message, notes=notes)
