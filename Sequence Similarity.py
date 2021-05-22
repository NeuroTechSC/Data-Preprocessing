import difflib

a = 'email user this email address customer'
b = 'email mail address netmail'

seq = difflib.SequenceMatcher(None,a,b)
print(seq.ratio()*100)