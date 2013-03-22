import sys


def word_list_less_than_5(count_file):
    word_list = {}
    less_list = set()
    for line in count_file.readlines():
        list = line.split()
        if list[1] == 'WORDTAG':
            word_list[list[3]] = word_list.get(list[3], 0) + int(list[0])

    for word in word_list:
        if word_list[word] < 5:
            less_list.add(word)
    return less_list

def replace_infrequent_word(original_file, less_list):
    write_list = []
    for line in original_file:
        list = line.split()
        if len(list) == 0:
            continue
        if list[0] in less_list:
            #write_list.append(list[0] + '\b_RARE_\n')
            write_list.append('_RARE_ ' + list[1] + '\n')
        else:
            write_list.append(line)
    original_file.truncate(0)
    original_file.writelines(write_list)



def usage():
    print """
    python rare_replace.py [original_file] [count_file]
        replace infrequent words(count < 5) in the original_file with a common symbol _RARE_.
    """

if __name__ == "__main__":

    #if len(sys.argv)!=3: # Expect exactly one argument: the training data file
        #usage()
        #sys.exit(3)

    try:
        original_file = file('gene.train',"r+")
        count_file = file('gene.counts',"r")
    except IOError:
        sys.stderr.write("ERROR: Cannot read inputfile.\n")
        sys.exit(1)


    lese_list = word_list_less_than_5(count_file)
    replace_infrequent_word(original_file, lese_list)


