import pandas as pd
import numpy as np
import time
import joblib

from keras.models import Sequential
from keras.layers import Activation, Dense, Dropout, LSTM
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, mean_absolute_percentage_error
from memory_profiler import profile

@profile

def test():

	hist = pd.read_csv('/home/pi/Raspberry_Pi/Project/Weather_HCM.csv')
	hist.Date = pd.to_datetime(hist.Date)
	hist = hist.set_index('Date')
	target_col = 'Temperature'
	hist.fillna(method = 'pad',  inplace=True)
	hist = hist[["Temperature"]]

	def train_test_split(df, test_size=0.9):
		train_size = int(len(df) * test_size)
		train_data = df.iloc[:train_size]
		test_data = df.iloc[train_size:]
		return train_data, test_data

	train, test = train_test_split(hist, test_size=0.9)

	def normalise_zero_base(df):
		return df / df.iloc[0] - 1

	def extract_window_data(df, window_len=5, zero_base=True):
		window_data = []
		for idx in range(len(df) - window_len):
			tmp = df[idx: (idx + window_len)].copy()
			if zero_base:
				tmp = normalise_zero_base(tmp)
			window_data.append(tmp.values)
		return np.array(window_data)

	def prepare_data(df, target_col, window_len=5, zero_base=True, test_size=0.9):
		train_data, test_data = train_test_split(df, test_size=test_size)
		X_train = extract_window_data(train_data, window_len, zero_base)
		X_test = extract_window_data(test_data, window_len, zero_base)
		y_train = train_data[target_col][window_len:].values
		y_test = test_data[target_col][window_len:].values
		if zero_base:
			y_train = y_train / train_data[target_col][:-window_len].values - 1 
			y_test = y_test / test_data[target_col][:-window_len].values - 1

		return train_data, test_data, X_train, X_test, y_train, y_test

	def build_lstm_model(input_data, output_size, neurons=100, activ_func='tanh',
						 dropout=0.2, loss='mse', optimizer='adam'):
		model = Sequential()
		model.add(LSTM(neurons, input_shape=(input_data.shape[1], input_data.shape[2])))
		model.add(Dropout(dropout))
		model.add(Dense(units=output_size))
		model.add(Activation(activ_func))

		model.compile(loss=loss, optimizer=optimizer)
		return model 

	window_len = 5
	test_size = 0.9
	zero_base = True
	lstm_neurons = 128
	output_size = 1
	epochs = 50
	batch_size = 32
	loss = 'mse'
	dropout = 0.2
	optimizer = 'adam'

	train, test, X_train, X_test, y_train, y_test = prepare_data(hist, target_col, window_len=window_len, zero_base=zero_base, test_size=test_size)

	#load saved trained model
	model = joblib.load('/home/pi/Raspberry_Pi/Project/LSTM.h5')
	
	#Train model
	#model = build_lstm_model(X_train, output_size=output_size, neurons=lstm_neurons, dropout=dropout, loss=loss,optimizer=optimizer)
	#model.summary()
	#history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=batch_size, verbose=1, shuffle=True)

	targets = test[target_col][window_len:]

	start_time = time.time()

	preds = model.predict(X_test).squeeze()
	preds = test[target_col].values[:-window_len] * (preds + 1)
	prediction = preds

	elapsed_time = time.time() - start_time
	print("elapsed time: {:.2}".format(elapsed_time))
	print("elapsed time: {} seconds".format(elapsed_time)) 

	preds = pd.Series(index=targets.index, data=preds)

	MAE = mean_absolute_error(targets, preds) #MAE 
	rmse=np.sqrt(mean_squared_error(targets, preds)) #rmse
	r2 = r2_score(targets, preds) #r2

	print('Mean absolute error(MAE) ',MAE)
	print('Root-mean-square deviation(RMSE)', rmse)
	print("R-square:", r2)

test()
