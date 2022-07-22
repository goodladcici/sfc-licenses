#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 10:46:14 2022

@author: xietianci
"""

import pandas as pd

df = pd.read_csv('/Users/xietianci/Desktop/webb.csv')


def advising(x):
    a = 'other'
    if x.startswith('Advising'):
        a = 'advising'
    return a

df['join_year'] = df['from'].apply(lambda x: str(x)[:4])
df['advising_or_not'] = df['activity'].apply(advising)

dff = df[df['advising_or_not']=='advising'].copy().fillna({'until':'2023/1/1'})
dff = dff[dff['until']=='2023/1/1'].drop_duplicates(subset = {'name'})
dff = dff.groupby('orgnization')['name'].count().reset_index()
dff = dff.sort_values('name',ascending=False).reset_index(drop=True)
dff.iloc[0,0]='CICCHK SERCURITIES LIMITED'
dff.iloc[:10].plot(x='orgnization',y='name',kind = 'bar',figsize=[10,2])



df = df.drop_duplicates(subset=['name','join_year'])
dfg = df.groupby(['join_year','advising_or_not']).apply(lambda x:len(x))
dfg = dfg.drop('nan',axis=0)
dfg = dfg.reset_index()
dfg = dfg.drop(0,axis=0)
dfg = dfg.rename(columns = {0:'num'})

dfgm = pd.merge(dfg[dfg['advising_or_not']=='advising']\
                ,dfg[dfg['advising_or_not']=='other']\
                    ,on='join_year',how='inner',suffixes=['_adv','_other'])
dfgm['total_num'] = dfgm['num_adv']+dfgm['num_other']
dfgm['ratio'] = dfgm['num_adv']/dfgm['total_num']
hs = [14230.14,14876.43,19964.72,27812.65,14387.48,21872.5,23035.45,18434.39
      ,22656.92,23306.39,23605.04,21914.4,22000.56,29919.15,25845.7,28189.75
      ,27231.13,23397.67,20832.94]
dfgm['hsi'] = hs
dfgm.assign(date = dfgm['join_year'].apply(lambda x:pd.to_datetime(x)))\
            .plot(x='date',y=['num_adv','total_num','hsi'],figsize = [10,2])

dfgm.assign(date = dfgm['join_year'].apply(lambda x:pd.to_datetime(x)))\
            .plot(x='date',y='ratio',figsize = [10,1])


    


df1 = df[df['advising_or_not']=='advising'].copy()
df1['orgnization_lower'] = df1['orgnization'].apply(lambda x: x.lower())
df1['join_year'] = df1['from'].apply(lambda x: str(x)[:4])

def chinese(x):
    for ch in x:
        a = 'without_chinese'
        if u'\u4e00' <= ch <= u'\u9fff':
            a = 'with_chinese'
            break
    return a
df1['chinese'] = df1['name'].apply(chinese)
df1 = df1.drop_duplicates(subset=['name','join_year'])
df1g = df1.groupby(['join_year','chinese']).apply(lambda x:len(x))
df1g = df1g.drop('nan',axis=0)
df1g = df1g.reset_index()
df1g = df1g.rename(columns = {0:'num'})

df1gm = pd.merge(df1g[df1g['chinese']=='with_chinese']\
                ,df1g[df1g['chinese']=='without_chinese']\
                    ,on='join_year',how='inner',suffixes=['_chinese','_other'])
df1gm['num_total'] = df1gm['num_chinese'] + df1gm['num_other'] 
df1gm['ratio'] = df1gm['num_chinese']/df1gm['num_total'] 

df1gm.assign(date = df1gm['join_year'].apply(lambda x:pd.to_datetime(x)))\
            .plot(x='date',y=['num_chinese','num_total'],figsize = [10,3])
df1gm.assign(date = df1gm['join_year'].apply(lambda x:pd.to_datetime(x)))\
            .plot(x='date',y='ratio',figsize = [10,1])





df2 = pd.read_csv('/Users/xietianci/Desktop/gephi.csv')
df2['join_year'] = df2['year'].apply(lambda x: str(x)[:4])
df2g = df2.groupby('year').apply(lambda x:len(x)).reset_index().rename(columns={0:'num'})
df2g['year'] = df2g['year'].apply(int).apply(str)
df2g.plot(x = 'year',y = 'num',figsize=[10,2])

















