import datetime
import time
import csv
import variables

def put_data_exactly(now, temperature):
	date = now.strftime("%Y-%m-%d")
	
	get_time = datetime.datetime.now() - datetime.timedelta(hours=1)
	get_time = get_time.replace(minute=0)
	
	current_time = get_time.strftime('%H:%M')
	time = date + " " + current_time

	with open(variables.LINK, mode='a') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow([time, temperature])
		
def put_data_temporary(now, temperature):
	date = now.strftime("%Y-%m-%d")
	
	get_time = datetime.datetime.now()
	get_time = get_time.replace(minute=0)
	
	current_time = get_time.strftime('%H:%M')
	time = date + " " + current_time

	with open(variables.LINK, mode='a') as file:
		writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow([time, temperature])

def delete_last_row():
    with open(variables.LINK, 'r') as file:
        lines = list(csv.reader(file))
    
    if len(lines) > 0:
        lines.pop()

        with open(variables.LINK, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(lines)
