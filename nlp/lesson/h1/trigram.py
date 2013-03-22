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
                trigram_count[list[2],list[3],list[4]] = int(list[0])
        except:
            pass

    for word in tag_word_count.iterkeys():
        for tag in tag_word_count[word].iterkeys():
            emission_rate.setdefault(word, {})[tag] = tag_word_count[word][tag] / tag_count[tag]

    for trigram in trigram_count.iterkeys():
        q_rate[trigram] = trigram_count[trigram] / bigram_count[trigram[0], trigram[1]]

    return emission_rate, q_rate

def evaluate(dev_file, tag_count, tag_word_count):
    write_lines = []
    for line in dev_file:
        if line == '\n':
            write_lines.append(line)
            continue
        word = line.strip()
        rate = 0
        if word not in tag_word_count:
            for tag in tag_word_count['_RARE_'].iterkeys():
                if tag_word_count['_RARE_'][tag] / tag_count[tag] > rate:
                    rate = tag_word_count['_RARE_'][tag] / tag_count[tag]
                    max_tag = tag
        else:
            for tag in tag_word_count[word].iterkeys():
                if tag_word_count[word][tag] / tag_count[tag] > rate:
                    rate = tag_word_count[word][tag] / tag_count[tag]
                    max_tag = tag

        write_lines.append(word + ' ' + max_tag + '\n')
    f = open('gene_test.p1.out', 'w')
    f.writelines(write_lines)



if __name__ == "__main__":
    try:
        dev_file = file('gene.test',"r")
        count_file = file('gene.counts',"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile.\n")
        sys.exit(1)

    emission_rate,q_rate = count_tag_and_word(count_file)
    evaluate(dev_file, tag_count, tag_word_count)
