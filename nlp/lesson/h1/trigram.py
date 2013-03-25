from __future__ import division
import sys


def count_tag_and_word(count_file):
    tag_count={}
    tag_word_count={}
    bigram_count={}
    trigram_count = {}
    emission_rate = {}
    q_rate = {}
    for line in count_file:
        list = line.split()
        try:
            if list[1] == 'WORDTAG':
                tag_count[list[2]] = tag_count.get(list[2], 0) + int(list[0])
                tag_word_count.setdefault(list[3],{})[list[2]] = int(list[0])
            elif list[1] == '2-GRAM':
                bigram_count[list[2], list[3]]  = int(list[0])
            elif list[1] == '3-GRAM':
                trigram_count.setdefault(list[4], {})[list[2], list[3]] = int(list[0])
        except:
            pass

    for word in tag_word_count.iterkeys():
        for tag in tag_word_count[word].iterkeys():
            emission_rate.setdefault(word, {})[tag] = tag_word_count[word][tag] / tag_count[tag]
    #emission_rate.setdefault('**',{})['**'] = 1
    #emission_rate.setdefault('STOP',{})['STOP'] = 1

    for trigram in trigram_count.iterkeys():
        for bi in trigram_count[trigram].iterkeys():
            q_rate.setdefault(trigram, {})[bi] = trigram_count[trigram][bi] / bigram_count[bi]

    return emission_rate, q_rate

def sentences(test_file):
    sentence = []
    for line in test_file:
        if line != '\n':
            sentence.append(line[:-1])
        else:
            if len(sentence) > 0:
                yield sentence
            sentence = []
            yield line
    if len(sentence) > 0:
        yield sentence

if __name__ == "__main__":
    try:
        dev_file = file('gene.test',"r")
        count_file = file('gene.counts',"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile.\n")
        sys.exit(1)

    emission_rate,q_rate = count_tag_and_word(count_file)
    write_lines = []
    for sentence in sentences(dev_file):
        if sentence == '\n':
            write_lines.append('\n')
            continue
        length = len(sentence)
        pi = {}
        pi.setdefault(0, {})['*','*'] = 1,None
        s = [None for i in range(len(sentence))]

        for v in emission_rate.get(sentence[0], emission_rate['_RARE_']).iterkeys():
            rate = pi[0].get(('*', '*'),(0,0))[0] * q_rate[v].get(('*', '*'), 0) * emission_rate.get(sentence[0], emission_rate['_RARE_'])[v]
            pi.setdefault(1, {})['*',v] = rate,'*'

        for v in emission_rate.get(sentence[1], emission_rate['_RARE_']).iterkeys():
            for u in emission_rate.get(sentence[0], emission_rate['_RARE_']).iterkeys():
                rate = pi[1].get(('*', u),(0,0))[0] * q_rate[v].get(('*', u), 0) * emission_rate.get(sentence[1], emission_rate['_RARE_'])[v]
                pi.setdefault(2, {})[u,v] = rate,'*'


        for i in range(2,length):
            for v in emission_rate.get(sentence[i], emission_rate['_RARE_']).iterkeys():
                for u in emission_rate.get(sentence[i-1], emission_rate['_RARE_']).iterkeys():
                    max_rate = 0
                    for w in emission_rate.get(sentence[i-2], emission_rate['_RARE_']).iterkeys():
                        rate = pi[i].get((w, u),(0,0))[0] * q_rate[v].get((w, u), 0) * emission_rate.get(sentence[i], emission_rate['_RARE_'])[v]
                        if rate >= max_rate:
                            max_rate = rate
                            pi.setdefault(i+1, {})[u,v] = max_rate,w
                    #if max_rate == 0:
                    #    pi[i+1][u,v] = 0.000000001, pi[i+1][u,v][1]

        max_rate = 0
        for v in emission_rate.get(sentence[length-1], emission_rate['_RARE_']).iterkeys():
            for u in emission_rate.get(sentence[length-2], emission_rate['_RARE_']).iterkeys():
                rate = pi[length].get((u,v),(0,0))[0] * q_rate['STOP'].get((u,v),0)
                if rate >= max_rate:
                    max_rate = rate
                    y_n1, y_n = u, v

        s[length-1] = y_n
        s[length-2] = y_n1
        for i in range(length-3, -1, -1):
            s[i] = pi[i+3][y_n1, y_n][1]
            y_n = y_n1
            y_n1 = s[i]

        for i in range(len(s)):
            write_lines.append(sentence[i] + ' ' + s[i] + '\n')
        #write_lines.append('\n')
    write_lines.append('\n')
    out_file = open("gene_test.p1.out", 'w')
    out_file.writelines(write_lines)





