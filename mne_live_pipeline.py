import time
import numpy as np
import matplotlib
import csv
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd

import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds

import mne
import sklearn
from mne.channels import read_layout
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations

def processing(sample):

  sample = sample.T
  ch_names = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5',
        'EXG Channel 6']
  #Butterworth filter
  info = mne.create_info(ch_names, sfreq=250, ch_types='emg')
  print ("SAMPLE DATA LEN:" + str(len(sample)))
  raw = mne.io.RawArray(sample, info)
  sfreq = 500
  f_p = 40

  # Applying butterworth filter
  iirs_params = dict(order=4, ftype='butter', output='sos')
  iir_params = mne.filter.construct_iir_filter(iirs_params, f_p, None, sfreq, 'lowpass', return_copy=False,
                          verbose=True)

  filtered_raw = mne.filter.filter_data(sample, sfreq=sfreq, l_freq=None, h_freq=f_p, picks=None, method='iir',
                      iir_params=iir_params, copy=False, verbose=True)

  filtered_data = mne.io.RawArray(filtered_raw, info)



  # Setting up data for fitting
  ica_info = mne.create_info(7, sfreq, ch_types='eeg')
  ica_data = mne.io.RawArray(filtered_data[:][0], ica_info)

  # Fitting and applying ICA
  ica = mne.preprocessing.ICA(verbose=True)
  ica.fit(inst=ica_data)
  ica.apply(ica_data)
  filtered_raw_numpy = ica_data[:][0]

  return_data = filtered_raw_numpy
  return return_data

def get_one_chunk(board, info):
    return_stream = []
    i = 0
    while i < 1250: #5 secs
        
        time.sleep(5)
        data = board.get_board_data()
        
        eeg_channels = BoardShim.get_eeg_channels(BoardIds.SYNTHETIC_BOARD.value)
        eeg_channels = eeg_channels[:7]
        eeg_data = data[:, eeg_channels]
        processed_data = processing(eeg_data)
        # print("PROCESSED DATA:")
        # print(processed_data)

        
        np.transpose(processed_data)
        processed_data = processed_data.astype(float)
        if i < 250:
            #raw = mne.io.RawArray(processed_data, info)
            #np.append(return_stream, processed_data)
            return_stream.append(processed_data)
        else:
            # temp = mne.io.RawArray(processed_data, info)
            # raw.append(temp)
            # raw.annotations.delete(int(i/250))
            #np.append(return_stream, processed_data, axis=0)
            return_stream.append(processed_data)

        i+=250
    return np.asarray(return_stream)

def chunk_generator(board,limit, info):
    i = 0
    while i < limit:
        yield  get_one_chunk(board, info)
        i+=1


def driver():
    BoardShim.enable_dev_board_logger()
    # use synthetic board for demo

    ch_names = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5',
                'EXG Channel 6']
    sfreq = 250
    info = mne.create_info(ch_names, sfreq, ch_types='emg')

    params = BrainFlowInputParams()
    board = BoardShim(BoardIds.SYNTHETIC_BOARD.value, params)
    board.prepare_session()
    board.start_stream()

    for chunks in chunk_generator(board, 1, info):
        print(chunks)
        temp = mne.io.RawArray(chunks, info)
        temp.plot(block = True, scalings="auto")

    board.stop_stream()
    board.release_session()

driver()