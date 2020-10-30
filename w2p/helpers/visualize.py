#visualize light curves

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from definitions import PNG_FOLDER

def chart_curves(kepid,tce_plnt_num,global_curve,local_curve,koi_disposition):
    fig,axes=plt.subplots(1,2,figsize=(20,6))
    gv=sns.scatterplot(data=global_curve,ax=axes[0])
    lv=sns.scatterplot(data=local_curve,ax=axes[1])
    axes[0].set_title('Global View: '+str(kepid)+'-'+str(tce_plnt_num)+' ('+koi_disposition+')')
    axes[1].set_title('Local View: '+str(kepid)+'-'+str(tce_plnt_num)+' ('+koi_disposition+')')
    gv.set(xticklabels=[])
    lv.set(xticklabels=[])
    gv.tick_params(bottom=False)
    lv.tick_params(bottom=False)
    plt.show()
    file_name=str(kepid)+'_'+str(tce_plnt_num)+'.png'
    plt.savefig(os.path.join(PNG_FOLDER,file_name))
    plt.close()

def main():
    file_path='/home/ubuntu/w210/w2p/processed_data'
    global_view=pd.read_csv(os.path.join(file_path,'globalbinned_df.csv'))
    local_view=pd.read_csv(os.path.join(file_path,'localbinned_df.csv'))
    tce_table=pd.read_csv(os.path.join(file_path,'tce_table.csv'))
    print('global_view shape:',global_view.shape)
    print('local_view shape:',local_view.shape)
    chart_curves(tce_table.kepid[1],tce_table.tce_plnt_num[1],tce_table.koi_disposition[1],global_view.loc[1],local_view.loc[1])


if __name__ == '__main__':
    main()
