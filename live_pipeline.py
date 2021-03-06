import time
import numpy as np
import asyncio
import csv
import pickle
import pandas as pd
import mne
import time
import sklearn
import brainflow
from brainflow.board_shim import BoardShim, BrainFlowInputParams


async def processing(sample):
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
  print(return_data)
  print('Processing Finished')

async def recordData(board_id=-1, samples=450000):
  unprocessed_data = [[0],[0],[0],[0],[0],[0],[0]]
  all_processed_data  = [[0],[0],[0],[0],[0],[0],[0]]
  params = BrainFlowInputParams()
  # params.serial_port = serial_port
  board = BoardShim(board_id, params)
  board.prepare_session()

  board.start_stream(samples + 1)

  i = 0
  while i < 1000:
    if board.get_board_data_count() > 1:
      data = board.get_board_data()
      print(data.shape)
      # print(len(data))
      # print(data)
      data = data[:7]
      unprocessed_data = np.append(unprocessed_data,data, axis=1)

      processed_data = await processing(data)
      all_processed_data = np.append(all_processed_data, processed_data, axis=1)
    i = i + 1

  board.stop_stream()
  board.release_session()

  # data = data[:7].T
  print(type(unprocessed_data))
  np.savetxt("unprocessed_data.csv", unprocessed_data, delimiter=',', newline='\n')
  return data

asyncio.run(recordData())