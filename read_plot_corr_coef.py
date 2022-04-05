import numpy as np
import pandas as pd
import h5py
import matplotlib.pyplot as plt

m1 = pd.read_csv(r'R:\Jillian\JS_for_MS\MS_Coeff_analysis\coef_F336-210610-153851.csv')
m2 = pd.read_csv(r'R:\Jillian\JS_for_MS\MS_Coeff_analysis\coef_F338.csv')
m3 = pd.read_csv(r'R:\Jillian\JS_for_MS\MS_Coeff_analysis\coef_F339.csv')
m4 = pd.read_csv(r'coef_FF337-210610-145106.csv')
#%%
low_limit = -2000
up_limit = 2000
m1_flt = (m1.loc[(m1['lag_time'] >= low_limit) & (m1['lag_time'] <= up_limit)]).reset_index().drop(columns = ['index', 'Unnamed: 0'])
m2_flt = (m2.loc[(m2['lag_time'] >= low_limit) & (m2['lag_time'] <= up_limit)]).reset_index().drop(columns = ['index', 'Unnamed: 0'])
m3_flt = (m3.loc[(m3['lag_time'] >= low_limit) & (m3['lag_time'] <= up_limit)]).reset_index().drop(columns = ['index', 'Unnamed: 0'])
m4_flt = (m4.loc[(m4['lag_time'] >= low_limit) & (m4['lag_time'] <= up_limit)]).reset_index().drop(columns = ['index', 'Unnamed: 0'])

#%%
grp_df = pd.DataFrame()
grp_df = (grp_df.assign( m1 = m1_flt['Co_Coef'],
                        m2 = m2_flt['Co_Coef'],
                        m3 = m3_flt['Co_Coef'],
                        m4 = m4_flt['Co_Coef'])
          )
grp_df = (grp_df.assign(mean = grp_df.mean(axis =1),
                        std=grp_df.std(axis=1),
                        sem = grp_df.sem(axis =1),
                        lag = m1_flt['lag_time']
                         )
          )
#%%
plt.plot(grp_df['lag'], grp_df['mean'])
plt.fill_between(grp_df['lag'],
                 (grp_df['mean']+grp_df['sem']),
                 (grp_df['mean']-grp_df['sem']),
                 color='blue',
                 alpha=0.3,
                 linewidth=0)
plt.savefig(r"R:\Jillian\JS_for_MS\MS_Coeff_analysis\\plt.tiff")