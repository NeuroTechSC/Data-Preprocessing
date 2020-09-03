import argparse
import time
import numpy as np
import pandas as pd
import os

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

    restored_data = DataFilter.read_file ('OpenBCI-RAW-2020-08-18_08-44-41.csv')
    restored_df = pd.DataFrame (np.transpose (restored_data))
    print ('Data From the File')
    print (restored_df.head (10))


if __name__ == "__main__":
    main ()