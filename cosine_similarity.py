from scipy import spatial
import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

a = [1, 2, 3]
b = [1, 2, 4]
c = [4, 5, 6]

ipa_dict =  {'b' : b , 'c' : c}
similarities = {}


''' WAY 1 with dictionaries '''
for key, vector in ipa_dict.items():
    cos_sim = 1 - spatial.distance.cosine(a, vector)
    similarities[key] = (cos_sim)

# way 1 (just lists)
cos_sim_ab = 1 - spatial.distance.cosine(a, b)
# similarities['b'] = (cos_sim_ab)
cos_sim_ac = 1 - spatial.distance.cosine(a, c)
# similarities['c'] = (cos_sim_ac)

print("first way values:")
print(cos_sim_ab)
print(cos_sim_ac)

best = max(similarities, key = similarities.get)
print("the most similar vector to a is " + best + "\n")



''' WAY 2 '''
cos_sim_b = np.dot(a,b)/(np.linalg.norm(a)*np.linalg.norm(b))
cos_sim_c = np.dot(a,c)/(np.linalg.norm(a)*np.linalg.norm(c))
print("second way values:")
print(cos_sim_b)
print(cos_sim_c)

''' WAY 3 (not working for me) '''
# cos_sim = cosine_similarity(a, b)
