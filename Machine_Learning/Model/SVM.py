import numpy as np
import pandas as pd
import joblib
import time

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.svm import SVR
from memory_profiler import profile

@profile

def test():
	bc = pd.read_csv('/home/pi/Raspberry_Pi/Project/Weather_HCM.csv')
	bc.fillna(method = 'pad',  inplace=True)
	bc.Date = pd.to_datetime(bc.Date)
	bc = bc.set_index('Date')
	bc = bc['Temperature']

	size = int(len(bc)*0.90)

	# Divide into train and test
	train_svm, test_svm = bc[0:size], bc[size:len(bc)]

	history = [x for x in train_svm]
	predictions = list()
	originals = list()

	start_time = time.time()

	for t in range(len(test_svm)):

	  test_data = np.arange(len(history),len(history)+1)
	  test_data = np.expand_dims(test_data,axis=1)
	  train_data = np.arange(0,len(history))
	  train_data = np.expand_dims(train_data,axis=1)

	  svr = SVR(kernel='rbf', C=1e1, gamma = 5e-2)

	  model_fit = svr.fit(train_data, history)

	  yhat = model_fit.predict(test_data)

	  predictions.append(yhat)
	  obs = test_svm[t]
	  history.append(obs)

	elapsed_time = time.time() - start_time
	print("elapsed time: {:.2}".format(elapsed_time))
	print("elapsed time: {} seconds".format(elapsed_time))

	MAE = mean_absolute_error(predictions, test_svm) #MAE 
	rmse=np.sqrt(mean_squared_error(predictions,test_svm)) #rmse
	r2 = r2_score(test_svm, predictions) #r2

	print('Mean absolute error(MAE) ',MAE)
	print('Root-mean-square deviation(RMSE)', rmse)
	print("R-square:", r2)

test()
