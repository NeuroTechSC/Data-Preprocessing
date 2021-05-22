# This Python file uses the following encoding: utf-8

import csv
import pickle
import numpy as np

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

	compare('/ˌsæn ɚɹænˈsɪskoʊ/', word_diction)

	print(word_diction)

def compare(input_IPA, word_diction):


	articulation = {'ŋ':0,'k':0,'ɡ':0,'x':0,'w':0,'h':0,'tʃ':1,'dʒ':1,'tʃ':1,'dʒ':1,'ʃ':1,'ʒ':1,'ɹ':1,'j':1,'n':2,'t':2,'d':2,'s':2,'z':2,'l':2,'θ':3,'ð':3,'m':4,'p':4,'b':4,'f':4,'v':4, 'ç': 1, 'ɾ': 1}
	manor = {'ŋ':2,'k':0,'ɡ':0,'x':0,'w':-1,'h':0,'tʃ':1,'dʒ':1,'tʃ':1,'dʒ':0,'ʃ':1,'ʒ':0,'ɹ':-1,'j':-1,'n':2,'t':1,'d':0,'s':1,'z':0,'l':-1,'θ':1,'ð':0,'m':2,'p':1,'b':0,'f':1,'v':0, 'ç':3 , 'ɾ': 4}
	occlusion = {'ŋ': -1, 'k': 0, 'ɡ': 0, 'x': 1, 'w': 2, 'h': 1, 'tʃ': 0, 'dʒ': 0,
				 'ʃ': 1, 'ʒ': 1, 'ɹ': 2, 'j': 2, 'n': -1, 't': 0, 'd': 0, 's': 1, 'z': 1, 'l': 2, 'θ': 1,'ð':1,'m':-1,'p':0,'b':0,'f':1,'v':1, 'ç': -1, 'ɾ':-1}

	IPA_vowels = ['ɪ', 'e', 'æ', 'ʌ', 'ʊ', 'ɒ', 'ə', 'o', 'i', 'ɐ', 'ɝ','u', 'a', 'ɛ', 'ɚ', 'ô', 'ɔ']
	IPA_symbols = ['ˈ', ':', '.', '̃.', 'ː', '̩', 'ˌ', ' ', '̃', '/', '\\']
	#back = 1, central = 2, front = 3
	placement = {'ɪ':2.8, 'e': 3, 'æ': 3, 'ʌ': 1, 'ʊ': 1.25, 'ɒ': 1, 'ə': 2, 'ɚ': 2, 'o': 1, 'i': 3, 'ɐ': 2, 'ɝ': 2 ,'u': 1, 'a': 3 , 'ɛ': 3, 'ô': 1, 'ɔ':1}
	rank = {'ɪ':2, 'e': 3, 'æ': 6, 'ʌ': 5, 'ʊ': 2, 'ɒ': 7, 'ə': 4, 'ɚ':4, 'o': 3, 'i': 1, 'ɐ': 6.5, 'ɝ': 6, 'u': 1, 'a': 7, 'ɛ': 5, 'ô': 3 , 'ɔ':5}
	subranks = {'ɪ':1.5, 'e': 2, 'æ': 4.25, 'ʌ': 15, 'ʊ': 2, 'ɒ': 16, 'ə': 8, 'o': 13, 'i': 1, 'ɐ': 10, 'ɝ': 9, 'u': 12, 'a': 5, 'ɛ':4, 'ɚ': 8, 'ô': 13,'ɔ': 15}
	diction_vectors = {}
	for key in word_diction.values():
		word_vectors = np.zeros((len(key), 3))
		for letters_index in range(len(key)):

			if key[letters_index] not in IPA_vowels and key[letters_index] not in IPA_symbols:
				word_vectors[letters_index][0] = articulation[key[letters_index]]
				word_vectors[letters_index][1] = manor[key[letters_index]]
				word_vectors[letters_index][2] = occlusion[key[letters_index]]
			elif key[letters_index] not in IPA_symbols:
				word_vectors[letters_index][0] = placement[key[letters_index]]
				word_vectors[letters_index][1] = rank[key[letters_index]]
				word_vectors[letters_index][2] = subranks[key[letters_index]]
			else :
				word_vectors[letters_index][0] = -10
				word_vectors[letters_index][1] = -10
				word_vectors[letters_index][2] = -10

		diction_vectors[key] = word_vectors
		# print("!")
		# print(word_vectors)


	#Vectorizes inputIPA
	word_vectors_input = np.zeros((len(input_IPA), 3))
	for letters_index in range(len(input_IPA)):
		if input_IPA[letters_index] not in IPA_vowels and input_IPA[letters_index] not in IPA_symbols:
			word_vectors_input[letters_index][0] = articulation[input_IPA[letters_index]]
			word_vectors_input[letters_index][1] = manor[input_IPA[letters_index]]
			word_vectors_input[letters_index][2] = occlusion[input_IPA[letters_index]]
		elif input_IPA[letters_index] not in IPA_symbols:
			word_vectors_input[letters_index][0] = placement[input_IPA[letters_index]]
			word_vectors_input[letters_index][1] = rank[input_IPA[letters_index]]
			word_vectors_input[letters_index][2] = subranks[input_IPA[letters_index]]
		else :
			word_vectors_input[letters_index][0] = -10
			word_vectors_input[letters_index][1] = -10
			word_vectors_input[letters_index][2] = -10

	word_vectors_input = np.true_divide(word_vectors_input, 1.05) #make the matrix look similar to predictive matrices coming from ML model.
	print("Matrix of the input_IPA is :", word_vectors_input)


	min_val = 9999
	min_key = 0
	sim = 9999
	for key in diction_vectors.keys():
		a, b = diction_vectors[key], word_vectors_input
		if len(a) == len(b):
			sim = np.linalg.norm(a-b)
			print(sim)
		if sim < min_val:
			min_key = key
			min_val = sim
	print(min_key)
	#
	# print("!!")
	# a, b = diction_vectors['/siˈætl̩/'], word_vectors
	# sim = np.linalg.norm(a-b)
	# print(sim)

	# sim_sparse = 1 - sp.distance.cdist(diction_vectors(['/siˈætl̩/']), word_vectors, 'cosine')
	# print(sim_sparse)


#splice("OpenBCI-RAW-2020-11-16_01-42-35.txt")

web_parser()


#recordData()