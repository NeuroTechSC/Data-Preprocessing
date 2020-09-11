import argparse
import time
import numpy as np
import pandas as pd
import os
import mne
from mne.preprocessing import (ICA, create_eog_epochs, create_ecg_epochs,
                               corrmap)
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
from sklearn.decomposition import FastICA
from sklearn import preprocessing as sk
def main ():


    #Convert text files to csv file. May possibly remove this part later. It's useless right now.
    directory = os.path.dirname(os.path.abspath(__file__))

    # renames .txt files to .csv and then prints its contents
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            print(os.path.join(directory, filename))
            os.rename(os.path.join(directory, filename), filename[:-4] + '.csv')

            restored_data = DataFilter.read_file (filename[:-4] + '.csv')
            restored_df = pd.DataFrame (np.transpose (restored_data))
            print ('Data From the File')
            print (restored_df.head (10))
        else:
            break

    #Use BrainFlow methods to read file containing raw EMG data.
    restored_data = DataFilter.read_file ('OpenBCI-RAW-2020-08-18_08-44-41.csv')
    if (restored_data.shape[0] > 23):  # If the timestamp has not already been removed then we will remove it
        new_data = np.delete(restored_data, 23,0)  # There to delete the date since that could not be converted into float
        restored_df = pd.DataFrame(np.transpose(new_data))
        DataFilter.write_file(new_data, "OpenBCI-RAW-2020-08-18_08-44-41.csv", 'w')
    else:
        restored_df = pd.DataFrame(np.transpose(restored_data))
    
    
    ##############################################################
    # Raw Data                                                   #
    ##############################################################
    
    print('Data From the File')
    print(restored_df.head(10))


    data = np.loadtxt("OpenBCI-RAW-2020-08-18_08-44-41.csv", delimiter=',')  # remember to remove the first five lines
    data = np.transpose(data)


    ch_names = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5',
                'EXG Channel 6', 'EXG Channel 7', 'Accel Channel 0', 'Accel Channel 1', 'Accel Channel 2', 'Other',
                'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Analog Channel 0', 'Analog Channel 1',
                'Analog Channel 2',
                'Timestamp', 'Timestamp(Formatted)']

    sfreq = 250
    info = mne.create_info(ch_names, sfreq, ch_types='emg')

    data = data.astype(float)

    raw = mne.io.RawArray(data, info)
    print(raw)
    print(raw.info)

    raw.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
     emg=1e2, ref_meg=1e-12, misc=1e-3, stim=1,
     resp=1, chpi=1e-4, whitened=1e2))


    ##############################################################
    # Butterworth Filter                                         #
    ##############################################################

    sfreq = 1000
    f_p = 40


    #Applying butterworth filter
    iirs_params = dict(order = 4, ftype = 'butter', output = 'sos')
    iir_params = mne.filter.construct_iir_filter(iirs_params, f_p, None, sfreq, 'lowpass', return_copy = False, verbose = True)
    filtered_data = mne.filter.filter_data(data, sfreq = sfreq,l_freq = None, h_freq = f_p, picks = None, method = 'iir', iir_params = iir_params, copy = False, verbose = True)

    filtered_raw = mne.io.RawArray(filtered_data, info)
    print(filtered_raw.info)
    filtered_raw.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
     emg=1e2, ref_meg=1e-12, misc=1e-3, stim=1,
     resp=1, chpi=1e-4, whitened=1e2))
    print(type(filtered_raw))

    ##############################################################
    # Normalization                                          #
    ##############################################################

    filtered_raw_numpy = filtered_raw[:][0]
    normalized_raw = sk.normalize(filtered_raw_numpy, norm='l2')
    print((normalized_raw))
    normalized_raw = mne.io.RawArray(normalized_raw, info)
    normalized_raw.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
    emg=1e2, ref_meg=1e-12, misc=1e-3, stim=1,
    resp=1, chpi=1e-4, whitened=1e2))


    
    ##############################################################
    # ICA Preprocessing                                          #
    ##############################################################

    # filtered_raw_numpy = filtered_raw[:][0]
    #     # filtered_raw_numpy=filtered_raw_numpy.astype(float)
    #     # ica = mne.preprocessing.ICA(verbose = True)
    #     # filtered_raw = mne.io.RawArray(filtered_raw_numpy,info)
    #     # ica.fit(filtered_raw)
    #ica_raw = ica.apply(filtered_raw)
    # filtered_raw.load_data().filter(l_freq = 1, h_freq = None)
    # ica = ICA(n_components = 23, random_state=97)
    # ica.fit(filtered_raw)
    # ica.plot_sources(raw)

    # ica_raw.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
    #  emg=1e2, ref_meg=1e-12, misc=1e-3, stim=1,
    #  resp=1, chpi=1e-4, whitened=1e2))
    #

if __name__ == "__main__":
    main ()
