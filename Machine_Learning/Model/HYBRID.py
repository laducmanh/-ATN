import pandas as pd
import numpy as np
import time

from statsmodels.tsa.arima.model import ARIMA
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
from statsmodels.tsa.stattools import adfuller
from memory_profiler import profile

@profile

def test():
	# load dataset
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
				break;
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

	true_data = list()
	prediction_svm = list()

	start_time = time.time()
	for t in range(len(test_arima)):
		model = ARIMA(history, order=(3, 1, 0))
		model_fit = model.fit()
		
		#output will store the predicted value of the ARIMA model for the next data point in the time series
		output = model_fit.forecast()

		pred_value = output[0] 
		original_value = test_arima[t]

		#Residuals in AIRMA model
		residuals = model_fit.resid  #returns an array of model residuals
		residuals_svm = residuals[-1]

		#SVR predictions
		predicted_data_svm = np.arange(len(history),len(history)+1)
		predicted_data_svm= np.expand_dims(predicted_data_svm,axis=1)

		train_data = np.arange(0,len(residuals))
		train_data = np.expand_dims(train_data,axis=1)

		svr = SVR(kernel='rbf', C=3, gamma=1e-7 )
		yhat = svr.fit(train_data,residuals).predict(predicted_data_svm)

		true_data.append(residuals_svm)
		prediction_svm.append(yhat)  #code dư (chỉ dùng riêng cho SVM)

		pred_value = pred_value + yhat
		pred_value = pred_value

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
	r2 = r2_score(originals, predictions) # r2

	print('Mean absolute error(MAE) ',MAE)
	print('Root-mean-square deviation(RMSE)', rmse)
	print("R-square:", r2)

test()
