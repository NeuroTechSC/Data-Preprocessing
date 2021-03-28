import time
import numpy as np
import matplotlib
import csv
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

import mne
from mne.channels import read_layout


def main():
    BoardShim.enable_dev_board_logger()
    # use synthetic board for demo
    i = 0
    while i < 1250: #5 secs
        params = BrainFlowInputParams()
        board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
        board.prepare_session()
        board.start_stream()
        time.sleep(5)
        data = board.get_board_data()
        board.stop_stream()
        board.release_session()

        eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
        eeg_channels = eeg_channels[:7]
        eeg_data = data[:, eeg_channels]
        #print(eeg_data)
        with open('new_live_data.csv', 'w', newline='') as file:#NEED TO APPEND TO FILE
            writer = csv.writer(file)
            for rows in range(eeg_data.shape[0]):
                writer.writerow(eeg_data[rows])
        #np.savetxt("new_live_data.csv", eeg_data, delimiter=',', newline='\n')
        i+=250
    #eeg_data = eeg_data / 1000000  # BrainFlow returns uV, convert to V for MNE

    # Creating MNE objects from brainflow data arrays
    # ch_types = ['eeg'] * len(eeg_channels)
    # ch_names = BoardShim.get_eeg_names(BoardIds.SYNTHETIC_BOARD.value)
    # sfreq = BoardShim.get_sampling_rate(BoardIds.SYNTHETIC_BOARD.value)
    # info = mne.create_info(ch_names=ch_names, sfreq=sfreq, ch_types=ch_types)
    # np.savetxt("new_live_data.csv", eeg_data, delimiter=',', newline='\n')
    # raw = mne.io.RawArray(eeg_data, info)
    # # its time to plot something!
    # raw.plot_psd(average=True)
    # plt.savefig('psd.png')


if __name__ == '__main__':
    main()