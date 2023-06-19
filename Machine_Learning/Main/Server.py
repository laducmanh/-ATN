import socket
import threading
import datetime
import firebase_admin
import CSV
import RF_LSTM
import Realtime_FB
import Firestore_FB

from firebase_admin import credentials

cred = credentials.Certificate('/home/pi/Raspberry_Pi/Project/raspberry-esp32-firebase-adminsdk-dd5v3-8b0d728a1f.json')
app = firebase_admin.initialize_app(cred, {
	'databaseURL': 'https://raspberry-esp32-default-rtdb.asia-southeast1.firebasedatabase.app'
	})

HOST = '192.168.1.123'
PORT = 8888    
BUFFER_SIZE = 1024

def handle_client(conn, addr):
	count = 0
	atleast_received = False
	temperature_child = 0
	
	now = datetime.datetime.now()
	next_hour = now + datetime.timedelta(hours=1)
	check_time = 0
	
	with conn:
		print(f"Connected by {addr}")
		
		while True:
			data = conn.recv(BUFFER_SIZE).decode()
			
			if not data:
				break
				
			values = data.split("|")
			
			if len(values) != 2: 
				continue
				
			temperature_received, humidity_received = values
			print(f"Temperature: {temperature_received}, Humidity: {humidity_received}")
			
			now = datetime.datetime.now()
			print('Now1: ', now)
			
			if(now.hour == 0):
				check_time = 1
			
			if now.hour < next_hour.hour or check_time == 0:
				Realtime_FB.push_actual(app, temperature_received)
				
				temperature_child += float(temperature_received)
				
				if(atleast_received == True):
					CSV.delete_last_row()
				
				CSV.put_data_temporary(now, temperature_received)
				
				predict_value = RF_LSTM.execute_predict()
				
				Realtime_FB.push_preddict(app, predict_value)
				
				count += 1
				atleast_received = True
			else:
				if(atleast_received == False):
					next_hour += datetime.timedelta(hours=1)
					continue
					
				temperature = temperature_child/count
				temperature_child = 0
				count = 0
				
				CSV.delete_last_row()
				
				CSV.put_data_exactly(now, temperature)
					
				Firestore_FB.save_firestore(app)
				
				predict_value = RF_LSTM.execute_predict()
				
				Realtime_FB.push_preddict(app, predict_value)
				
				next_hour += datetime.timedelta(hours=1)
				
				if(next_hour.hour == 0):
					check_time = 0
				
				atleast_received = False
            
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
	s.bind((HOST, PORT))
	s.listen()
	
	print(f"Listening on {HOST}:{PORT}...")
	
	while True:
		conn, addr = s.accept()
		thread = threading.Thread(target=handle_client, args=(conn, addr))
		thread.start()
