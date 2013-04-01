import nltk
import codecs
import unicodedata
path = nltk.data.find('corpora/unicode_samples/polish-lat2.txt')
print path
f = codecs.open(path, encoding='latin2')
# latin2 line in f:
    #line = line.split()
    # print line.encode('unicode_escape')
lines = f.readlines()
line = lines[2]

print line
for c in line:
    if ord(c) > 127:
        print '%r U+%04x %s' % (c.encode('utf8'), ord(c), unicodedata.name(c))