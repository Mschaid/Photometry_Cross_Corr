
import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt
from scipy import signal
#Mouse 1
cell = r"R:\Jillian\JS_for_MS\F339\z_score_cell.hdf5"
axon = r"R:\Jillian\JS_for_MS\F339\z_score_axon.hdf5"
path_to_save = r"R:\Jillian\JS_for_MS\MS_Coeff_analysis"

cell_h5 = h5py.File(cell, 'r')
cell_data = cell_h5.get('data')
cell_arr = np.array(cell_data)

axon_h5 = h5py.File(axon, 'r')
axon_data = axon_h5.get('data')
axon_arr = np.array(axon_data)


corr = signal.correlate(cell_arr, axon_arr)
corr /= np.max(corr)
lag = signal.correlation_lags(len(cell_arr), len(axon_arr))

dict = {"Co_Coef":corr,
        "lag_time":lag }
data_df = pd.DataFrame.from_dict(dict).to_csv(path_to_save + "//coef_F339.csv")


#%%
