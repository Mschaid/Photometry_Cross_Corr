import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt

import os
import glob
import cross_correlation_setup as cc

path_to_folders = r'R:\Mike\JS_for_MS'
#
## create new folder in each output folder called analysis
sub_folders = next(os.walk(os.path.abspath(path_to_folders)))

list_of_folders = [] ## create list of the output folders from the path_to_folders
for i in sub_folders[1]:
    folder_path = sub_folders[0] +'\\' + i
    list_of_folders.append(folder_path)
print(list_of_folders)

## create new folder in each output folder called 'cross_correlation_analyis - indiv analysis will be stored here
new_folder = 'cross_correlation_analysis'
for i in list_of_folders:
    cc.new_folder(path = i, name = 'cross_correlation_analysis')

data_list = [] ## list of list containing all files to analyze
for i in list_of_folders:
    files = cc.get_data(path=i, search_for="z_score", file_type=".hdf5")
    data_list.append(files)

## extract data into dict -> dataframe
for files in data_list:
    dict_of_data = {}
    arrs_to_analyze = []
    for f in files:
        id = cc.get_id(f)  # get mouse fD from path
        label = ((os.path.basename(f).split("."))[0]).split('_')[-1] #  get label of data - this extracts the last string from guppy output file
        k = str(label) #  create key value name from id and label
        v = cc.read_hdf5(f) #  read HDF5 file and make it an array (dict value)
        dict_of_data.update({k:v}) #  update dict with key:value pair
    df = pd.DataFrame( dict([(k, pd.Series(v)) for k, v in dict_of_data.items()]) )#  convert to dataframe

    df.to_csv(f'{os.path.dirname(f)}\\{new_folder}\\{id}.csv')

#
print ('Data extracted and saved')

#%%

df = (pd.read_csv(r'R:\Mike\JS_for_MS\F336-210610-153851_output_1\cross_correlation_analysis\F336.csv').dropna())
# corr = signal.correlate(df['F339_z_score_axon'], df['F339_z_score_cell'])
# corr /= np.max(corr)
# lag = signal.correlation_lags(len(df['F339_z_score_axon']), len(df['F339_z_score_cell']))

correlation = cc.cross_correlate(df['cell'], df['axon'])

#%%

