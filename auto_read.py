import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import os
import glob
import cross_correlation_setup as cc
#%%  search files for sig 1 and sig 2
path_to_files = "R:\Mike\JS_for_MS"
#%%  make new folder of analyzed data
cc.new_folder(path_to_files)
#%% compile files to analyze, set path, name to search for and file type.
data = cc.get_data(path= path_to_files, search_for="z_score", file_type=".hdf5")
#extract data
#%%
test = cc.read_hdf5(data[0])
print(test)
