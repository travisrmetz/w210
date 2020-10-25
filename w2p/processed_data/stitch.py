#aggregates separate files created by make_dataset.py
#hacked to run across different cpus in different processes
import pandas as pd

SEQUENCE=2 #number of output files created
file_list=['failed_kepids','globalbinned_df','localbinned_df','tce_table']
for file in file_list:
    df=pd.DataFrame()
    for i in range(0,SEQUENCE):
        file_name=file+str(i+1)+'.csv'
        print(file,file_name, i)
        try:
            if i==0:
                df=pd.read_csv(file_name)
                print(df.shape)
            else:
                print(df.shape)
                temp=pd.read_csv(file_name)
                print(temp.shape)
                df=pd.concat([df,temp])
                print(df.shape)
        except:
            pass
    df.to_csv(file+'.csv',index=False)
