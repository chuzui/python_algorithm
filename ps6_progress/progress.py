#!/usr/bin/python
import math
def longest_increasing_subsequence(scores):
    n = len(scores)
    if n == 0:
        return []
    L = 0
    m = [0]
    p = [0]

    for i in range(n):
        j = binary_search(scores,m, 1, len(m)-1, scores[i])
        p.append(m[j])
        if j == L or scores[i] < scores[m[j+1]-1]:
            if j == L:
                m.append(i+1)
            else:
                m[j+1] = i+1
            L = max(L, j+1)
    last = m[L]
    re = []
    while last != 0:
        re.append(scores[last-1])
        last = p[last]
    re.reverse()
    return re


def binary_search(scores, m, start, end, value):
    for i in range(end,start-1,-1):
        if value > scores[m[i]-1]:
            return i
    return 0

#print longest_increasing_subsequence([1,2,3])