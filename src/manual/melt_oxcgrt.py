#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 14:09:09 2020

@author: hamishgibbs
"""
import pandas as pd
import re
import numpy as np
#%%

ox = pd.read_csv('https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/OxCGRT_latest_withnotes.csv')

#%%

def melt_oxcgrt(ox, drop_columns = [], sep = 'XXXXX', quick = False, quiet = True):
    
    keep_columns = list(set(ox.columns).difference(set(drop_columns)))
    
    ox = ox[keep_columns]
    
    full_value_names, value_names, stub_names = get_names(ox)
    
    id_columns = list(set(ox.columns).difference(set(full_value_names)))
            
    #only use first columns for a quick run
    if quick:
        
        value_names = value_names[0:2]
        stub_names = stub_names[0:2]
    
    for i, k in enumerate(value_names):
        value_name = value_names[i]
        stub = stub_names[i]
        
        stub_cols = [x for x in ox.columns if stub in x]
        
        ox[stub] = ox.apply(lambda x: value_name + sep + sep.join([str(s) for s in x[stub_cols]]), axis=1)
        
        if not quiet:
            
            print(stub)
    
    ox_melted = pd.melt(ox[id_columns + stub_names], id_columns, stub_names)
    
    ox_expand = ox_melted['value'].str.split(sep, expand=True)
    
    ox_expand.columns = ['measure', 'value', 'flag', 'notes']
    
    ox_expand[id_columns] = ox_melted[id_columns]
    
    return(ox_expand)

def get_names(ox):

    stub_exp = r'[A-Z][0-9]+_'

    full_value_names = [match for match in ox.columns if re.findall(stub_exp , match) != []]

    value_names = [x for x in full_value_names  if 'Flag' not in x]
    value_names = [x for x in value_names if 'Notes' not in x]

    stub_names = [x.split('_')[0] for x in value_names]
    
    return(full_value_names, value_names, stub_names)
    
#%%
drop_columns = ['ConfirmedCases',
       'ConfirmedDeaths', 'StringencyIndex', 'StringencyIndexForDisplay',
       'StringencyLegacyIndex', 'StringencyLegacyIndexForDisplay',
       'GovernmentResponseIndex', 'GovernmentResponseIndexForDisplay',
       'ContainmentHealthIndex', 'ContainmentHealthIndexForDisplay',
       'EconomicSupportIndex', 'EconomicSupportIndexForDisplay']
#%%
ox_melted = melt_oxcgrt(ox, drop_columns, quick = True, quiet = False)
#%%
sep = 'XXXXX'

for i, k in enumerate(value_names[0:2]):
    value_name = value_names[i]
    stub = stub_names[i]
    
    stub_cols = [x for x in ox.columns if stub in x]
    
    ox[stub] = ox.apply(lambda x: value_name + sep + sep.join([str(s) for s in x[stub_cols]]), axis=1)
    print(i)
#%%
ox_melted = pd.melt(ox[['Date'] + stub_names[0:2]], 'Date', stub_names[0:2])
#%%
v = ox_melted['value'].str.split(sep, expand=True)
v.columns = ['measure', 'value', 'flag', 'notes']
v['Date'] = ox_melted['Date']