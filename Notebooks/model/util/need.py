#!/usr/bin/env python
# coding: utf-8

# In[1]:
#  The useful functions used to solve the prediction problem of the Data Challenge

import holidays


def time_features(df):

    ''' This function create time features and add them to the DataFrame'''

    df['hour'] = df.index.hour
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['day_of_month'] = df.index.day
    df['quarter'] = df.index.quarter
    df['week_of_year'] = df.index.weekofyear
    df['dayofweek'] = df.index.dayofweek


def is_holiday(df):
    ''' This function create holiday features and add them to the DataFrame.
    if the input is a holiday day it returns 1 else it returns 0'''

    fr_holidays = holidays.France()
    df['isHoliday'] = df.timestamp.apply(lambda x:1 if x in fr_holidays else 0)


def is_weekend(df):
    
    ''' This function create weekend features and add them to the DataFrame.
        if the input is a weekend day it returns 1 else it returns 0'''

    df['isWeekend'] = df['dayofweek'].apply(lambda x: 1 if x in [5, 6] else 0)

