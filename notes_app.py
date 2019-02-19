from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import notes

app = Flask(__name__)

@app.route('/')
@app.route('/notes', methods=['GET'])
def get_notes():
    message = ""
    #my_notes = notes.get_notes()
    #return render_template("notes.html", message=message, notes=my_notes)
    return render_template("notes.html", message=message)

@app.route('/notes', methods=['POST'])
def post_notes():
    message = "Note = '" + request.form.get("note") + "'"
    note = request.form.get("note")
    if note != None and note != "":
        notes.add_note(str(note))
    #my_notes = notes.get_notes()
    #return render_template("notes.html", message=message, notes=my_notes)
    return render_template("notes.html", message=message)

@app.route("/content/<filter>")
def get_content(filter=None):
    items = notes.get_notes()
    items.append(filter)
    items = [item for item in items if filter in item]
    data = {"data": items}
    return jsonify(data)


