import numpy as np
import pandas as pd
import os
import mne
from brainflow.data_filter import DataFilter
from sklearn import preprocessing as sk
def main ():


    #Convert text files to csv file. May possibly remove this part later. It's useless right now.
    directory = os.path.dirname(os.path.abspath(__file__))

    # renames .txt files to .csv and then prints its contents
    filename = 'OpenBCI-RAW-2020-08-28_23-19-46.csv'
    restored_data = DataFilter.read_file(filename)
    print(restored_data.shape)
    if (restored_data.shape[0] > 9):  # If the timestamp has not already been removed then we will remove it
        #Removing the first 5 lines

        # Deleting Time channel and all the other 'unneccessary' channels
        for i in range(9,24):
            new_data = np.delete(restored_data, 9, 0)
            restored_df = pd.DataFrame(np.transpose(new_data))
            DataFilter.write_file(new_data, filename, 'w')
            restored_data = DataFilter.read_file(filename)

        new_data = np.delete(restored_data, 0, 0)
        restored_df = pd.DataFrame(np.transpose(new_data))
        DataFilter.write_file(new_data, filename, 'w')
        restored_data = DataFilter.read_file(filename)

        new_data = np.delete(restored_data, 7, 0)
        restored_df = pd.DataFrame(np.transpose(new_data))
        DataFilter.write_file(new_data, filename, 'w')
        restored_data = DataFilter.read_file(filename)


    else:
        restored_df = pd.DataFrame(np.transpose(restored_data))

    # new_data = np.delete(restored_data, 7, 0)
    # restored_df = pd.DataFrame(np.transpose(new_data))
    # DataFilter.write_file(new_data, filename, 'w')

    ##############################################################
    # Raw Data                                                   #
    ##############################################################

    print('Data From the File')
    print(restored_df.head(10))


    data = np.loadtxt(filename, delimiter=',')  # remember to remove the first five lines
    data = np.transpose(data)


    ch_names = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5',
                'EXG Channel 6']

    sfreq = 250
    info = mne.create_info(ch_names, sfreq, ch_types='emg')

    data = data.astype(float)

    print(data.shape)

    raw = mne.io.RawArray(data, info)
    print(raw)
    print(raw.info)

    raw.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
     emg=1e2, ref_meg=1e-12, misc=1e-3, stim=1,
     resp=1, chpi=1e-4, whitened=1e2))


    ##############################################################
    # Butterworth Filter                                         #
    ##############################################################

    sfreq = 250
    f_p = 7

    #Applying butterworth filter
    iirs_params = dict(order = 8, ftype = 'butter', output = 'sos')
    iir_params = mne.filter.construct_iir_filter(iirs_params, f_p, None, sfreq, btype='lowpass', return_copy = False, verbose = True)

    filtered_raw = mne.filter.filter_data(data, sfreq = sfreq, l_freq = None, h_freq = f_p, picks = None, method = 'iir', iir_params = iir_params, copy = False, verbose = True)

    # get rid of the spike
    filtered_raw = filtered_raw[0:, 190:]

    filtered_data = mne.io.RawArray(filtered_raw, info)
    print(filtered_data.info)

    #Plotting filtered data
    filtered_data.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
     emg=1e2, ref_meg=1e-12, misc=1e-3, stim=1,
     resp=1, chpi=1e-4, whitened=1e2))
    print(type(filtered_data))


    ##############################################################
    # ICA Preprocessing                                          #
    ##############################################################

    #Setting up data for fitting
    ica_info = mne.create_info(ch_names, sfreq, ch_types='eeg')
    ica_data = mne.io.RawArray(filtered_raw, ica_info)

    #Fitting and applying ICA
    ica = mne.preprocessing.ICA(verbose = True)
    ica.fit(inst = ica_data)
    ica.apply(ica_data)

    #Plotting data
    ica_data.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=1e2, eog=150e-6, ecg=5e-4,
     emg=1e2, ref_meg=1e-12, misc=1e-3, stim=1,
     resp=1, chpi=1e-4, whitened=1e2))


    ##############################################################
    # Normalization                                              #
    ##############################################################

    filtered_raw_numpy = ica_data[:][0]
    normalized_raw = sk.normalize(filtered_raw_numpy, norm='l2')
    preprocessed_raw = ica_data[:][0]
    normalized_raw = sk.normalize(preprocessed_raw, norm='l2')
    print((normalized_raw))

    normalized_data = mne.io.RawArray(normalized_raw, info)

    normalized_data.plot(block = True, scalings=dict(mag=1e-12, grad=4e-11, eeg=20e-6, eog=150e-6, ecg=5e-4,
    emg=5e-3, ref_meg=1e-12, misc=1e-3, stim=1,
    resp=1, chpi=1e-4, whitened=1e2))



if __name__ == "__main__":
    main ()
