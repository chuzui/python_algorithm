from __future__ import division
import sys
import json

def computer_rule(count_file):
    nonterminal_count = {}
    binaryrule_count = {}
    word_to_rule_count = {}
    for line in count_file:
        wordlist = line.split();
        if len(wordlist) > 1:
            mark = wordlist[1]
            count = int(wordlist[0])
            if mark == 'NONTERMINAL':
                nonterminal_count[wordlist[2]] = count
            elif mark == "BINARYRULE":
                binaryrule_count.setdefault(wordlist[2], {})[(wordlist[3], wordlist[4])] = count
            elif mark == "UNARYRULE":
                word_to_rule_count.setdefault(wordlist[3], {})[wordlist[2]] = count

    binaryrule_rate = {}
    word_to_rule_rate = {}
    for head in binaryrule_count.iterkeys():
        for body in binaryrule_count[head].iterkeys():
            binaryrule_rate.setdefault(body, {})[head] = binaryrule_count[head][body] / nonterminal_count[head]

    for word in word_to_rule_count.iterkeys():
        for head in word_to_rule_count[word].iterkeys():
            word_to_rule_rate.setdefault(word, {})[head] = word_to_rule_count[word][head] / nonterminal_count[head]

    return binaryrule_rate, word_to_rule_rate

def cky(source_file, binaryrule_rate, word_to_rule_rate):
    def pro_word(word):
        if not word_to_rule_rate.has_key(word):
            return "_RARE_"
        return word

    def jsonToString(start, end, head):
        if start == end:
            return '["' + head + '", "' + wordlist[start] + '"]'
        else:
            midIndex, first, second = bp[start, end][head]
            return '["' + head + '", ' + jsonToString(start, midIndex, first) + ', ' + jsonToString(midIndex + 1, end, second) + ']'

    for line in source_file:
        wordlist = line.split()
        rateDict = {}
        bp = {}
        for i, word in enumerate(wordlist):
            for head in word_to_rule_rate[pro_word(word)].iterkeys():
                rateDict.setdefault((i, i), {})[head] = word_to_rule_rate[pro_word(word)][head]

        for step in range(1, len(wordlist)):
            for i in range(0, len(wordlist) - step):
                for j in range(i, i + step):
                    for first in rateDict.get((i, j), {}).iterkeys():
                        for second in rateDict.get((j+1, i+step),{}).iterkeys():
                            for head in binaryrule_rate.get((first, second), {}).iterkeys():
                                rate = binaryrule_rate[(first, second)][head] * rateDict[i,j][first] * rateDict[j+1, i+step][second]
                                if rate >= rateDict.setdefault((i, i+step),{}).get(head, 0):
                                    rateDict[i, i+step][head] = rate
                                    bp.setdefault((i, i + step), {})[head] = (j, first, second)

        sys.stdout.write(jsonToString(0, len(wordlist)-1, 'SBARQ') + '\n')

if __name__ == "__main__":
    try:
        #count_file = open(sys.argv[1], 'r')
        #source_file = open(sys.argv[2], 'r')
        #count_file = open(sys.argv[1], 'r')
        #source_file = open(sys.argv[2], 'r')
        count_file = open('parse_train.counts.out', 'r')
        source_file = open('parse_dev.dat', 'r')
    except IOError:
        sys.stderr.write("error")

    binaryRule_rate, word_to_rule_rate = computer_rule(count_file)
    cky(source_file, binaryRule_rate, word_to_rule_rate)
