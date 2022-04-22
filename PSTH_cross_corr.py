import numpy as np
import pandas as pd
import os
import glob
import cross_correlation_setup as cc
import fnmatch
from scipy import signal


path_to_folders = r"C:\Users\mds8301\Desktop\PSTH_corr_test"

# search path for guppy outputs
sub_folders = glob.glob(path_to_folders + "\\**\\*output_*", recursive=True)

# create new file called cross corelation analysis
new_folder = "cross_correlation_analysis"

# create new folder in each output folder called
# 'cross_correlation_analyis - indiv analysis will be stored here
for i in sub_folders:
    cc.new_folder(path=i, name=new_folder)

#  give signal input files for Signal A vs Signal B
signal_A = "cue_NAC_z_score_NAC.h5"
signal_B = "cue_LH_z_score_LH.h5"

# set parameters to filter around time 0
filter_ts_low = -2
filter_ts_high = 2

# in each ouput get cue z_score
for i in sub_folders:
    # here we are reading the hdf files into a dataframe, filterting epoch around time zero
    # and converting into np array for speed
    df_A = pd.read_hdf(f"{i}\\{signal_A}")
    df_A = df_A[df_A["timestamps"].between(filter_ts_low, filter_ts_high)]
    df_A = df_A.rolling(window=1000, center=True).mean().dropna()
    A_arr = df_A.iloc[:, :-3].T.to_numpy()

    df_B = pd.read_hdf(f"{i}\\{signal_B}")
    df_B = df_B[df_B["timestamps"].between(filter_ts_low, filter_ts_high)]
    df_B = df_B.rolling(window=1000, center=True).mean().dropna()
    B_arr = df_B.iloc[:, :-3].T.to_numpy()

    # create empty list to build array of correlations for each event
    cross_corr = []
    cross_corr *= 0  # ensures list is empty
    # zip signal A and signal B arrays to iterate in parallel  and calculate correlation coefficient
    # TO DO check weird values in console to make sure this is working. it
    # shouldn't be giving values over 1?
    for (a, b) in zip(A_arr, B_arr):
        corr = signal.correlate(a, b)
        corr_norm = corr/ np.max(np.abs(corr))
        cross_corr.append(corr_norm)
        lag = signal.correlation_lags(len(a), len(b))
        lag_msec = lag / 1.017e3
        cross_corr_arr = np.asarray(cross_corr, dtype="float16").transpose()
    # create new dataframe, calculate mean, sem and attach lag time
    df_c = pd.DataFrame(cross_corr_arr)
    df_c = df_c.assign(mean=df_c.mean(axis=1),
                       sem=df_c.sem(axis=1),
                       lag_time=lag_msec)
    #  save to csv in output file path + new folder we created
    df_c.to_csv(
        f'{i}\\{new_folder}\\{os.path.basename(i).split("_")[0]}_{signal_A.split(".")[0]}_VS_{signal_B.split(".")[0]}.csv')
print('analysis completed and files saved')

# %%
day = 'day12'
files_by_day = f"{path_to_folders}\\{day}"

compiled_files = []
for dirpath, dirs, files in os.walk(files_by_day):
    for filename in fnmatch.filter(files, f'*VS*.csv'):
        compiled_files.append((os.path.join(dirpath, filename)))

all_df = []
for f in compiled_files:
    df = pd.read_csv(f)
    df = (df.rename(columns={
        'mean': f"{(os.path.basename(f).split('_')[0])}_{day}_mean"})
    )
    all_df.append(df.iloc[:, -3])
df_grp = pd.DataFrame(all_df).T
df_grp = (df_grp.assign(group_mean=df_grp.mean(axis=1),
                        std=df_grp.std(axis=1),
                        sem=df_grp.sem(axis=1),
                        lag_time=lag_msec)
          )
path_to_save_grp = path_to_folders
df_grp.to_csv(
    r"C:\Users\mds8301\Desktop\PSTH_corr_test\\_NAc_VS_LHA_day12.csv")

# %%
