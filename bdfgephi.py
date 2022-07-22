#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 23:59:13 2022

@author: xietianci
"""

import pandas as pd

df = pd.read_csv('/Users/xietianci/Desktop/webb.csv')

df['year_from'] = df['from'].apply(lambda x: str(x)[:4])
df['year_until'] = df['until'].apply(lambda x: str(x)[:4])
df = df.drop_duplicates(subset={'name','year_from'}).reset_index(drop=True)
df = df.sort_values(['name','year_from'])
df['year_until_lag1'] = df.groupby('name').shift(1)['year_until']

df['trans'] = (df['year_from']==df['year_until_lag1'])
df['trans'] = df['trans'].apply(str)
df['orgnization'] = df['orgnization'].apply(str).apply(lambda x : x.lower())

tran = []
for i in range(1,len(df)):
    if (df.iloc[i,-1] == 'True')\
        & (df['orgnization'][i].split(' ')[0] != df['orgnization'][i-1].split(' ')[0])\
        & (df['name'][i]==df['name'][i-1]):
        t = [df['orgnization'][i-1],df['orgnization'][i],df['year_from'][i]]
        tran.append(t)


gephi = pd.DataFrame(tran,columns = ['from','to','year'])
gephi['weight'] = [1]*len(gephi)
gephi.to_csv('/Users/xietianci/Desktop/gephi.csv')

