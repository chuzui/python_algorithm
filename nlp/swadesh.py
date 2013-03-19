from nltk.corpus import swadesh

fe2en = swadesh.entries(['en', 'fr'])

translate = dict(fe2en)
print translate['I']