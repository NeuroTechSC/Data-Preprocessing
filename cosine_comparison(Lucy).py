import numpy as np 
import math

a = np.array([1,2,3])
b = np.array([2,3,4])
i = np.array([3,4,5])
w = np.array([7,8,9])
def cosine_comparison(a,b):
  product = np.dot(a,b)
  mag_a = math.sqrt(sum(pow(num,2) for num in a))
  mag_b = math.sqrt(sum(pow(num,2)for num in b))
  mag_product = mag_a * mag_b
  final_score = product / mag_product
  print(final_score)
a_b = cosine_comparison(a,b)
a_i = cosine_comparison(a,i)
a_w = cosine_comparison(a,w)
b_i = cosine_comparison(b,i)
b_w = cosine_comparison(b,w)
i_w = cosine_comparison(i,w)