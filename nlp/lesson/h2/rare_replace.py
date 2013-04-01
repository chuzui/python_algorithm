import sys
import re
def count_less_than_5_word_set(count_file):
    wordFreq = {}
    lessSet = set()
    for line in count_file:
        wordlist = line.split();
        if len(wordlist) > 1:
            if wordlist[1] == 'UNARYRULE':
                wordFreq[wordlist[3]] = wordFreq.get(wordlist[3], 0) + int(wordlist[0])


    for word in wordFreq.iterkeys():
        if wordFreq[word] < 5:
            lessSet.add(word)
    return lessSet

def rara_replace(source_file, lessSet):
    lessSet = map(lambda x : '"' + x + '"]', lessSet)
    # patten = '|'.join(lessSet)
    # for s in source_file:
    #     sys.stdout.write(re.sub(patten, lambda x: '_RARE_"]', s))
    s = source_file.read()
    for word in lessSet:
        s = s.replace(word, '"_RARE_"]')

    sys.stdout.write(s)

if __name__ == "__main__":
    try:
        count_file = open(sys.argv[1], 'r')
        source_file = open(sys.argv[2], 'r')
        #count_file = open("cfg.count", 'r')
        #source_file = open("parse_train.dat", 'r')
    except IOError:
        sys.stderr.write("error")

    lessSet = count_less_than_5_word_set(count_file)
    rara_replace(source_file, lessSet)
    source_file.close()