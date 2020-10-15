# -*- coding: utf-8 -*-
import click
import logging
import os
from pathlib import Path
#from dotenv import find_dotenv, load_dotenv
import multiprocessing
import numpy as np
import pandas as pd
import helpers.preprocess as preprocess
import sys
from definitions import OUTPUT_DIR, TCE_TABLE_DIR, KEPLER_DATA_DIR,NUMBER_OF_RECORDS

def generate_tce_data(tce_table):

    # Initialise dataframes to populate with processed data
    flattened_fluxes_df = pd.DataFrame()
    folded_fluxes_df = pd.DataFrame()
    globalbinned_fluxes_df = pd.DataFrame()
    localbinned_fluxes_df = pd.DataFrame()

    # Processing metrics
    num_tces = len(tce_table)
    processed_count = 0
    failed_count = 0


    # Iterate over every TCE in the table
    for _, tce in tce_table.iterrows():

        try:
            # Process the TCE and retrieve the processed data.
            flattened_flux, folded_flux, local_view, global_view = process_tce(tce)
            #TRM:  the above statement originally had local and global views reversed so were mislabeled

            # Append processed flux light curves for each TCE to output dataframes.
            flattened_fluxes_df = flattened_fluxes_df.append(pd.Series(flattened_flux), ignore_index=True)
            folded_fluxes_df = folded_fluxes_df.append(pd.Series(folded_flux), ignore_index=True)
            globalbinned_fluxes_df = globalbinned_fluxes_df.append(pd.Series(global_view), ignore_index=True)
            localbinned_fluxes_df = localbinned_fluxes_df.append(pd.Series(local_view), ignore_index=True)

            print('Kepler ID: {} processed'.format(tce.kepid))
            print("Processed Percentage: ", ((processed_count + failed_count) / num_tces) * 100, "%")
            processed_count += 1

        except:
            print('Kepler ID: {} failed'.format(tce.kepid))
            failed_count += 1

    return flattened_fluxes_df, folded_fluxes_df, globalbinned_fluxes_df, localbinned_fluxes_df


def process_tce(tce):
  """Processes the light curve for a Kepler TCE and returns processed data

  Args:
    tce: Row of the input TCE table.

  Returns:
    Processed TCE data at each stage (flattening, folding, binning).

  Raises:
    IOError: If the light curve files for this Kepler ID cannot be found.
  """
  # Read and process the light curve.
  print('Calling preprocess.read_and_process_light_curve for ',tce.kepid,' in ',KEPLER_DATA_DIR)
  time, flattened_flux = preprocess.read_and_process_light_curve(tce.kepid, KEPLER_DATA_DIR)

  time, folded_flux = preprocess.phase_fold_and_sort_light_curve(time, flattened_flux, tce.tce_period, tce.tce_time0bk)

  # Generate the local and global views.
  local_view = preprocess.local_view(time, folded_flux, tce.tce_period, tce.tce_duration, num_bins=201, bin_width_factor=0.16, num_durations=4)
  global_view = preprocess.global_view(time, folded_flux, tce.tce_period, num_bins=2001, bin_width_factor=1 / 2001)

  return flattened_flux, folded_flux, local_view, global_view


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('Making final data set from raw data')

    # Load TCE Table
    tce_table = pd.read_csv(TCE_TABLE_DIR)
    tce_table=tce_table[0:NUMBER_OF_RECORDS]
    #print(tce_table.columns)
    logger.info('Loaded TCE file - about to call generate_tce_data')
    tce_table["tce_duration"] /= 24  # Convert hours to days.
    tce_table['av_training_set']='PC'
    #np.random.seed(123)
    #tce_table = tce_table.iloc[np.random.permutation(num_tces)]
    flattened_df, folded_df, globalbinned_df, localbinned_df = generate_tce_data(tce_table)
    flattened_df.to_csv(OUTPUT_DIR + 'flattened.csv', na_rep='nan', index=False)
    folded_df.to_csv(OUTPUT_DIR + 'folded.csv', na_rep='nan', index=False)
    globalbinned_df.to_csv(OUTPUT_DIR + 'globalbinned.csv', na_rep='nan', index=False)
    localbinned_df.to_csv(OUTPUT_DIR + 'localbinned.csv', na_rep='nan', index=False)
    flattened_df.to_pickle(OUTPUT_DIR + 'flattened.pkl')
    folded_df.to_pickle(OUTPUT_DIR + 'folded.pkl')
    globalbinned_df.to_pickle(OUTPUT_DIR + 'globalbinned.pkl')
    localbinned_df.to_pickle(OUTPUT_DIR + 'localbinned.pkl')

    logger.info('Succesfully saved TCE samples')
    sys.exit()


    # Name of the target column and labels to use as training labels.
    #_LABEL_COLUMN = "av_training_set"
    #_ALLOWED_LABELS = {"PC", "AFP", "NTP"}

    # Discard other labels from TCE table other than the allowed labels.
    #allowed_tces = tce_table[_LABEL_COLUMN].apply(lambda l: l in _ALLOWED_LABELS)
    #tce_table = tce_table[allowed_tces]
    

    # Randomly shuffle the TCE table.
    np.random.seed(123)
    tce_table = tce_table.iloc[np.random.permutation(num_tces)]

    # Split positive and negative TCE samples
    neg = ['AFP', 'NTP']
    positive_tce_table = tce_table.loc[tce_table['av_training_set'] == "PC"]
    negative_tce_table = tce_table.loc[tce_table['av_training_set'].isin(neg)]

    # Process the TCE tables
    # positive_flattened_df, positive_folded_df, positive_globalbinned_df, positive_localbinned_df = generate_tce_data(positive_tce_table)
    # logger.info('Succesfully processed positive TCE samples.')

    negative_flattened_df, negative_folded_df, negative_globalbinned_df, negative_localbinned_df = generate_tce_data(negative_tce_table)
    logger.info('Succesfully processed negative TCE samples.')
    #
    # # Store processed data
    # positive_flattened_df.to_csv(OUTPUT_DIR + 'positives_flattened.csv', na_rep='nan', index=False)
    # positive_folded_df.to_csv(OUTPUT_DIR + 'positives_folded.csv', na_rep='nan', index=False)
    # positive_globalbinned_df.to_csv(OUTPUT_DIR + 'positives_globalbinned.csv', na_rep='nan', index=False)
    # positive_localbinned_df.to_csv(OUTPUT_DIR + 'positives_localbinned.csv', na_rep='nan', index=False)
    # positive_flattened_df.to_pickle(OUTPUT_DIR + 'positives_flattened.pkl')
    # positive_folded_df.to_pickle(OUTPUT_DIR + 'positives_folded.pkl')
    # positive_globalbinned_df.to_pickle(OUTPUT_DIR + 'positives_globalbinned.pkl')
    # positive_localbinned_df.to_pickle(OUTPUT_DIR + 'positives_localbinned.pkl')
    #
    # logger.info('Succesfully saved positive TCE samples.')

    negative_flattened_df.to_csv(OUTPUT_DIR + 'negatives_flattened.csv', na_rep='nan', index=False)
    negative_folded_df.to_csv(OUTPUT_DIR + 'negatives_folded.csv', na_rep='nan', index=False)
    negative_globalbinned_df.to_csv(OUTPUT_DIR + 'negatives_globalbinned.csv', na_rep='nan', index=False)
    negative_localbinned_df.to_csv(OUTPUT_DIR + 'negatives_localbinned.csv', na_rep='nan', index=False)
    negative_flattened_df.to_pickle(OUTPUT_DIR + 'negatives_flattened.pkl')
    negative_folded_df.to_pickle(OUTPUT_DIR + 'negatives_folded.pkl')
    negative_globalbinned_df.to_pickle(OUTPUT_DIR + 'negatives_globalbinned.pkl')
    negative_localbinned_df.to_pickle(OUTPUT_DIR + 'negatives_localbinned.pkl')

    logger.info('Succesfully saved negative TCE samples.')

    # Label dataframes
    # positive_flattened_df['LABEL'] = 1
    # positive_folded_df['LABEL'] = 1
    # positive_globalbinned_df['LABEL'] = 1
    # positive_localbinned_df['LABEL'] = 1
    negative_flattened_df['LABEL'] = 0
    negative_folded_df['LABEL'] = 0
    negative_globalbinned_df['LABEL'] = 0
    negative_localbinned_df['LABEL'] = 0

    # Merge positive and negative TCE samples in a final dataframe
    # final_globalbinned_df = positive_globalbinned_df.append(negative_globalbinned_df)
    # final_localbinned_df = positive_localbinned_df.append(negative_localbinned_df)
    # final_folded_df = positive_folded_df.append(negative_folded_df)
    # final_flattened_df = positive_flattened_df.append(negative_flattened_df)

    # Store as .csv and serialized
    # final_globalbinned_df.to_csv(OUTPUT_DIR + 'final_globalbinned.csv', na_rep='nan', index=False)
    # final_localbinned_df.to_csv(OUTPUT_DIR + 'final_localbinned.csv', na_rep='nan', index=False)
    # final_folded_df.to_csv(OUTPUT_DIR + 'final_folded.csv', na_rep='nan', index=False)
    # final_flattened_df.to_csv(OUTPUT_DIR + 'final_flattened.csv', na_rep='nan', index=False)
    #
    # final_globalbinned_df.to_pickle(OUTPUT_DIR + 'final_globalbinned.pkl')
    # final_localbinned_df.to_pickle(OUTPUT_DIR + 'final_localbinned.pkl')
    # final_folded_df.to_pickle(OUTPUT_DIR + 'final_folded.pkl')
    # final_flattened_df.to_pickle(OUTPUT_DIR + 'final_flattened.pkl')


if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    #load_dotenv(find_dotenv())

    main()