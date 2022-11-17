'''
    database.py
    teamlit
    This file handles everything related to getting and/or setting the names and scores stored with Firebase.
    The two functions it provides are addScore(String name, int score) and getTopScores()
'''

import sys
from google.auth.credentials import AnonymousCredentials
from google.cloud import firestore
from google.cloud.firestore import Client

from PyQt6.QtWidgets import QMessageBox

project_id = "teamlit-dd6f2"

credentials = AnonymousCredentials()
db = Client(project = project_id, credentials = credentials)

def addScore(name, score):
    # Create an entry in the players collection with this player's new ID
    try:
        id_ref = db.collection(u'ids').document(u'id')
        getID = id_ref.get()
    except:
        displayError()
        return
    newID = getID.to_dict().get(u'nextID')

    # Increment the nextID value in the ids collection id document
    try:
        id_ref.set({
            u'nextID': str((int(newID) + 1))
        })
    except:
        displayError()
        return
    
    # Create a newID document with a name of name and a score of score
    try:
        doc_ref = db.collection(u'scores').document(newID)
    except:
        displayError()
        return
    try:
        doc_ref.set({
            u'name': name,
            u'score': score
        })
    except:
        displayError()
        return

def getTopScores():
    try:
        scores_ref = db.collection(u'scores')
        query = scores_ref.order_by(u'score', direction=firestore.Query.DESCENDING).limit(10)
        docs = query.get()
    except:
        displayError()
        return None

    # Makes a string that contains the top ten list of scores with their players, separated by new lines
    topScores = ''
    for doc in docs:
        name = doc.to_dict().get(u'name')
        score = doc.to_dict().get(u'score')
        line = '{:<20} {:>10}'.format(name, str(score))
        topScores += line + '\n'

    return topScores

def displayError():
    errorMessage = QMessageBox()
    errorMessage.setStyleSheet("background-color: #293D48;"
                                "color: white;"
                                "min-width: 300 em;"
                                "padding: 10 px;")
    errorMessage.setWindowTitle('Error Message')
    errorMessage.setStandardButtons(QMessageBox.StandardButton.Ok)
    errorMessage.button(QMessageBox.StandardButton.Ok).setStyleSheet("background-color: lightGray;"
                                                                    "color: black;")
    errorMessage.setText("Error: Could not connect to score database.<br>Please try again later.")
    errorMessage.exec()

