# Final Project for W210, MIDS, University of California Berkeley
# Exoplanet Discovery
## Fall 2020
## Christine Barger, Cullen Kavoussi, Travis Metz, Dean Wang

[Final project website](https://people.ischool.berkeley.edu/~kavoussi/ExoDiscovery/catal.html)

This repo has code and notebooks for our final project.

Team ExoPlanet was focused on helping astronomers and scientists understand the different machine learning algorithms used to detect exoplanets. Using data from NASA’s Kepler and TESS satellite missions, which contain graphical views of star brightness over time called threshold crossing events, we are applying known existing planet validation algorithms and comparing these results on a user-friendly website. In addition, we have built our own detection algorithm model that slightly improves the accuracy of exoplanet validation. We intend to use our website to contribute to peer and industry learning regarding exoplanet validation that can be done using machine learning techniques rather than manual visual inspection.


The W2P model relies in part on earlier work done on the Astronet model by [Shallue and Vandenberg](https://arxiv.org/abs/1712.05044), with some further inspiration from [Firmino](https://github.com/dinismf/exoplanet_classification_thesis).

![Transit](/images/TRANSIT.gif)

### General workflow
- Get list of TCEs from the [Kepler website](https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=tce)
- Download raw data files (.FITS) for all TCEs from the [Mikulsi Archive](https://archive.stsci.edu/).  Use a script to create a batch file to retrieve one by one
- Process data files into global and local vectors representing light curves using existing Kepler processing pipeline
- Create PNGs of light curves and move to S3 for use in Tableau
- Use global and local vectors to build w2p CNN model for TCE classification and add those results to runs from Robovetter and Autovetter
- Add classification results from Triceratops
- Create output file used by TABLEAU

### Explanation of key folder structure and files
#### w210
- data_clean.ipynb:  notebook that reads in the output csv file from Triceratops folder (which begins with the output csv from the w2p model) and creates forweb3.csv, which is the data file used for our Tableau visualizaton
- forweb3.csv: see above
- 
- /triceratops: This folder contains our running versionof the Triceratops model.  See more detailed description below.
- /w2p:  This folder has our exoplanet classification model
  * exoplanet_model_v3.ipynb:  this is the notebook which creates the w2p deep learning model to classify TCEs as either planets or no planets.  It outputs a csv file into /processed_data with its results.  In the case of our core CNN model that file is w2p_cnn_final.csv
  * get_light_curves.py:  master script for retrieving raw light curve data files from online archives.  Calls make_light_curve_batch.py which creates a batch file (get_kepler.sh) that actually retrieves
  * make_dataset.py:  runs the entire Kepler processing pipeline to using raw light curve/FITS files downloaded into raw_data.  Stores results in /processed_data.  This can be parallelized as demonstrated with 
  * make_png.py: makes PNG light curves from the processed fit files.  Then s3_upload_png.py moves them to S3 bucket
  * s3_upload_png.py:  takes PNGs created by make_png.py and uploads to S3 bucket so can be used in TABLEAU visualizations
  * /raw_data
    * make_light_curve_batch.py:  python script to create a batch file in light_curves directory and can be run to download the thousands of .FIT curves required for analysis
    * /light_curves
      * get_kepler.sh:  batch file that retrieves light curves and stores in this directory


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

More on `triceratops` can be found in the tool creators' [triceratops repo](https://github.com/stevengiacalone/triceratops).

Notebooks:
* `triceratops.ipynb`: this notebook takes in planet candidate entries and outputs probability of being a planet candidate as well as classificiations (false positives or planet candidates) from the probabilities.
* `join.ipynb`: this notebook takes in the results of the above classification as well as the w2p classification and merges the datasets together.


#### Documentation for accessing FITS files
https://docs.astropy.org/en/stable/io/fits/


#### Documentation on TCE and KOI column names
https://exoplanetarchive.ipac.caltech.edu/docs/API_kepcandidate_columns.html
https://exoplanetarchive.ipac.caltech.edu/docs/API_tce_columns.html

#### List of Kepler TCE from DR25 (34,032)
https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=tce

#### DR25 KOI (8054) - has 'final' disposition
https://exoplanetarchive.ipac.caltech.edu/cgi-bin/TblView/nph-tblView?app=ExoTbls&config=q1_q17_dr25_koi
