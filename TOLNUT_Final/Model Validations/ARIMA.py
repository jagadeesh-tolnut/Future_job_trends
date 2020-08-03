import pandas as pd
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
from PyQt5 import


df = pd.read_csv('Synthetic_data_1.csv')
train_size = int(df.shape[0]*0.8)
train, test = df.jobs[0:train_size], df.jobs[train_size:]

data = train
predict = []
for t in test:
    model = ARIMA(data,order=(2,1,2))
    model_fit = model.fit()
    y = model_fit.forecast()
    print(y[0][0])
    predict.append(y[0][0])
    data = np.append(data, t)
    data = pd.Series(data)

print("##############################################################\n##############################################################\n##############################################################\n##############################################################\n##############################################################\n##############################################################\n##############################################################\n##############################################################\n##############################################################\n##############################################################\n##############################################################\n")

from sklearn.metrics import mean_squared_error
mse = mean_squared_error(test.values, predict)

print(mse)
