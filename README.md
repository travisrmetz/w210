# w210_planets
## Fall 2020
## Christine Barger, Cullen Kavoussi, Travis Metz, Dean Wang

#### Project management
https://docs.google.com/document/d/1XaAeHGVal1ctlBBxCX1fzuqN_SWe4_n72n47J9HB9nI/edit?usp=sharing 

#### TCE list
CSV with all TCE's is in kepler-robovetter folder.

#### stellarium
get_skies.py and ssc_generator.yml (in stellarium folder) are from TRM w251 project and are examples of how you use Stellarium's scripting language.  I never got it to work headless (x11 etc) but Greg did

#### join-to-tess
This folder contains notebooks used to join Kepler space telescope transit candidate events (TCEs) to TESS space telescope data. It is used in the classification with the `triceratops` model.

The Kepler dataset is called `full_tce_list.csv` and can be found in the `kepler-robovetter` folder. 

The TESS dataset is called `CTL_v8_ExoFOP-TESS.csv` and can be downloaded from [ExoFOP-TESS](https://exofop.ipac.caltech.edu/tess/).

Notebooks:
* `join.ipynb`: takes in the Kepler TCE list file and finds the corresponding TESS object IDs.
* `Get Target Pixel File Counts.ipynb`: finds the number of target pixel files each TESS object ID has. This file is necessary for the `triceratops` tool classification

#### triceratops
The `triceratops` tool is used to validate planet candidates and it uses data from the TESS space telescope.

The `triceratops` package can be installed with the following command:

```
pip install triceratops
```

More on `triceratops` can be found in the [triceratops repo](https://github.com/stevengiacalone/triceratops).

Notebooks:
* `triceratops.ipynb`: this notebook takes in planet candidate entries and outputs probability of being a planet candidate as well as classificiations (false positives or planet candidates) from the probabilities.
* `join.ipynb`: this notebook takes in the results of the above classification as well as the w2p classification and merges the datasets together.

#### Literature review and links
https://docs.google.com/document/d/151AY7xbjxsxmGY2OcXakqFYXvKBICA64gBdTG9wCZfE/edit?usp=sharing 

#### Documentation for accessing FITS files
https://docs.astropy.org/en/stable/io/fits/

#### List of Kepler TCE from DR25 (34,032)
https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=tce

#### Documentation on TCE and KOI column names
https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html
https://exoplanetarchive.ipac.caltech.edu/docs/API_tce_columns.html



#### DR25 KOI (8054) - has 'final' disposition
https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=q1_q17_dr25_koi


#### astronet github
https://github.com/google-research/exoplanet-ml/tree/master/exoplanet-ml/astronet

#### dissertation
https://github.com/dinismf/exoplanet_classification_thesis/blob/master/reports/dissertation.pdf

![Transit](/images/TRANSIT.gif)