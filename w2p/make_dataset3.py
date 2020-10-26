# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import time
import sys
import helpers.preprocess as preprocess
from definitions import OUTPUT_DIR, TCE_TABLE_DIR, KEPLER_DATA_DIR,NUMBER_OF_RECORDS

SEQUENCE=3
TRANCHE=1250

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
    failed_kepids=[]


    # Iterate over every TCE in the table
    generate_time=time.time()
    for _, tce in tce_table.iterrows():

        try:
            # Process the TCE and retrieve the processed data.
            print('Calling process_tce for: ',tce.kepid,'-',tce.tce_plnt_num)
            flattened_flux, folded_flux, local_view, global_view = process_tce(tce)
            #TRM:  the above statement originally had local and global views reversed so were mislabeled

            # Append processed flux light curves for each TCE to output dataframes.
            flattened_fluxes_df = flattened_fluxes_df.append(pd.Series(flattened_flux), ignore_index=True)
            folded_fluxes_df = folded_fluxes_df.append(pd.Series(folded_flux), ignore_index=True)
            globalbinned_fluxes_df = globalbinned_fluxes_df.append(pd.Series(global_view), ignore_index=True)
            localbinned_fluxes_df = localbinned_fluxes_df.append(pd.Series(local_view), ignore_index=True)

            print('Successfully processed: ',tce.kepid,'-',tce.tce_plnt_num)
            processed_count += 1
            processed_percentage=((processed_count+failed_count)/num_tces)*100
            print("Processed Percentage: ", processed_percentage, "%")
            execution_time=(time.time()-generate_time)
            #print('Execution time (seconds): ',execution_time)
            full_time=(execution_time/processed_percentage)*100
            print(processed_count,' | ',failed_count)
            print('Estimated total run time (hours): ',full_time/3600)

        except:
            print('Failed at processing: ',tce.kepid,'-',tce.tce_plnt_num)
            print('Error: ',sys.exc_info()[0],' | ',sys.exc_info()[1], ' | ',sys.exc_info()[2])
            failed_count += 1
            failed_kepids.append([tce.kepid,tce.tce_plnt_num])

    print('Success: ', processed_count,' | ','Failed: ', failed_count)
    print('Failed list: ', failed_kepids)
    return flattened_fluxes_df, folded_fluxes_df, globalbinned_fluxes_df, localbinned_fluxes_df,failed_kepids

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
  time, flattened_flux = preprocess.read_and_process_light_curve(tce.kepid, KEPLER_DATA_DIR)
  # prior statement brought down light curves for star.  following one processes individual tces as is being sent period and time for a tce of that star (kepid)
  time, folded_flux = preprocess.phase_fold_and_sort_light_curve(time, flattened_flux, tce.tce_period, tce.tce_time0bk)

  # Generate the local and global views.
  local_view = preprocess.local_view(time, folded_flux, tce.tce_period, tce.tce_duration, num_bins=201, bin_width_factor=0.16, num_durations=4)
  global_view = preprocess.global_view(time, folded_flux, tce.tce_period, num_bins=2001, bin_width_factor=1 / 2001)

  return flattened_flux, folded_flux, local_view, global_view


def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    
    start_time = time.time()

    # Load TCE Table
    tce_table = pd.read_csv(TCE_TABLE_DIR)
    original_length=tce_table.shape[0]
    starting_record=(SEQUENCE-1)*TRANCHE
    ending_record=(SEQUENCE)*TRANCHE
    tce_table=tce_table[starting_record:ending_record]
    print('Starting record: ',starting_record,'Ending record: ',ending_record)
    print('Loaded TCE table: ',tce_table.shape)
    
    tce_table["tce_duration"] /= 24  # Convert hours to days.
    tce_table['av_training_set']='PC'
    
    #not saving or using flattened or folded
    print('Calling generate_tce_data with tce_table')
    flattened_df, folded_df, globalbinned_df, localbinned_df,failed_kepids = generate_tce_data(tce_table)

    #save actual data
    global_name='globalbinned_df'+str(SEQUENCE)+'.csv'
    local_name='localbinned_df'+str(SEQUENCE)+'.csv'
    globalbinned_df.to_csv(OUTPUT_DIR + global_name, na_rep='nan', index=False)
    localbinned_df.to_csv(OUTPUT_DIR + local_name, na_rep='nan', index=False)
    
    #save the tce_table to this folder
    tce_name='tce_table'+str(SEQUENCE)+'.csv'
    tce_table.to_csv(OUTPUT_DIR+tce_name,index=False)

    #save the kepid and planet number where processing failed
    failed_kepids=pd.DataFrame(failed_kepids)
    failed_name='failed_kepids'+str(SEQUENCE)+'.csv'
    failed_kepids.to_csv(OUTPUT_DIR+failed_name,index=False)
    
    execution_time = (time.time() - start_time)
    print('Time in minutes:',execution_time/60 )
    extrapolated_time=(original_length/NUMBER_OF_RECORDS)*execution_time
    print('Time extrapolated to full TCE file (hours):',extrapolated_time/3600)

if __name__ == '__main__':
    main()