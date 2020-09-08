import argparse
import time
import numpy as np
import pandas as pd
import os
import mne
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def main ():


    # demo for data serialization using Pipeline API, we recommend to use it instead pandas.to_csv()
    #DataFilter.write_file (data, 'test.csv', 'w') # use 'a' for append mode
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

    restored_data = DataFilter.read_file ('OpenBCI-RAW-2020-08-18_08-44-41.csv')
    if (restored_data.shape[0] > 23):  # If the timestamp has not already been removed then we will remove it
        new_data = np.delete(restored_data, 23,0)  # There to delete the date since that could not be converted into float
        restored_df = pd.DataFrame(np.transpose(new_data))
        DataFilter.write_file(new_data, "OpenBCI-RAW-2020-08-18_08-44-41.csv", 'w')
    else:
        restored_df = pd.DataFrame(np.transpose(restored_data))
    print('Data From the File')
    print(restored_df.head(10))

    data = np.loadtxt("OpenBCI-RAW-2020-08-18_08-44-41.csv", delimiter=',')  # remember to remove the first three lines
    data = np.transpose(data)

    ch_names = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5',
                'EXG Channel 6', 'EXG Channel 7', 'Accel Channel 0', 'Accel Channel 1', 'Accel Channel 2', 'Other',
                'Other', 'Other', 'Other', 'Other', 'Other', 'Other', 'Analog Channel 0', 'Analog Channel 1',
                'Analog Channel 2',
                'Timestamp', 'Timestamp(Formatted)']

    sfreq = 250
    info = mne.create_info(ch_names, sfreq, ch_types='emg')

    raw = mne.io.RawArray(data, info)
    print(raw)
    print(raw.info)

    raw.plot()
    print(type(raw))


if __name__ == "__main__":
    main ()