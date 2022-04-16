import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
import os
import glob
import cross_correlation_setup as cc
import fnmatch

path_to_folders = r"C:\Users\mds8301\Desktop\test_coef\day14"
#
## create new folder in each output folder called analysis
sub_folders = glob.glob(path_to_folders + '\\**\\*output_*', recursive=True)

## create new folder in each output folder called 'cross_correlation_analyis - indiv analysis will be stored here
new_folder = "cross_correlation_analysis"
for i in sub_folders:
    cc.new_folder(path=i, name="cross_correlation_analysis")

data_list = []  ## list of list containing all files to analyze
for i in sub_folders:
    files = cc.get_data(path=i, search_for="z_score", file_type=".hdf5")
    data_list.append(files)
for i in data_list:
    print(i)
#%%
## extract data into dict -> dataframe
for files in data_list:
    dict_of_data = {}
    arrs_to_analyze = []
    for f in files:
        id = cc.get_id(f)  # get mouse fD from path
        label = ((os.path.basename(f).split("."))[0]).split("_")[-1]  #  get label of data - this extracts the last string from guppy output file
        k = str(label)  #  create key value name from id and label
        v = cc.read_hdf5(f,'data')  #  read HDF5 file and make it an array (dict value)
        dict_of_data.update({k: v})  #  update dict with key:value pair
    df = pd.DataFrame(
        dict([(k, pd.Series(v)) for k, v in dict_of_data.items()])
    )  #  convert to dataframe

    df.to_hdf(f"{os.path.dirname(f)}\\{new_folder}\\{id}.h5", key='df', mode = 'w')


print("Data extracted and saved")

print('collecting data to cross correlate')
files_to_analyze = glob.glob(f'{path_to_folders}\\**\\{new_folder}\\*.h5')
print('files collected')

#%%

##for each correlation, change signals to correlate (Signal_A vs Signal_B) and re-run this cell. when finished, move to next cell and run 1 time
Signal_A = 'axon'
Signal_B = 'receptor'
print(f'computing {Signal_A} vs {Signal_B} cross correlation')
## for each file read into dataframe and drop nan
for f in files_to_analyze:
    df = (pd.read_hdf(f)
          .dropna()
          )
## cross correlate signal a to signal b and create new dataframe
    correlation = cc.df_cross_correlate(df[Signal_A], df[Signal_B])
    dict_corr = {f'{Signal_A}VS{Signal_B}': correlation[0], 'lag_time(ms)':correlation[1]}
    id = (os.path.basename(f)).split('.')[0]
##  save new dataframe as mousename_A_VS_B.csv
    df_corr =  pd.DataFrame.from_dict(dict_corr)
    df_corr = (df_corr
                .assign(ID =id,
                        correlation=df_corr.columns[0])
                .rename(columns = {df_corr.columns[0]: 'co_coef'})
           )

    df_corr.to_hdf(f'{os.path.dirname(f)}\\{id}_{Signal_A}VS{Signal_B}_.h5', key = 'df', mode='w')

print(f'{Signal_A} vs {Signal_B} cross correlation computed and saved')

#%%
##  this cell will compiled all correlation files i with SignalA VS SignalB and save as master file.
compiled_files = []
for dirpath, dirs, files in os.walk(path_to_folders):
  for filename in fnmatch.filter(files, f'*VS*.h5'):
    compiled_files.append((os.path.join(dirpath, filename)))

for f in compiled_files:
    print(f)

all_df = []
for f in compiled_files:
    df = pd.read_hdf(f)
    all_df.append(df)
df_grp = pd.concat(all_df)

low_time = -10
high_time = 10
df_grp = (
    df_grp.loc[(df_grp['lag_time(ms)']>= low_time) & (df_grp['lag_time(ms)'] <= high_time)]
)

df_grp.to_hdf(f'{path_to_folders}\\cross_correlation_analysis_compiled_.h5', key='df', mode='w')

print(f'data compiled and saved in {path_to_folders}')
#%%
