import nltk

with open('2554.txt', 'r') as corpus_file:
    fdisk = nltk.FreqDist(ch.lower() for line in corpus_file for ch in line if ch.isalpha())

fdisk.plot()