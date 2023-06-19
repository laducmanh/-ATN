import firebase_admin
import datetime
import time
import pandas as pd

from firebase_admin import credentials
from firebase_admin import db

def push_actual(app, temperature):
    new_data = {
    'Temperature': float(temperature)
    }

    ref = db.reference('Actual', app=app)
    ref.update(new_data)

def push_preddict(app, prediction_2):
    current_time = datetime.datetime.now()
    current_date = current_time.date()
    current_hour = current_time.hour
    
    ref = db.reference('Predict', app=app)
    existing_data = ref.get()  # Lấy dữ liệu hiện có trên Firebase
    new_data = {}

    for i in range(1, len(prediction_2)):
        next_time = current_time.replace(minute=0) + datetime.timedelta(hours=i)

	
        if next_time.date() != current_date:
            current_date = next_time.date()
            formatted_time = next_time.strftime('%Y-%m-%d %H:%M')
        else:
            formatted_time = next_time.strftime('%Y-%m-%d %H:%M')
	    
        new_data[formatted_time] = float(prediction_2[i])
	    
    if existing_data:
        for key in existing_data.keys():
            if key not in new_data:
                ref.child(key).delete()

    ref.update(new_data)
	
