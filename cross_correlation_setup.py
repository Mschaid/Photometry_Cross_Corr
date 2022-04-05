
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import os
import glob

##  function to create new folder
def new_folder(path):
    new_folder_path = (path + "\\" + path.split("\\")[-1] + "_cross_coor_analysis")
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
        return print("Directory created")
    else:
       return  print("Directory already exists")
