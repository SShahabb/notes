# note

import os
import json
import re
from tinydb import TinyDB, Query

notes_db = TinyDB("notes_tinydb.json")
profiles_db = TinyDB("notes_tinydb.json")

def get_profiles(search=None):
    global profiles_db
    query = Query()
    if search:
        the_profiles = profiles_db.search(query.user.matches(".*"+search+".*", flags=re.IGNORECASE))
    else:
        the_profiles = profiles_db.all()
    print(the_profiles)
    for n in the_profiles:
        n['id'] = n.doc_id
    return the_profiles

def add_profile(profile):
    global profiles_db
    assert type(profile) is dict
    assert 'user' in profile
    assert type(profile['user']) is str
    id = profiles_db.insert(profile)
    return id

def delete_profile(id):
    global profiles_db
    try:
        profiles_db.remove(doc_ids = [id])
    except KeyError:
        pass

#get the list of notes
def get_notes(search=None):
    global notes_db
    query = Query()
    if search:
        the_notes = notes_db.search(query.text.matches(".*"+search+".*", flags=re.IGNORECASE))
    else:
        the_notes = notes_db.all()
    print(the_notes)
    for n in the_notes:
        n['id'] = n.doc_id
    return the_notes

# add a note to the list of notes
def add_note(note):
    global notes_db
    id = notes_db.insert({"text":note})
    return id

def delete_note(id):
    global notes_db
    try:
        notes_db.remove(doc_ids = [id])
    except KeyError:
        pass
        