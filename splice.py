import csv
import pickle
import numpy as np
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter, FilterTypes, AggOperations
import mne
import requests
from bs4 import BeautifulSoup
import asyncio

stored_data = 0
return_data = 0

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


async def recordData(serial_port, board_id=0, samples=500):
    params = BrainFlowInputParams()
    params.serial_port = serial_port
    board = BoardShim(board_id, params)
    board.prepare_session()

    board.start_stream(samples + 1)
    #time.sleep(2.5)

    data = board.get_board_data()
    board.stop_stream()
    board.release_session()

    data = data[:7].T
    return data


# We're going recording the data and processing in parrallel
async def driver():
	#record and processing synch..
	record_task = recordData(55)
	next_data = record_task
	await asyncio.gather(
		# factorial("A", 2),
		# factorial("B", 3),
		# factorial("C", 4),
		processing(record_task),
	)

def web_parser():
	word_list = ['Seattle', 'San Francisco', 'Los Angeles', 'Berkeley', 'Houston', 'Chicago',
				'Davis', 'Oakland', 'Santa Cruz', 'San Jose', 'Austin', 'Denver',
				 'Boston', 'Phoenix', 'Indianapolis', 'Portland', 'Las Vegas', 'Detroit']
	word_diction = {}

	for i in word_list:
		page = requests.get('https://en.wiktionary.org/wiki/' + i)
		soup = BeautifulSoup(page.text, 'html.parser')
		IPA_list = soup.findAll(class_='IPA')
		print(i)
		for j in IPA_list:
			if str(j).count('/') == 3:
				for y in j:
					word_diction[i] = y

	print(word_diction)

	# Create for loop to print out all artists' names

#splice("OpenBCI-RAW-2020-11-16_01-42-35.txt")

web_parser()
