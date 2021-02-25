#!/usr/bin/env python
# coding: utf-8

# In[1]:
#  The useful functions used to solve the prediction problem of the Data Challenge

import holidays

def timefeatures(df):
    ''' This function creates time features and add them to the DataFrame file'''
    
    df['hour'] = df.index.hour
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofmonth'] = df.index.day
    df['quarter'] = df.index.quarter
    df['weekofyear'] = df.index.weekofyear
    df['dayofweek'] = df.index.dayofweek


def isHoliday(df):
    fr_holidays = holidays.France()
    df['isHoliday'] = df.timestamp.apply(lambda x:1 if x in fr_holidays else 0)


def isWeekend(df):
    df['isWeekend'] = df['dayofweek'].apply(lambda x: 1 if x in [5,6] else 0)

