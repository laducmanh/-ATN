import pandas as pd
import numpy as np
import joblib
import time

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from statsmodels.tsa.stattools import adfuller
from memory_profiler import profile

@profile

def  test():
	file_path = '/home/pi/Raspberry_Pi/Project/Weather_HCM.csv'
	data = pd.read_csv(file_path, sep=',',usecols=[0,1], header=0, skipinitialspace=True) 

	data.fillna(method = 'pad',  inplace=True)
	data.Date = pd.to_datetime(data.Date)
	data = data.set_index('Date')

	def test_stationarity(x):
		#Perform Dickey Fuller test    
		result=adfuller(x)
		print('ADF Stastistic: %f'%result[0])
		print('p-value: %f'%result[1])
		pvalue=result[1]
		for key,value in result[4].items():
			if result[0]>value:
				print("The graph is non stationery")
				break
			else:
				print("The graph is stationery")
				break
			
		print('Critical values:')
		for key,value in result[4].items():
			print('\t%s: %.3f ' % (key, value))

	ts = data['Temperature']   
	test_stationarity(ts)

	ts_log = np.log(ts)

	test_stationarity(ts_log)

	ts_log_diff = ts_log - ts_log.shift()

	ts_log_diff.dropna(inplace=True)
	test_stationarity(ts_log_diff)
	ts_log = ts_log_diff.cumsum() + ts_log.iloc[0]

	size = int(len(ts_log)*0.9)

	# Divide into train and test
	train_arima, test_arima = ts_log[0:size], ts_log[size:len(ts_log)]

	history = [x for x in train_arima]
	predictions = list()
	originals = list()
	error_list = list()

	start_time = time.time()

	for t in range(len(test_arima)):

	  model = ARIMA(history, order=(4, 1, 1))
	  model_fit = model.fit()

	  output = model_fit.forecast()
	  pred_value = output[0]   
		  
	  original_value = test_arima[t]
	  history.append(original_value)

	  pred_value = np.exp(pred_value)

	  original_value = np.exp(original_value)

	  # Calculating the error
	  error = ((abs(pred_value - original_value)) / original_value) * 100
	  error_list.append(error)

	  predictions.append(float(pred_value))
	  originals.append(float(original_value))

	elapsed_time = time.time() - start_time
	print("elapsed time: {:.2}".format(elapsed_time))
	print("elapsed time: {} seconds".format(elapsed_time))

	MAE = mean_absolute_error(predictions, originals) #MAE 
	rmse=np.sqrt(mean_squared_error(predictions,originals)) #rmse
	r2 = r2_score(originals, predictions) #r2

	print('Mean absolute error(MAE) ',MAE)
	print('Root-mean-square deviation(RMSE)', rmse)
	print("R-square:", r2)

test()
