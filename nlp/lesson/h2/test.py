__author__ = 'chuzui'
import sys
import re
f = open('test.txt', 'r')

for line in f:
    sys.stdout.write(eval(line))