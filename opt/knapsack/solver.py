#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
from copy import copy
from Queue import PriorityQueue
import profile

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    items = int(firstLine[0])
    capacity = int(firstLine[1])

    values = []
    weights = []

    for i in range(1, items+1):
        line = lines[i]
        parts = line.split()

        values.append(int(parts[0]))
        weights.append(int(parts[1]))

    value, taken = depth(capacity, weights, values)

    # prepare the solution in the specified output format
    outputData = str(value) + ' ' + str(1) + '\n'
    outputData += ' '.join(map(str, taken))
    return outputData

def depth(k, weights, values):
    l = len(weights)
    sorted_ratios = ratios = [(values[i] / weights[i], i) for i in range(l)]
    sorted_ratios.sort(reverse=True)

    f = lambda ratios, k, start: estimate(ratios, k, start,  weights, values)

    e = f(sorted_ratios, k, 0)

    s = []

    index = sorted_ratios[0][1]
    s.append((0, 0, k, f(sorted_ratios, k, 1), [0]))
    s.append((0, values[index], k-weights[index], values[index] + f(sorted_ratios, k-weights[index], 1), [1]))
    maxV = 0
    maxToken = []
    while len(s) != 0:
        i, v, w, e, token = s.pop()

        if w >= 0:
            if i == l-1:
                if v > maxV:
                    maxV = v
                    maxToken = copy(token)
            else:
                if e > maxV:
                    index = sorted_ratios[i+1][1]
                    t1 = copy(token)
                    t1.append(0)
                    s.append((i+1, v, w, v + f(sorted_ratios, w, i+1), t1))
                    t2 = copy(token)
                    t2.append(1)
                    s.append((i+1, v+values[index], w-weights[index], v+values[index] + f(sorted_ratios, w-weights[index], i+1), t2))

    token = [0 for i in range(l)]
    for i in range(l):
        token[sorted_ratios[i][1]] = maxToken[i]

    return maxV, token

def best(k, weights, values):
    l = len(weights)
    sorted_ratios = ratios = [(values[i] / weights[i], i) for i in range(l)]
    sorted_ratios.sort(reverse=True)

    f = lambda ratios, k, start: estimate(ratios, k, start,  weights, values)

    e = f(sorted_ratios, k, 0)

    s = PriorityQueue()

    index = sorted_ratios[0][1]
    s.put((-f(sorted_ratios, k, 1), 0, 0, k, [0]))
    s.put((-values[index] - f(sorted_ratios, k-weights[index], 1), 0, values[index], k-weights[index], [1]))
    maxV = 0
    maxToken = []
    while not s.empty():
        e, i, v, w, token = s.get()

        if w >= 0:
            if i == l-1:
                if v > maxV:
                    maxV = v
                    maxToken = copy(token)
            else:
                if e < maxV:
                    index = sorted_ratios[i+1][1]
                    t1 = copy(token)
                    t1.append(0)
                    s.put((v - f(sorted_ratios, w, i+1), i+1, v, w, t1))
                    t2 = copy(token)
                    t2.append(1)
                    s.put((v-values[index] - f(sorted_ratios, w-weights[index], i+1), i+1,  v+values[index], w-weights[index], t2))

    token = [0 for i in range(l)]
    for i in range(l):
        token[sorted_ratios[i][1]] = maxToken[i]

    return maxV, token

def estimate(sorted_ratios, k, start, weights, values):
    l = len(sorted_ratios)
    tempK = k
    e = 0
    for i in range(start, l):
        index = sorted_ratios[i][1]
        if tempK > weights[index]:
            e += values[index]
            tempK -= weights[index]
        else:
            e += values[index] * (tempK / weights[index])
            tempK = 0
    return e


def ps():
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'



import sys

if __name__ == '__main__':
    #profile.run("ps()")
    ps()

