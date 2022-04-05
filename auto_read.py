import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import signal
import os
import glob
import cross_correlation_setup as ms_funct
#%%  search files for sig 1 and sig 2
path_to_files = "R:\Mike\JS_for_MS"
#  make new folder of analyzed data
new_folder(path_to_files)
#  for each sig 1 and sig 2, do cross correlation and lag time, then input into a data frame with mouse ID
