import csv
import pickle
import numpy as np
#from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds

import mne
import requests
from bs4 import BeautifulSoup
import asyncio
from difflib import get_close_matches
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


#def recordData(board_id=-1, samples=450000):
	#params = BrainFlowInputParams()
	#params.serial_port = serial_port
	#board = BoardShim(board_id, params)
	#board.prepare_session()

	#board.start_stream(samples + 1)
	#time.sleep(2.5)

	#
#data = board.get_board_data()
	# for i in range(0, 5):
	# 	print('try')
	# 	print(data)
	# 	data = board.get_board_data()
	# print(data)
	# board.stop_stream()
	# board.release_session()
	#
	# data = data[:7].T
	# return data

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
		#print(i)
		for j in IPA_list:
			if str(j).count('/') == 3:
				for y in j:
					word_diction[i] = y

	compare('/siˈætl̩/', word_diction)

	print(word_diction)

def compare(input_IPA, word_diction):


	articulation = {'ŋ':0,'k':0,'g':0,'x':0,'w':0,'h':0,'tʃ':1,'dʒ':1,'tʃ':1,'dʒ':1,'ʃ':1,'ʒ':1,'r':1,'j':1,'n':2,'t':2,'d':2,'s':2,'z':2,'l':2,'θ':3,'ð':3,'m':4,'p':4,'b':4,'f':4,'v':4}
	manor = {'ŋ':2,'k':0,'g':0,'x':0,'w':-1,'h':0,'tʃ':1,'dʒ':1,'tʃ':1,'dʒ':0,'ʃ':1,'ʒ':0,'r':-1,'j':-1,'n':2,'t':1,'d':0,'s':1,'z':0,'l':-1,'θ':1,'ð':0,'m':2,'p':1,'b':0,'f':1,'v':0}
	occlusion = {'ŋ': -1, 'k': 0, 'g': 0, 'x': 1, 'w': 2, 'h': 1, 'tʃ': 0, 'dʒ': 0,
				 'ʃ': 1, 'ʒ': 1, 'r': 2, 'j': 2, 'n': -1, 't': 0, 'd': 0, 's': 1, 'z': 1, 'l': 2, 'θ': 1,'ð':1,'m':-1,'p':0,'b':0,'f':1,'v':1}
	diction_vectors = {}
	for key in word_diction.values():
		word_vectors = np.zeros((len(key),3))
		for letters_index in range(len(key)):
			if key[letters_index] != '/' and key[letters_index] != "\\":
				print(key)
				word_vectors[letters_index][0] = articulation[key[letters_index]]
				word_vectors[letters_index][1] = manor[key[letters_index]]
				word_vectors[letters_index][2] = occlusion[key[letters_index]]
		diction_vectors[key] = word_vectors
	print(diction_vectors)

	#place of articulation, manner of articulation, occlusion
	#vectors for each letter....vowel height, vowel frontedness, labialization
	best = get_close_matches(input_IPA, word_diction.values())
	print(best)
	# score = 0
	# best_score = 0
	# best_one = word_diction['Seattle']
	# x = 0
	# for i in word_diction:
	# 	for j in word_diction[i]:
	# 		if x > (len(input_IPA) -1):
	# 			break
	# 		#if word_diction[i][j] == input_IPA[i]:
	# 		if j == input_IPA[x]:
	# 		# if word_diction[i].get(j) == input_IPA[i]:
	# 			print(best_one)
	# 			score += 1
	# 			if score > best_score:
	# 				best_score = score
	# 				best_one = word_diction[i]
	# 		x += 1
	# 	x = 0
	# 	score = 0

		# for symbol in word_diction[key]:
		# 	for j in len(inputIPA):
		# 	print(symbol)
		# for letter in i:
		# 	print (letter)
		# 
		# 	if inputIPA[j] == word_dictioncalue
	# Create for loop to print out all artists' names

#splice("OpenBCI-RAW-2020-11-16_01-42-35.txt")

web_parser()


#recordData()