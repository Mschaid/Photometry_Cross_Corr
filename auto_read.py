import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import os
import glob
import cross_correlation_setup as cc

path_to_files = "R:\Mike\JS_for_MS"


df_t = (df.transpose() #define df_t and transpose df
#         .reset_index()
#         )
# df_t = (df_t.assign(mouse = df_t['index'].str.split('_', expand=True)[0], #split index column string and assign to mouse and signal
#                     signal = df_t['index'].str.split('_', expand=True)[3])
#         .drop(['index'], axis=1) #drop index column from df
#         .melt(id_vars = ["mouse", "signal"],ignore_index=True) #reform dataframe to define variables
#         # .assign(time = df_t['variable'].transform(lambda x: x / 1.6E7)))
#     )
# print(df_t)
# # df_t.to_hdf(cross_correlation_analysis_path + "\\" + "cleaned_compiled_data.h5", key = "data", mode = 'w')
# print('Clean data saved as H5 file')
#
# # time = df_t['variable'].transform(lambda x: x / 1.6E7))