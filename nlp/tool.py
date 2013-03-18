from __future__ import division
from nltk.corpus import *


def unusual_words(texts):
    text_vocab = set(w.lower() for w in texts if w.isalpha())
    english_vocab = set(w.lower() for w in words.words())
    unusual = text_vocab.difference(english_vocab)
    return sorted(unusual)

def content_fraction(text):
    stop_words = stopwords.words('english')
    content = [w for w in text if w.lower() not in stop_words]
    return len(content) / len(text)

#print unusual_words(gutenberg.words('austen-sense.txt'))
print content_fraction(reuters.words())