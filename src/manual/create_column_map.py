#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:58:46 2020

@author: hamishgibbs
"""

import json

import pandas as pd

column_map = pd.read_csv(
    "/Users/hamishgibbs/Documents/Covid-19/WHO_Interventions/WHO_Intervention_Cleaning/cleaning_utility_data/dataset_dictionary.csv"
)

column_map.columns

datasets = column_map["dataset"].unique()

res = {}
for dataset in datasets:

    res[dataset] = []

    for index, row in column_map.loc[column_map["dataset"] == dataset, :].iterrows():

        if pd.isna(row["who_variable"]):
            row["who_variable"] = ""

        res[dataset].append(
            {"orig_col": row["input_variable"], "new_col": row["who_variable"]}
        )


#%%
file = {
    "description": "Mapping of columns from provider datasets to who column names",
    "date_updated": None,
    "data": res,
}

with open(
    "/Users/hamishgibbs/Documents/Covid-19/WHO_PHSM_Cleaning/config/column_map.json",
    "w",
) as outfile:
    json.dump(file, outfile)
