import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import os
import glob
import cross_correlation_setup as cc

path_to_folders = r'R:\Mike\JS_for_MS'

## create new folder in each output folder called analysis
sub_folders = next(os.walk(os.path.abspath(path_to_folders)))
# print(sub_folders)

list_of_folders = [] ## create list of the output folders from the path_to_folders
for i in sub_folders[1]:
    folder_path = sub_folders[0] +'\\' + i
    list_of_folders.append(folder_path)
print(list_of_folders)

## create new folder in each output folder called 'cross_correlation_analyis - individ analysis will be stored here
for i in list_of_folders:
    cc.new_folder(path = i, name = 'cross_correlation_analysis')

data_list = [] ## list of list containing all files to analyze
for i in list_of_folders:
    files = cc.get_data(path=i, search_for="z_score", file_type=".hdf5")
    data_list.append(files)
