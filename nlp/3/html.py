from __future__ import division
import nltk, stem, pprint

import urllib2


#url = "http://www.gutenberg.org/files/2554/2554.txt"
url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
req = urllib2.Request(url, headers={'User-Agent':'Chrome'})
raw = urllib2.urlopen(req).read()
with open('2284783.stm','w') as f:
    f.write(raw)
    f.close()
print len(raw)

#raw = open('2554.txt').read()

#tokens = nltk.word_tokenize(raw)
#print len(tokens)
#print tokens[:10]
