#visualize light curves

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def chart_curves(kepid,global_curve,local_curve):
    fig,axes=plt.subplots(1,2,figsize=(20,6))
    gv=sns.scatterplot(data=global_curve,ax=axes[0])
    lv=sns.scatterplot(data=local_curve,ax=axes[1])
    axes[0].set_title('Global View: '+str(kepid))
    axes[1].set_title('Local View: '+str(kepid))
    gv.set(xticklabels=[])
    lv.set(xticklabels=[])
    gv.tick_params(bottom=False)
    lv.tick_params(bottom=False)
    plt.show()
    file_name=str(kepid)+'.png'
    plt.savefig('save_as_a_png.png')

def main():
    global_view=pd.read_csv('globalbinned.csv')
    local_view=pd.read_csv('localbinned.csv')
    tce_table=pd.read_csv('tce_table.csv')
    print('global_view shape:',global_view.shape)
    print('local_view shape:',local_view.shape)
    chart_curves(tce_table.kepid[1],global_view.loc[1],local_view.loc[1])


if __name__ == '__main__':
    main()
