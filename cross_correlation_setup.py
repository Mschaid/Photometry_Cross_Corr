import numpy as np
import h5py
import os
from scipy import signal


##  function to create new folder
def new_folder(path, name):
    new_folder_path = path + "\\" + name
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
        print("Directory created")
        return new_folder_path
    else:
        print("Directory already exists")
        return new_folder_path


##  function to compile list of files to analyze
def get_data(path, search_for, file_type):

    list_of_files = []
    list_of_files *= 0
    for path, currentDirectory, files in os.walk(path):
        for file in files:
            if file.startswith(search_for) and file.endswith(file_type):
                list_of_files.append(os.path.join(path, file))
    print("Files collected")
    return list_of_files


## function to read hdf5 data
def read_hdf5(file, input):
    read_file = h5py.File(file, "r")
    extracted_data = read_file.get(input)
    arr = np.array(extracted_data)
    return arr


## function to get mouse ID from guppy output
def get_id(path):
    mouse_id = path.split("\\")[-2].split("_")[0]
    return mouse_id


## function to pass in dataframe column names to cross correlate


def df_cross_correlate(signal_A, signal_B):
    corr = signal.correlate(signal_A, signal_B)
    corr /= np.max(corr)
    lag = signal.correlation_lags(len(signal_A), len(signal_B))
    lag_msec = (lag/1.017E2)
    return (corr, lag_msec)


def normalize(array):
    if np.max(array) >= -np.min(array):
        arr = array/np.max(array)
    else:
        arr = array/(- np.min(array))
    return arr