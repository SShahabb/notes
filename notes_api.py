# notes
import os
import json
from tinydb import TinyDB, Query
import re

db = TinyDB("notes_tinydb.json")

#get list of notes
def get_notes(search=None):
    global db
    query = Query()
    if search:
        the_notes = db.search(query.text.matches(".*"+search+".*", flags=re.IGNORECASE))
    else:
        the_notes = db.all()
    the_notes = [n["text"] for n in the_notes]
    return the_notes

# add a note to the list of notes
def add_note(note):
    global db
    db.insert({"text":note})


