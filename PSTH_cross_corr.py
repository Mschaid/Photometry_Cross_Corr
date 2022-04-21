import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
import os
import glob
import cross_correlation_setup as cc
import fnmatch
import functools
import operator
import itertools
from scipy import signal
import sys


path_to_folders = r'C:\Users\mds8301\Desktop\PSTH_corr_test'

## search path for guppy outputs
sub_folders = glob.glob(path_to_folders + '\\**\\*output_*', recursive=True)

## create new file called cross corelation analysis
new_folder = "cross_correlation_analysis"

## create new folder in each output folder called 'cross_correlation_analyis - indiv analysis will be stored here
for i in sub_folders:
    cc.new_folder(path=i, name=new_folder)

#  give signal input files for Signal A vs Signal B
signal_A = 'cue_NAC_z_score_NAC.h5'
signal_B = 'cue_LH_z_score_LH.h5'

# set parameters to filter around time 0
filter_ts_low = -3
filter_ts_high = 3

## in each ouput get cue z_score
for i in sub_folders:
    # here we are reading the hdf files into a dataframe, filterting epoch around time zero
    # and converting into np array for speed
    df_A = pd.read_hdf(f'{i}\\{signal_A}')
    df_A = df_A[df_A['timestamps'].between(filter_ts_low, filter_ts_high)]
    A_arr = df_A.iloc[:, :-3].T.to_numpy()

    df_B = pd.read_hdf(f'{i}\\{signal_B}')
    df_B = df_B[df_B['timestamps'].between(filter_ts_low, filter_ts_high)]
    B_arr = df_B.iloc[:, :-4].T.to_numpy()

    # create empty list to build array of correlations for each event
    cross_corr = []
    cross_corr *= 0  # ensures list is empty

    # zip signal A and signal B arrays to iterate in parallel  and calculate correlation coefficient
    for (a, b) in zip(A_arr, B_arr):
        corr = signal.correlate(a, b)
        corr /= np.max(corr)
        cross_corr.append(corr)
        lag = signal.correlation_lags(len(a), len(b))
        lag_msec = (lag / 1.017E2)
        cross_corr_arr = np.asarray(cross_corr, dtype='float16').transpose()
    # create new dataframe, calculate mean, sem and attach lag time
    df_c = pd.DataFrame(cross_corr_arr)
    df_c = (df_c.assign(mean=df_c.mean(axis=1),
                        sem=df_c.sem(axis=1),
                        lag_time=lag_msec))
    #  save to csv in output file path + new folder we created
    df_c.to_csv(f'{i}\\{new_folder}\\{os.path.basename(i).split("_")[0]}_.csv')


#%%
