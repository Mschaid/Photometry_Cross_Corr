import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_hdf(r'R:\Mike\JS_for_MS\cross_correlation_analysis_compiled_.h5').reset_index(drop=True)
data = data.iloc[::5,:]

sns.lineplot(data=data, x='lag_time(ms)', y='co_coef', hue = 'correlation', ci=0.68, err_style='band')
plt.show()

print(data)


#%%


