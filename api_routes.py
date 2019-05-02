#
# API ROUTES
#

from flask import redirect, jsonify

import storage

from main import app
from main import verify_login

@app.route("/content/")
@app.route("/content/<search>")
def get_content(search=None):
    response = verify_login(request)
    if response:
        return response
    items = storage.get_notes(search)
    data = { "data": items }
    return jsonify(data)

@app.route("/remove/<int:id>")
def get_remove(id):
    response = verify_login(request)
    if response:
        return response
    storage.delete_note(id)
    return redirect("/notes")
