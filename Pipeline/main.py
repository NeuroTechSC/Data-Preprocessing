import argparse
import time
import numpy as np
import pandas as pd

from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations


def main ():


    # demo for data serialization using Pipeline API, we recommend to use it instead pandas.to_csv()
    #DataFilter.write_file (data, 'test.csv', 'w') # use 'a' for append mode
    restored_data = DataFilter.read_file ('OpenBCI-RAW-2020-08-18_08-44-41.csv')
    restored_df = pd.DataFrame (np.transpose (restored_data))
    print ('Data From the File')
    print (restored_df.head (10))

    

if __name__ == "__main__":
    main ()