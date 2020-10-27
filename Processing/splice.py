import csv
import pickle
import numpy as np
import pandas as pd
import os
from sklearn import preprocessing as sk
import mne

def processing(sample):
	# TODO: perform MNE processing here
	print(type(sample))
	sample = np.transpose(sample)

	info = mne.create_info(7, sfreq=250, ch_types='emg')

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
	ica_data = mne.io.RawArray(filtered_raw, ica_info)

	# Fitting and applying ICA
	ica = mne.preprocessing.ICA(verbose=True)
	ica.fit(inst=ica_data)
	ica.apply(ica_data)
	filtered_raw_numpy = ica_data[:][0]

	#Normalization
	# normalized_raw = sk.normalize(filtered_raw_numpy, norm='l2')
	# preprocessed_raw = ica_data[:][0]
	# normalized_raw = sk.normalize(preprocessed_raw, norm='l2')
	# print((normalized_raw))

	# normalized_data = mne.io.RawArray(normalized_raw, info)
	# return normalized_data[:][0]
	return filtered_raw_numpy

def splice(filename, truth, channels=8, hz=250, chunkSecs=2):
	count = 0
	chunks, curr, labels = [], [], [] # all chunks, current reading sample
	with open(filename, 'r') as file:
		f = csv.reader(file)
		for i in range(5): # skip first five lines
			next(f)

		for l in f:
			if len(curr) == chunkSecs * hz: # if done with one sample
				# if len(chunks) < 35:
				# 	labels.append(1)
				# else:
				# 	labels.append(0)



				# decide how to label data.
				if truth == "no" :
					labels.append(0)
				elif truth == "yes" :
					labels.append(1)

				if count != 0:
					chunks.append(processing(curr)) # add to list of all chunks
				
				curr = [] # prepare for next sample

				curr.append([float(x) for x in l[1:channels]]) # add channel recording to current sample
				count += 1

	data = np.asarray(chunks) # convert chunks to np array
	with open('%s_labels.csv' % filename.split('.')[0], 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerow(labels)
	
	

	pickle.dump(data, open('%s.pkl' % filename.split('.')[0], 'wb'))
	print('Extracted %d chunks from %s' % (data.shape[0], filename))



directory = os.path.dirname(os.path.abspath(__file__))

for filename in os.listdir(directory):
	if filename.endswith('.txt'):
		print (filename)
		splice(filename,'yes')