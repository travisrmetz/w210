import numpy as np
import pandas as pd
import os
from helpers.visualize import chart_curves
from definitions import PROCESSED_DATA_DIR,PROCESSED_DATA_CATALOG,PNG_FOLDER
import time


#takes in the tce index number, the tce id table, the results table (which figures out tp etc),
#and the two vector tables and then calls the visualization helper function which
#creates a chart and saves inside of processed_data folder structure

def chart(tce_number,
    tce_id,
    x_global,
    x_local,
    results=''):
    
    kepid=tce_id.loc[tce_number].kepid
    
    if results=='':
        result=tce_id.loc[tce_number].koi_disposition
        #ie use original disposition from ground truth, in 3 categories
    else:
        result=results.loc[tce_number].result
    
    print ('Result:',result)
    if result=='FALSE POSITIVE':
        adj_result='No Planet'
    if result=='CANDIDATE':
        adj_result='Planet'
    if result=='CONFIRMED':
        adj_result='Planet'

    print(kepid,result,adj_result)
    tce_plnt_num=tce_id.loc[tce_number].tce_plnt_num
    
    chart_curves(str(kepid),
                tce_plnt_num,
                x_global[tce_number],
                x_local[tce_number],
                adj_result)



LOCAL='localbinned_df.csv'
GLOBAL='globalbinned_df.csv'
x_local=pd.read_csv(os.path.join(PROCESSED_DATA_DIR,LOCAL))
x_global=pd.read_csv(os.path.join(PROCESSED_DATA_DIR,GLOBAL))
x_local=x_local.to_numpy()
x_global=x_global.to_numpy()
print(x_local.shape)
print(x_global.shape)

processed=pd.read_csv(os.path.join(PROCESSED_DATA_DIR,PROCESSED_DATA_CATALOG))
print(processed.shape)
print(processed.koi_disposition.value_counts())

LIMIT_FOR_TESTING=35000
processed=processed[0:LIMIT_FOR_TESTING]
start_time=time.time()
for i in range(len(processed)):
    chart(i,processed,x_global,x_local)
    print ('Processing',i+1,'of',len(processed))
    execution_time = (time.time() - start_time)
    print('Time in minutes:',execution_time/60 )
    extrapolated_time=(len(processed)/(i+1))*execution_time
    print('Time extrapolated to full TCE file (hours):',extrapolated_time/3600)
    print('Time remaining (hours):',(extrapolated_time-execution_time)/3600)
