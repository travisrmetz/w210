#visualize light curves

import pandas as pd 

global_view=pd.read_csv('globalbinned.csv')
local_view=pd.read_csv('localbinned.csv')
print(global_view.head(2))
print(global_view.shape)