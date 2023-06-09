# -*- coding: utf-8 -*-
"""Bostonhousepricepredictor.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1cOD4S-ycMldtunuJ7kbZvFTjSA9Flar6
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
# %matplotlib inline
warnings.filterwarnings('ignore')
import io

from google.colab import files
uploaded=files.upload()

df = pd.read_csv(io.BytesIO(uploaded['BostonDataset.csv']))
print(df)

df.head()

df.describe()

df.info()

#check null values
df.isnull().sum()

#create dist plots
fig, ax= plt.subplots(ncols=7, nrows=2, figsize=(20, 10))
index=0
ax= ax.flatten()

for col,value in df.items():
  sns.distplot(value,ax=ax[index-1])
  index += 1
plt.tight_layout(pad=0.5, w_pad=0.7, h_pad=5.0)

#min-max normalization
cols = ['crim','zn','tax','black']
for col in cols:
  #find min-max of each column
  minimum = min(df[col])
  maximum = max(df[col])
  df[col] = (df[col]- minimum)/ (maximum-minimum)

#create dist plots
fig, ax= plt.subplots(ncols=7, nrows=2, figsize=(20, 10))
index=0
ax= ax.flatten()

for col,value in df.items():
  sns.distplot(value,ax=ax[index-1])
  index += 1
plt.tight_layout(pad=0.5, w_pad=0.7, h_pad=5.0)

#standardization
from sklearn import preprocessing
scalar = preprocessing.StandardScaler()

#FIT THE DATA
scaled_cols = scalar.fit_transform(df[cols])
scaled_cols = pd.DataFrame(scaled_cols, columns=cols)
scaled_cols.head()

for col in cols:
  df[col] = scaled_cols[col]

#create dist plots
fig, ax= plt.subplots(ncols=7, nrows=2, figsize=(20, 10))
index=0
ax= ax.flatten()

for col,value in df.items():
  sns.distplot(value,ax=ax[index-1])
  index += 1
plt.tight_layout(pad=0.5, w_pad=0.7, h_pad=5.0)

corr = df.corr()
plt.figure(figsize=(20,10))
sns.heatmap(corr, annot=True, cmap='coolwarm')

sns.regplot(y=df['medv'], x=df['lstat'])

sns.regplot(y=df['medv'], x=df['rm'])

#input split
X = df.drop(columns=['medv','rad'], axis=1)
y= df['medv']

#model train
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import mean_squared_error
def train(model, X, y):
    #train model
    x_train, x_test, y_train, y_test = train_test_split(X, y, random_state=42)
    model.fit(x_train,y_train)
    model.fit(X,y)

    #predict training set
    pred = model.predict(x_test)

    #perform cross validation
    cv_score = cross_val_score(model, X, y, scoring='neg_mean_squared_error', cv=5)
    cv_score = np.abs(np.mean(cv_score))

    print("Model Report")
    print("MSE:", mean_squared_error(y_test, pred))
    print('CV Score:', cv_score)

from sklearn.linear_model import LinearRegression
model=LinearRegression()
train(model,X,y)
coef=pd.Series(model.coef_,X.columns).sort_values()
coef.plot(kind='bar',title='Model Coefficients')

from sklearn.tree import DecisionTreeRegressor
model = DecisionTreeRegressor()
train(model,X,y)
coef = pd.Series(model.feature_importances_,X.columns).sort_values(ascending=False)
coef.plot(kind='bar',title='Feature Importance')

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor()
train(model,X,y)
coef = pd.Series(model.feature_importances_,X.columns).sort_values(ascending=False)
coef.plot(kind='bar',title='Feature Importance')

from sklearn.ensemble import ExtraTreesRegressor
model = ExtraTreesRegressor()
train(model,X,y)
coef = pd.Series(model.feature_importances_,X.columns).sort_values(ascending=False)
coef.plot(kind='bar',title='Feature Importance')

import xgboost as xgb
model = xgb.XGBRegressor()
train(model,X,y)
coef = pd.Series(model.feature_importances_,X.columns).sort_values(ascending=False)
coef.plot(kind='bar',title='Feature Importance')