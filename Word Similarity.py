def word2vec(word):
    from collections import Counter
    from math import sqrt

    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))

    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]


list_A = ['email','user','this','email','address','customer']
list_B = ['email','mail','address','netmail']

for key in list_A:
    for word in list_B:
        try:
            res = cosdis(word2vec(word), word2vec(key))
            print("The cosine similarity between : {} and : {} is: {}".format(word, key, res*100))
        except IndexError:  pass