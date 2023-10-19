# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 12:52:34 2022

@author: csukh
"""
import pandas as pd
import numpy as np
import networkx as nx

x = pd.read_csv('visa_matrix.csv')
x.fillna(1,inplace=True)

x.drop(['Unnamed: 0'],axis=1,inplace=True)
countries = x.columns.to_list()

y = x.to_numpy()

g = nx.from_numpy_array(y)
eig_scores = nx.eigenvector_centrality(g)

inds = np.argsort(list(eig_scores.values()))
evals = list(eig_scores.values())
#evals = [evals[ind] for ind in inds]

sorted_dict = {countries[ind]:evals[ind] for ind in inds} 

