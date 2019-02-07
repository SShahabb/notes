# notes
import os
import json
#import pickle

the_notes = []

#get list of notes
def get_notes():
    global the_notes
    if os.path.exists("notes.json"):
        with open("notes.json","r") as f:
            the_notes = json.load(f)
    return the_notes

#add note to the list
def add_note(note):
    global the_notes
    if os.path.exists("notes.json"):
        with open("notes.json","r") as f:
            the_notes = json.load(f)
    the_notes.append(note)
    with open("notes.json","w") as f:
        json.dump(the_notes, f)
