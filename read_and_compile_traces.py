
import pandas as pd
import os
import cross_correlation_setup as cc

path_to_files = "R:\Mike\JS_for_MS"

# make new folder of analyzed data

cross_correlation_analysis_path = cc.new_folder(path_to_files, name = "cross_corr_analysis")
# compile files to analyze, set path, name to search for, and file type.
data_list = cc.get_data(path= path_to_files, search_for="z_score", file_type=".hdf5")
## extract data into dict -> dataframe
dict_of_data = {}
for i in data_list:
    id = cc.get_id(i)  # get mouse ID from path
    label = os.path.basename(i).split(".")[0] #  get label of data
    k = str(id+"_"+label) #  create key value name from id and label
    v = cc.read_hdf5(i) #  read HDF5 file and make it an array value
    dict_of_data.update({k:v}) #  update dict with key:value pair
    df = pd.DataFrame(
        dict([(k, pd.Series(v)) for k, v in dict_of_data.items()]) #  convert to dataframe
    )


## save dataframe to h5
compiled_data_path = cross_correlation_analysis_path + "\\" + "compiled_data.h5"
df.to_hdf(compiled_data_path, key = 'data', mode = 'w')
print("Compiled data saved as H5 file")
print("Proceed to next step")

#%%
df_clean = pd.read_hdf(compiled_data_path)
#%%
df_clean =(df_clean .transpose()
           .reset_index()
           .rename(columns={"index": 'name'})
           .dropna(axis=1)
           # .melt(id_vars= ['name'])


           )
print(df_clean)
df_split = df_clean['name'].str.split('_', expand=True)
print(df_split)
#%%
#  for some reason I need to assign columns after closing the previous function chain. it won't work otherwise
df_clean = (df_clean.assign(
                # time = df_clean['variable'].div(1.071E3),
                mouse = df_split[0], #split index column string and assign to mouse and signal
                signal = df_split[3]
                    .drop(columns = ['name', 'variable'])
         ))
## TODO make this faster
print("data reformatted and cleaned")
#%%
clean_data_h5_path = cross_correlation_analysis_path + "\\" + "cleaned_compiled_data.h5"
df_clean.to_hdf(clean_data_h5_path, key = "data", mode = 'w')
print('Clean data saved as H5 file')
