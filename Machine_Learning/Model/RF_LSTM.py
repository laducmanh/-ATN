import pandas as pd
import numpy as np
import time
import joblib

from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, mean_absolute_percentage_error

def execute_predict():
    df = pd.read_csv('/home/pi/Raspberry_Pi/Project/Weather_HCM.csv')

    # Create a new dataframe with only the 'Close column 
    data = df.filter(['Temperature'])
    # Convert the dataframe to a numpy array
    dataset = data.values
    # Get the number of rows to train the model on
    #training_data_len = int(np.ceil( len(dataset) * .9 ))
    training_data_len = len(dataset) - 168

    # Scale the data
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(dataset)

    # Create the training data set 
    # Create the scaled training data set
    train_data = scaled_data[0:int(training_data_len), :]
    # Split the data into x_train and y_train data sets
    x_train = []
    y_train = []
    # 48, i<=49
    for i in range(48, len(train_data)):
        x_train.append(train_data[i-48:i, 0])
        y_train.append(train_data[i, 0])
        if i<= 49:
            print()
            
    # Convert the x_train and y_train to numpy arrays 
    x_train, y_train = np.array(x_train), np.array(y_train)

    # Reshape the data
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    test_data = scaled_data[training_data_len: , :] #48

    test_data = scaled_data[training_data_len - 48: , :]

    # Create the data sets x_test and y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(48, len(test_data)):
        x_test.append(test_data[i-48:i, 0])
        
    # Convert the data to a numpy array
    x_test = np.array(x_test)

    # Reshape the data
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

    x_train_rs= x_train.reshape(x_train.shape[0], (x_train.shape[1]*x_train.shape[2]))
    x_test_rs= x_test.reshape(x_test.shape[0], (x_test.shape[1]*x_test.shape[2]))

    #Load saved trained model
    model_rf = joblib.load('/home/pi/Raspberry_Pi/Project/RF.h5')
    model_lstm_2 = joblib.load('/home/pi/Raspberry_Pi/Project/RF_LSTM.h5')

    start_time = time.time()

    predictions_2 = model_lstm_2.predict(np.reshape(np.array((model_rf.predict(x_test_rs))),(-1,1))).squeeze()
    predictions_reshape_2 = np.reshape((predictions_2),(-1,1))
    predictions_2 = scaler.inverse_transform(predictions_reshape_2)

    elapsed_time = time.time() - start_time
    print("elapsed time: {:.2}".format(elapsed_time))
    print("elapsed time: {} seconds".format(elapsed_time))

    MAE = mean_absolute_error(y_test, predictions_2) #MAE 
    rmse=np.sqrt(mean_squared_error(y_test, predictions_2)) #rmse
    r2 = r2_score(y_test, predictions_2)

    print("MAE:",MAE)
    print("rmse:",rmse)
    print("r2:",r2)
    
    return predictions_2
