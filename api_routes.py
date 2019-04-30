#
# API ROUTES
#

from flask import redirect, jsonify

import storage

from main import app

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
