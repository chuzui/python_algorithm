from __future__ import division
import sys


def count_tag_and_word(count_file):
    tag_count={}
    tag_word_count={}
    for line in count_file:
        list = line.split()
        try:
            if list[1] == 'WORDTAG':
                tag_count[list[2]] = tag_count.get(list[2], 0) + int(list[0])
                tag_word_count.setdefault(list[3],{})[list[2]] = int(list[0])
        except:
            pass
    return tag_count, tag_word_count

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
    f = open('gene_dev.p1.out', 'w')
    f.writelines(write_lines)



if __name__ == "__main__":
    try:
        dev_file = file('gene.dev',"r")
        count_file = file('gene.counts',"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile.\n")
        sys.exit(1)

    tag_count, tag_word_count = count_tag_and_word(count_file)
    evaluate(dev_file, tag_count, tag_word_count)
