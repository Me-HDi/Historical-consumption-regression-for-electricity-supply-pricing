#!/usr/bin/env python
# coding: utf-8

# ### The useful function used to solve the prediction problem of the Data Challenge

# In[1]:


def timefeatures(df):
    ''' This function creates time features and add them to the DataFrame file'''
    
    df['hour'] = df.index.hour
    df['month'] = df.index.month
    df['year'] = df.index.year
    df['dayofmonth'] = df.index.day
    df['quarter'] = df.index.quarter
    df['weekofyear'] = df.index.weekofyear
    df['dayofweek'] = df.index.dayofweek

    return df

