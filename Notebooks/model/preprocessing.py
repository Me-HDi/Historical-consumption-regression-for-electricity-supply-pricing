#!/usr/bin/env python
# coding: utf-8

# # Data Challenge : Historical consumption regression for electricity supply pricing

## This model helps the pre-processing automation of our data set. 
## It includes all the funtion needed for dealing with missing values, adding features, normalisation and handling data type.


# # # Importings

from datetime import datetime
from .util import need
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


# See the other notebook for data preprocessing details and visualisation

# In[2]:

class Data: 	

    ''' The aim of this class is to help applying different preprocessing function to our dataset.
	we begin by cleaning our data set by removing useless features then we add more features. The last two methods splits 
	the data of the two sites.'''


    def __init__(self, data_train, data_test, y_data):
        self.data_train = data_train
        self.data_test = data_test
        self.y_data = y_data
	
	
    
    def data_preprocessing(self):
        
        
        #Remove useless features
        self.data_train = self.data_train.drop(["loc_1",
                                      "loc_2",
                                      "loc_secondary_1",
                                      "loc_secondary_2",
                                      "loc_secondary_3"],
                                     axis = 1)
        self.data_test = self.data_test.drop(["loc_1", 
                                    "loc_2",
                                    "loc_secondary_1",
                                    "loc_secondary_2", 
                                    "loc_secondary_3"],
                                   axis = 1)
        # add is holiday feature
        need.isHoliday(self.data_train)
        need.isHoliday(self.data_test)

        # convert timestamp to index
        self.data_train.timestamp = pd.to_datetime(self.data_train.timestamp)
        self.data_test.timestamp = pd.to_datetime(self.data_test.timestamp)

        # indexing with timestamp
        self.data_test = self.data_test.set_index('timestamp')
        self.data_train = self.data_train.set_index('timestamp')

        # add time features
        need.timefeatures(self.data_train)
        need.timefeatures(self.data_test)

        # add is weekend feature
        need.isWeekend(self.data_train)
        need.isWeekend(self.data_test)
	
        ## add smoothing temp and humidity
        self.data_train['temp_1_smooth7D'] = self.data_train['temp_1'].interpolate().rolling(24*7).mean().fillna(method='bfill').round(decimals=1)
        self.data_train['temp_2_smooth7D'] = self.data_train['temp_2'].interpolate().rolling(24*7).mean().fillna(method='bfill').round(decimals=1)
        self.data_test['temp_1_smooth7D'] = self.data_test['temp_1'].interpolate().rolling(24*7).mean().fillna(method='bfill').round(decimals=1)
        self.data_test['temp_2_smooth7D'] = self.data_test['temp_2'].interpolate().rolling(24*7).mean().fillna(method='bfill').round(decimals=1)

        self.data_train['humidity_1_smooth7D'] = self.data_train['humidity_1'].interpolate().rolling(24*7).mean().fillna(method='bfill').round()
        self.data_train['humidity_2_smooth7D'] = self.data_train['humidity_2'].interpolate().rolling(24*7).mean().fillna(method='bfill').round()
        self.data_test['humidity_1_smooth7D'] = self.data_test['humidity_1'].interpolate().rolling(24*7).mean().fillna(method='bfill').round()
        self.data_test['humidity_2_smooth7D'] = self.data_test['humidity_2'].interpolate().rolling(24*7).mean().fillna(method='bfill').round()

        ## Normalising and inetrpolating features with missing data
        scaler = MinMaxScaler()
        self.data_train[['temp_1', 'temp_2', 
                 'mean_national_temp',
                 'humidity_1', 'humidity_2',
                 'consumption_secondary_1',
                 'consumption_secondary_2',
                 'consumption_secondary_3', 
                 'temp_1_smooth7D',
                 'temp_2_smooth7D', 
                 'humidity_1_smooth7D',
                'humidity_2_smooth7D']] = scaler.fit_transform(self.data_train[['temp_1', 'temp_2',
                                                                               'mean_national_temp', 
                                                                               'humidity_1', 'humidity_2',
                                                                               'consumption_secondary_1', 
                                                                               'consumption_secondary_2',
                                                                               'consumption_secondary_3', 
                                                                               'temp_1_smooth7D',
                                                                               'temp_2_smooth7D',
                                                                               'humidity_1_smooth7D',
                                                                               'humidity_2_smooth7D']])
        self.data_train=self.data_train.interpolate()
        self.data_test[['temp_1', 'temp_2', 
                 'mean_national_temp',
                 'humidity_1', 'humidity_2',
                 'consumption_secondary_1',
                 'consumption_secondary_2',
                 'consumption_secondary_3', 
                 'temp_1_smooth7D',
                 'temp_2_smooth7D', 
                 'humidity_1_smooth7D',
                'humidity_2_smooth7D']] = scaler.fit_transform(self.data_test[['temp_1', 'temp_2',
                                                                               'mean_national_temp', 
                                                                               'humidity_1', 'humidity_2',
                                                                               'consumption_secondary_1', 
                                                                               'consumption_secondary_2',
                                                                               'consumption_secondary_3', 
                                                                               'temp_1_smooth7D',
                                                                               'temp_2_smooth7D',
                                                                               'humidity_1_smooth7D',
                                                                               'humidity_2_smooth7D']])
        self.data_test=self.data_test.interpolate()

    	
	
    ## defining our train and test data
    def get_data_split(self):
        # split data train and test of the two sites 
        X_train1 = self.data_train.drop(['temp_2',
					'humidity_2',
					'temp_2_smooth7D',
                            		'humidity_2_smooth7D'], axis=1)

        X_train2 = self.data_train.drop(['temp_1',
					'humidity_1',
					'temp_1_smooth7D',
					'humidity_1_smooth7D'], axis=1)
        
        X_test1 = self.data_test.drop(['temp_2',
					'humidity_2',
					'temp_2_smooth7D',
					'humidity_2_smooth7D'], axis=1)

        X_test2 = self.data_test.drop(['temp_1',
					'humidity_1',
					'temp_1_smooth7D',
					'humidity_1_smooth7D'], axis=1)

        return X_train1,X_train2,X_test1,X_test2
    
    
    def get_split_y_data(self):
	# split the data target of the two sites 
        self.y_data=self.y_data.set_index(self.data_train.index)

        y_train1 = self.y_data['consumption_1']
        y_train2 = self.y_data['consumption_2']
        
        return y_train1,y_train2
    
        

