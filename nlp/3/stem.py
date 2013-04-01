import re
import nltk
from nltk.corpus import gutenberg, nps_chat
def stem(word):
    regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
    stem,suffix = re.findall(regexp, word)[0]
    return stem

print stem('processing')

moby = nltk.Text(gutenberg.words('melville-moby_dick.txt'))
print moby.findall(r"<a> (<.*>) <man>")

chat = nltk.Text(nps_chat.word())
print chat.findall(r"<.*><.*><bro>")
