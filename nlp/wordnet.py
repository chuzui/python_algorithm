from nltk.corpus import wordnet as wn
print wn.synsets('motorcar')

print wn.synset('car.n.01').lemma_names

print wn.synsets('track')

for i in wn.synsets('color'):
    print i,i.definition