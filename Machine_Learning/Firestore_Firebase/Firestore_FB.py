import firebase_admin
import pandas as pd

from firebase_admin import credentials
from firebase_admin import firestore

def save_firestore(app):
    # Truy cập Firestore Database
    db = firestore.client(app=app)

    df = pd.read_csv('/home/pi/Raspberry_Pi/Project/Weather_HCM.csv')

    #push last data to firebase
    last_row = df.tail(1)
    last_date = last_row["Date"].values[0]
    last_temp = last_row["Temperature"].values[0]

    date_string, time_string = last_date.split(" ")

    doc_ref = db.collection('Database').document(date_string)

    doc_ref.set({
	time_string: last_temp
    }, merge=True)

