#### Downloading light curves

`python3 get_light_curves.py` calls `make_light_curve_batch.py` (which create batch file to download light curves from kepid columns in `q1_q17_dr25_tce.csv`) and then runs the actual batch file (with timing).  With approximately 35k kepids in TCE file this should take ~250gb and about 29 hours.

