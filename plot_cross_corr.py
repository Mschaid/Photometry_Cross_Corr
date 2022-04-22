import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv(r"C:\Users\mds8301\Desktop\PSTH_corr_test\_NAc_VS_LHA_day12.csv")
print(data)



#%%
axs_list= [0]
fig, axs = plt.subplots(ncols = 2,
                       nrows = 1,
                        squeeze=True)
fig.suptitle('NAc VS LH \n'
             'day12')
sns.lineplot(data= data, x= 'lag_time', y= 'group_mean', ax= axs[0], )
axs[0].fill_between(data['lag_time'],
                    data['group_mean']+ data['sem'],
                    data['group_mean']- data['sem'],
                    alpha=0.3,
                    linewidth= 0)


sns.heatmap(data= data.iloc[:,1:-4].T,
            cbar=False,
            yticklabels=False,
            cmap= 'Blues',
            ax = axs[1]
            )
axs[1].set_xticks([])
for a in axs_list:
    #  x axis parameters
    axs[a].tick_params(axis='both', which='major', labelsize=12)
    axs[a].set_xlabel('Lag time(sec)',fontsize = 12, labelpad=2) #    x axis label
    axs[a].set_ylabel('Correlation Coefficient', fontsize=12, labelpad=2)
    sns.despine(ax=axs[a])
plt.tight_layout()
plt.rcParams['svg.fonttype'] = 'none' #save text as text in svg
plt.savefig(r"C:\Users\mds8301\Desktop\PSTH_corr_test\_NAc_VS_LHA_day12.tiff",
            dpi=300,
            transparent=True)
plt.savefig(r"C:\Users\mds8301\Desktop\PSTH_corr_test\_NAc_VS_LHA_day12.svg",
            dpi=300,
            transparent=True)
plt.show()


