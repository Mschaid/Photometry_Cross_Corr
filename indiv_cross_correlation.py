import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
import os
import glob
import cross_correlation_setup as cc
import fnmatch

path_to_folders = r"R:\Mike\JS_for_MS"
#
## create new folder in each output folder called analysis
sub_folders = next(os.walk(os.path.abspath(path_to_folders)))

list_of_folders = []  ## create list of the output folders from the path_to_folders
for i in sub_folders[1]:
    folder_path = sub_folders[0] + "\\" + i
    list_of_folders.append(folder_path)
print(list_of_folders)

## create new folder in each output folder called 'cross_correlation_analyis - indiv analysis will be stored here
new_folder = "cross_correlation_analysis"
for i in list_of_folders:
    cc.new_folder(path=i, name="cross_correlation_analysis")

data_list = []  ## list of list containing all files to analyze
for i in list_of_folders:
    files = cc.get_data(path=i, search_for="z_score", file_type=".hdf5")
    data_list.append(files)

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

#
print("Data extracted and saved")

print('collecting data to cross correlate')
files_to_analyze = glob.glob(f'{path_to_folders}\\**\\{new_folder}\\*.h5')
print('files collected')

#%%
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
compiled_files = []
for dirpath, dirs, files in os.walk(path_to_folders):
  for filename in fnmatch.filter(files, f'*VS*.h5'):
    compiled_files.append((os.path.join(dirpath, filename)))

for f in compiled_files:
    df_grp = pd.read_hdf(f)
    pd.concat([df_grp])
df_grp.to_hdf(f'{path_to_folders}\\cross_correlation_analysis_compiled_.h5', key='df', mode='w')

print(f'data compiled and saved in {path_to_folders}')
#%%

