import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy import sparse

a = np.random.random((10, 10))
b = np.random.random((10, 10))

a_sparse, b_sparse = sparse.csr_matrix(a), sparse.csr_matrix(b)

sim_sparse = cosine_similarity(a_sparse, b_sparse, dense_output=False)
print(sim_sparse)