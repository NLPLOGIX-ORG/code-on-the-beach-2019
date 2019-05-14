# -*- coding: utf-8 -*-
"""
Created on Mon May 13 08:36:23 2019

@author: kbakewell
"""


from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics
from sklearn.utils import resample 
import pandas as pd
import numpy as np
import os, random
import matplotlib.pyplot as plt
from sklearn.tree import export_graphviz
import pickle 

#set hardcoded file paths -- Sorry Toooooooom 
data = "E:\MyWork\Property Tax Roll"
model = "E:\MyWork\Property Tax Roll"

#load Data
fpath = os.path.join(data, "casetable.psv")
df = pd.read_csv(fpath, sep = "|")

plt.hist(df['Assessed Value'], normed=True, bins=30)
plt.ylabel('AssessedValue')

df.columns.values
plt.hist(df['Number Of Bedrooms'], normed=True, bins=30)
plt.ylabel('Number Of Bedrooms')

df = df[df['Assessed Value']<1000000]
df = df[df['Number Of Bedrooms']<10]


df.fillna(-999,inplace = True)

features.columns.values

features = df.copy()
features.drop(['Parcel Number','Section','Township','Total Market Value',
               'Assessed Value','Total Just Value', 'Site Address Number',
               'Site Address Street Name','Site Address Street Type',
               'Site Address Unit Number','Site Address City','Building Number',
               'Exemption Code', 'Date of Sale', 'Sale Price','Site Zip Code',
               'Amenity Item Code', "building value"], axis = 1, 
                inplace = True)

y_val = df['Assessed Value'].copy()


def split(df, pct=.7):
    tr, xv = [], []
     
    indices = [x for x in df.index]
    random.shuffle(indices)
 
    for ind in indices:
        if np.random.rand() <= pct:
            tr.append(ind)
        else:
            xv.append(ind)
 
    return tr, xv

tr_indices, xv_indices = split(df)




features_tr = features.ix[tr_indices]
features_xval = features.ix[xv_indices]
y_tr = y_val.ix[tr_indices]
y_xval = y_val.ix[xv_indices]

#create split function
random.seed(19860406)
np.random.seed(19860406)


rfc = RandomForestRegressor(
        max_depth = 5, 
        n_estimators = 25, 
        min_samples_leaf = 15)


rfc.fit(features_tr, y_tr.values.ravel())




tr_yhat2 = rfc.predict(features_tr)
xval_yhat2 = rfc.predict(features_xval)

tr_MSE = metrics.mean_squared_error(y_tr, tr_yhat2)
print(tr_MSE)

print(tr_MSE**.5)
xval_MSE = metrics.mean_squared_error(y_xval, xval_yhat2)
print(xval_MSE)
print(xval_MSE**.5)



features.head()
features.columns.values

np.mean(features)

features.dtypes

df_fits =  pd.DataFrame(rfc.predict(features))
df_full = pd.concat([df, df_fits], axis = 1)

df_full