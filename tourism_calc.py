# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 13:43:31 2022

@author: csukh
"""

import numpy as np
import pandas as pd


visits = pd.read_csv('most_visited.csv')
total_tourism = np.sum(visits['touristArrivals'])

visits['touristArrivalsWeighted'] = 1000*visits['touristArrivals']/total_tourism
top_visited = visits['country'].to_list()
visits.index = visits['country']
visits.drop(['country'],axis=1,inplace=True)


x = pd.read_csv('visa_matrix_updated.csv')
x.drop(['Unnamed: 0'],axis=1,inplace=True)
x.fillna(1,inplace=True)
x = x/10

countries = x.columns.to_list()

x.index = countries

for ctry in countries:
    for tv in top_visited:
        try:
            if x[ctry][tv] > 0:
                x[ctry][tv] = visits['touristArrivalsWeighted'][tv]
        except:
            print(tv)

x.index = [i for i in range(len(x))]
df2 = x.sum(axis=0)

df2.index = countries
df2.sort_values(ascending=False,inplace=True)