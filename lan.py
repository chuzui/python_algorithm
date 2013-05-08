__author__ = 'chuzui'

f = open('1.txt')

d = {}
for l in f:
    l = l.decode('gbk')
    for i in range(len(l) - 1):
         d[l[i], l[i+1]] = d.get((l[i], l[i+1]), 0) + 1

l = list()
for key in d.iterkeys():
    if d[key] > 10:
        print ''.join(key), d[key]