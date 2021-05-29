from scipy import spatial 
import numpy as np
from numpy import dot
from numpy.linalg import norm
from sklearn.metrics.pairwise import cosine_similarity # i think this does the comparison quicker? 

'''vectors being compared'''
v1 = [1, 2, 3] # the main vecotor compared to
v2 = [3, 2, 1]
v3 = [2, 3, 1]
v4 = [4, 2, 3]

keys = ['vector 2', 'vector 3', 'vector 4'] # list of keys
simValues = [] # list for similarity values

simValues.append(1 - spatial.distance.cosine(v1, v2)) # comparing v1 to v2 and appending the similarity value to list
simValues.append(1 - spatial.distance.cosine(v1, v3)) # comparing v1 to v3 and appending the similarity value to list
simValues.append(1 - spatial.distance.cosine(v1, v4)) # comparing v1 to v4 and appending the similarity value to list

simDict = dict(zip(keys, simValues)) # create dictionary with key as vector and value as the similarity value
# print(simDict) 
highest_value = max(simDict, key = simDict.get)
print("The best match to vector 1 is: {0}.".format(highest_value))

'''another method????'''

simValues_2 = []
simValues_2.append( dot(v1, v2) / (norm(v1)*norm(v2)))
simValues_2.append( dot(v1, v3) / (norm(v1)*norm(v3)))
simValues_2.append( dot(v1, v4) / (norm(v1)*norm(v4)))

simDict_2 = dict(zip(keys, simValues_2))
highest_value2 = max(simDict_2, key = simDict_2.get)
print("The best match to vector 1 is: {0}.".format(highest_value2))

'''another method????'''
v1 = np.reshape(v1, (1, -1))
v2 = np.reshape(v2, (1, -1))
v3 = np.reshape(v3, (1, -1))
v4 = np.reshape(v4, (1, -1))

simValues_3 = []
simValues_3.append(cosine_similarity(v1, v2))
simValues_3.append(cosine_similarity(v1, v3))
simValues_3.append(cosine_similarity(v1, v4))

simDict_3 = dict(zip(keys, simValues_3))
highest_value3 = max(simDict_3, key = simDict_3.get)
print("The best match to vector 1 is: {0}.".format(highest_value3))