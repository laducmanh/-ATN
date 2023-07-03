import datetime
import pandas as pd
import random
import csv

# Đường dẫn đến file chứa dữ liệu
data_file = '/home/pi/Desktop/data.txt'

start_date = datetime.datetime(2023, 5, 1, 0, 0)  # Ngày bắt đầu
time_step = datetime.timedelta(hours=1)  # Bước thời gian giữa các dữ liệu

# Mở file để đọc dữ liệu
with open(data_file, 'r') as file:
    lines = file.readlines()
    data = [line.strip().split() for line in lines]

# Chuyển đổi dữ liệu sang định dạng yêu cầu và lưu vào file mới
output_file = '/home/pi/Desktop/temp.csv'
with open(output_file, 'w') as file:
    writer = csv.writer(file)
    writer.writerow(['Date', 'Temperature'])
    current_date = start_date
    for values in data:
        for value in values:
            formatted_date = current_date.strftime('%Y-%m-%d %H:%M')
            line = f"{formatted_date},{value}\n"
            file.write(line)
            current_date += time_step

# Đọc file CSV vào DataFrame
#df = pd.read_csv(output_file)

# Tạo số thập phân ngẫu nhiên cho giá trị nhiệt độ
#df['Temperature'] = df['Temperature'].apply(lambda x: round(float(x) + random.uniform(0, 1), 6))

# Lưu kết quả vào file b.csv
#df.to_csv(output_file, sep=',', index=False, header=False)
