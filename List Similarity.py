from collections import Counter
import math

list_A = ['email','user','this','email','address','customer']
list_B = ['email','mail','address','netmail']

counterA = Counter(list_A)
counterB = Counter(list_B)

def counter_cosine_similarity(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

print(counter_cosine_similarity(counterA, counterB) * 100)