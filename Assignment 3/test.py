arr = []
with open('test.txt') as fp:
    for line in fp:
    	for word in line.split():
    		word = ''.join(c for c in word if c not in ' ()[]\/|.-,\'\"')
    		word = "'{}'".format(word)
    		arr.append(word)
print ','.join(arr)


