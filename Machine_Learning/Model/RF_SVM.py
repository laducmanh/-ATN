import pandas as pd
import numpy as np
import time
import joblib

from sklearn.feature_selection import SelectFromModel
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor
from keras.models import Sequential
from keras.layers import Dense, Dropout, LSTM
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error, mean_absolute_percentage_error

df = pd.read_csv('/home/pi/Raspberry_Pi/Project/Weather_HCM.csv')

# Create a new dataframe with only the 'Close column 
data = df.filter(['Temperature'])
# Convert the dataframe to a numpy array
dataset = data.values
# Get the number of rows to train the model on
training_data_len = int(np.ceil( len(dataset) * .9 ))

# Scale the data
scaler = MinMaxScaler(feature_range=(0,1))
scaled_data = scaler.fit_transform(dataset)

# Create a new dataframe with only the 'Close column 
data = df.filter(['Temperature'])
# Convert the dataframe to a numpy array
dataset = data.values
# Get the number of rows to train the model on
training_data_len = int(np.ceil( len(dataset) * .9 ))

# Create the training data set 
# Create the scaled training data set
train_data = scaled_data[0:int(training_data_len), :]
# Split the data into x_train and y_train data sets
x_train = []
y_train = []
# 60, i<=61
for i in range(60, len(train_data)):
    x_train.append(train_data[i-60:i, 0])
    y_train.append(train_data[i, 0])
    if i<= 61:
        # print(x_train)
        # print(y_train)
        print()
        
# Convert the x_train and y_train to numpy arrays 
x_train, y_train = np.array(x_train), np.array(y_train)

# Reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

test_data = scaled_data[training_data_len - 10: , :] #60

# Create the data sets x_test and y_test
# Create a new array containing scaled values from index 1543 to 2002 
test_data = scaled_data[training_data_len - 60: , :]

# Create the data sets x_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for i in range(60, len(test_data)):
    x_test.append(test_data[i-60:i, 0])
    
# Convert the data to a numpy array
x_test = np.array(x_test)

# Reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1 ))

x_train_rs= x_train.reshape(x_train.shape[0], (x_train.shape[1]*x_train.shape[2]))
x_test_rs= x_test.reshape(x_test.shape[0], (x_test.shape[1]*x_test.shape[2]))

#load saved trained model
model_rf = joblib.load('/home/pi/Raspberry_Pi/Project/RF.h5')
svm_model = joblib.load('/home/pi/Raspberry_Pi/Project/RF_SVM.h5')

feature_selector = SelectFromModel(model_rf, prefit=True)
X_train_selected = feature_selector.transform(x_train_rs)
X_test_selected = feature_selector.transform(x_test_rs)

start_time = time.time()

# make predictions on test data
predict_rf_svm = svm_model.predict(X_test_selected)
#print('y_pred: ', predict_rf_svm)
predict_rf_svm_reshape = np.reshape((predict_rf_svm),(-1,1))
predictions = scaler.inverse_transform(predict_rf_svm_reshape)

elapsed_time = time.time() - start_time
print("elapsed time: {:.2}".format(elapsed_time))
print("elapsed time: {} seconds".format(elapsed_time))

MAE = mean_absolute_error(y_test, predictions) #MAE 
rmse=np.sqrt(mean_squared_error(y_test, predictions)) #rmse
r2 = r2_score(y_test, predictions)

print("MAE:",MAE)
print("rmse:",rmse)
print("r2:",r2)
