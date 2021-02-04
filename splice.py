import csv
import pickle
import numpy as np
import pandas as pd
import os
from sklearn import preprocessing as sk
import mne
import time
import threading

stored_data;
return_data;

def processing(sample):
	# TODO: perform MNE processing here

	sample = np.transpose(sample)
	ch_names = ['EXG Channel 0', 'EXG Channel 1', 'EXG Channel 2', 'EXG Channel 3', 'EXG Channel 4', 'EXG Channel 5',
				'EXG Channel 6']
	#Butterworth filter
	info = mne.create_info(ch_names, sfreq=250, ch_types='emg')

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


def splice(filename, channels=8, hz=250, chunkSecs=2):
	# prints out True every second
	# while(True):
	# 	time.sleep(1)
	# 	print(True)

	count = 0
	chunks, curr, labels = [], [], [] # all chunks, current reading sample
	i = 0
	with open(filename, 'r') as file:
		f = csv.reader(file)
		for i in range(5): # skip first five lines
	 		next(f)

		for l in f:
			if len(curr) == chunkSecs * hz: # if done with one sample
				# if i%2 == 0:
				# 	labels.append(1)
				# 	i+=1
				# else:
				# 	labels.append(0)
				# 	i+=1
				labels.append(0)
				chunks.append((processing(curr))) # add to list of all chunks
				# count+=1
				curr = [] # prepare for next sample

			curr.append([float(x) for x in l[1:channels]]) # add channel recording to current sample
	data = np.asarray(chunks) # convert chunks to np array

	with open('%s_labels.csv' % filename.split('.')[0], 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(labels)

	pickle.dump(data, open('%s.pkl' % filename.split('.')[0], 'wb'))
	print('Extracted %d chunks from %s' % (data.shape[0], filename))
	print(data.shape)
	print(len(labels))

def record(data):
	return;

# We're going recording the data and processing in parrallel
def driver(data):
	if (data):
		# Record 1 sec
		rd = threading.Thread(target=record, args=(data,))
		
		# Wait for recording to finish
		rd.join()

		# Process the sec of recording
		pd = threading.Thread(target=processing, args=(data,))

		# Return the data after processing
		return return_data

splice("OpenBCI-RAW-2020-11-16_01-42-35.txt")
