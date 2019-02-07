# notes
import os
import pickle

the_notes = []

#get list of notes
def get_notes():
    global the_notes
    if os.path.exists("notes.pkl"):
        with open("notes.pkl","rb") as f:
            the_notes = pickle.load(f)
    return the_notes

#add note to the list
def add_note(note):
    global the_notes
    if os.path.exists("notes.pkl"):
        with open("notes.pkl","rb") as f:
            the_notes = pickle.load(f)
    the_notes.append(note)
    with open("notes.pkl","wb") as f:
        pickle.dump(the_notes, f)
