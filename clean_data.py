import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import os
import glob
import cross_correlation_setup as cc
from read_and_compile_traces import compiled_data_path

#%% read data
df_clean = (pd.read_hdf(compiled_data_path)
            .transpose()
            .reset_index()
            .rename(columns={"index": 'name'})
            .melt(id_vars = ["name"],ignore_index=False)
            .dropna()
                )
#  for some reason I need to assign columns after closing the previous function chain. it won't work otherwise
df_clean = (df_clean.assign(time = df_clean['variable'].div(1.071E3),
                mouse = df_clean['name'].str.split('_', expand=True)[0], #split index column string and assign to mouse and signal
                signal = df_clean['name'].str.split('_', expand=True)[3])
            .drop(columns = ['name', 'variable'])
         )
## TODO make this faster
print(df_clean)
print("data reformatted and cleaned")


# # df_clean.to_hdf(cross_correlation_analysis_path + "\\" + "cleaned_compiled_data.h5", key = "data", mode = 'w')
# print('Clean data saved as H5 file')
#
# # time = df_clean['variable'].transform(lambda x: x / 1.6E7))