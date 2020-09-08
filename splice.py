import csv
import numpy as np
import pickle

def processing(sample):
	# TODO: perform MNE processing here
	return sample

def splice(filename, channels=8, hz=250, chunkSecs=2):
	chunks, curr = [], [] # all chunks, current reading sample
	with open(filename, 'r') as file:
		f = csv.reader(file)
		for i in range(5): # skip first few lines
			next(f)

		for l in f:
			if len(curr) == chunkSecs * hz: # if done with one sample
				chunks.append(processing(curr)) # add to list of all chunks
				curr = [] # prepare for next sample
			curr.append([float(x) for x in l[1:channels + 1]]) # add channel recording to current sample

	data = np.asarray(chunks) # convert chunks to np array
	pickle.dump(data, open('%s.pkl' % filename.split('.')[0], 'wb'))
	print('Extracted %d chunks from %s' % (data.shape[0], filename))

splice('OpenBCI-RAW-2020-09-04_11-46-16-YES.txt')