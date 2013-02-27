# docdist7.py
# Author: Ronald L. Rivest
# Date Last Modified: February 14, 2007
# Changelog:
#   Version 1: 
#     Initial version
#   Version 2:
#     Added profiling to get routine timings
#   Version 3:
#     Changed concatenate to extend in get_words_from_line_list
#   Version 4:
#     Changed count_frequency to use dictionaries instead of lists
#   Version 5:
#     Change get_words_from_string to use string translate and split
#   Version 6:
#     Changed sorting from insertion sort to merge sort
#   Version 7:
#     Changed metric for use in PS1
#
# Usage:
#    docdist7.py filename1 filename2
#     
# This program computes the "distance" between two text files
# as the angle between their word frequency vectors (in radians).
#
# For each input file, a word-frequency vector is computed as follows:
#    (1) the specified file is read in
#    (2) it is converted into a list of alphanumeric "words"
#        Here a "word" is a sequence of consecutive alphanumeric
#        characters.  Non-alphanumeric characters are treated as blanks.
#        Case is not significant.
#    (3) for each word, its frequency of occurrence is determined
#    (4) the word/frequency lists are sorted into order alphabetically
#

import math
    # math.acos(x) is the arccosine of x.
    # math.sqrt(x) is the square root of x.

import string
    # string.join(words,sep) takes a given list of words,
    #    and returns a single string resulting from concatenating them
    #    together, separated by the string sep .
    # string.lower(word) converts word to lower-case

import sys

##################################
# Operation 1: read a text file ##
##################################
def read_file(filename):
    """ 
    Read the text file with the given filename;
    return a list of the lines of text in the file.
    """
    try:
        fp = open(filename)
        L = fp.readlines()
    except IOError:
        print "Error opening or reading input file: ",filename
        sys.exit()
    return L

#################################################
# Operation 2: split the text lines into words ##
#################################################
def get_words_from_line_list(L):
    """
    Parse the given list L of text lines into words.
    Return list of all words found.
    """

    word_list = []
    for line in L:
        words_in_line = get_words_from_string(line)
        # Using "extend" is much more efficient than concatenation here:
        word_list.extend(words_in_line)
    return word_list


# this line is sometimes needed because of a unicode bug (apparently)
ll = min(len(string.uppercase), len(string.lowercase))
# global variables needed for fast parsing
# translation table maps upper case to lower case and punctuation to spaces
translation_table = string.maketrans(string.punctuation+string.uppercase[:ll],
                                     " "*len(string.punctuation)+string.lowercase[:ll])

def get_words_from_string(line):
    """
    Return a list of the words in the given input string,
    converting each word to lower-case.

    Input:  line (a string)
    Output: a list of strings 
              (each string is a sequence of alphanumeric characters)
    """
    line = line.translate(translation_table)
    word_list = line.split()
    return word_list

##############################################
# Operation 3: count frequency of each word ##
##############################################
def count_frequency(word_list):
    """
    Return a list giving pairs of form: (word,frequency)
    """
    D = {}
    for new_word in word_list:
        if D.has_key(new_word):
            D[new_word] = D[new_word]+1
        else:
            D[new_word] = 1
    return D.items()

###############################################################
# Operation 4: sort words into alphabetic order             ###
###############################################################
def merge_sort(A):
    """
    Sort list A into order, and return result.
    """
    n = len(A)
    if n==1: 
        return A
    mid = n//2     # floor division
    L = merge_sort(A[:mid])
    R = merge_sort(A[mid:])
    return merge(L,R)

def merge(L,R):
    """
    Given two sorted sequences L and R, return their merge.
    """
    i = 0
    j = 0
    answer = []
    while i<len(L) and j<len(R):
        if L[i]<R[j]:
            answer.append(L[i])
            i += 1
        else:
            answer.append(R[j])
            j += 1
    if i<len(L):
        answer.extend(L[i:])
    if j<len(R):
        answer.extend(R[j:])
    return answer

def insertion_sort(A):
    """
    Sort list A into order, in place.

    From Cormen/Leiserson/Rivest/Stein,
    Introduction to Algorithms (second edition), page 17,
    modified to adjust for fact that Python arrays use 
    0-indexing.
    """
    for j in range(len(A)):
        key = A[j]
        # insert A[j] into sorted sequence A[0..j-1]
        i = j-1
        while i>-1 and A[i]>key:
            A[i+1] = A[i]
            i = i-1
        A[i+1] = key
    return A
    
#############################################
## compute word frequencies for input file ##
#############################################
def word_frequencies_for_file(filename):
    """
    Return alphabetically sorted list of (word,frequency) pairs 
    for the given file.
    """

    line_list = read_file(filename)
    word_list = get_words_from_line_list(line_list)
    freq_mapping = count_frequency(word_list)
    freq_mapping = merge_sort(freq_mapping)

    print "File",filename,":",
    print len(line_list),"lines,",
    print len(word_list),"words,",
    print len(freq_mapping),"distinct words"

    return freq_mapping

from ps1 import inner_product
from ps1 import vector_angle

def calculate_angle_from_files(filename_1, filename_2):
    sorted_word_list_1 = word_frequencies_for_file(filename_1)
    sorted_word_list_2 = word_frequencies_for_file(filename_2)
    distance = vector_angle(sorted_word_list_1,sorted_word_list_2)
    return distance

def main():
    if len(sys.argv) != 3:
        print "Usage: docdist7.py filename_1 filename_2"
    else:
        filename_1 = sys.argv[1]
        filename_2 = sys.argv[2]
        distance = calculate_angle_from_files(filename_1, filename_2)
        print "The distance between the documents is: %0.6f (radians)"%distance

if __name__ == "__main__":
    import profile
    profile.run("main()")

    
    



