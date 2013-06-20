#!/usr/bin/python
# -*- coding: utf-8 -*-
from copy import copy
import profile


def checkConfilct(node, color, nodes_color, d):
    l = len(nodes_color)
    for w in d[node]:
        if w < l and color == nodes_color[w]:
            return False
    return True

def colorSpace(node, nodes_color, d):
    s = set(nodes_color[:node])
    for i in range(node):
        if d[node][i] == 1 and nodes_color[i] in s:
            s.remove(nodes_color[i])

    # flag = True
    # for i in range(node, len(d)):
    #     if d[node][i] == 1:
    #         flag = False
    #         break
    #
    # if flag and len(s) > 0:
    #     s = [s.pop()]
    return s

def solveIt(inputData):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = inputData.split('\n')

    firstLine = lines[0].split()
    nodeCount = int(firstLine[0])
    edgeCount = int(firstLine[1])

    edges = []
    for i in range(1, edgeCount + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    # build a trivial solution
    # every node has its own color
    solution = range(0, nodeCount)

    d = [[0 for i in range(nodeCount)] for j in range(nodeCount)]

    for v,w in edges:
        d[v][w] = 1
        d[w][v] = 1

    s = []
    s.append((1, 0, 0))
    min_colors = nodeCount + 1
    min_nodes_color = []
    nodes_color = [0 for i in range(nodeCount)]
    while len(s) != 0:
        colors_count, node, node_color = s.pop()
        if colors_count < min_colors:
            nodes_color[node] = node_color
            if node == nodeCount - 1:
                min_colors = colors_count
                min_nodes_color = copy(nodes_color)
            else:
                s.append((colors_count+1, node+1, colors_count))
                for color in colorSpace(node+1, nodes_color, d):
                    s.append((colors_count, node+1, color))
                # for color in range(colors_count-1, -1, -1):
                #     if checkConfilct(node, color, nodes_color, d):
                #         temp = copy(nodes_color)
                #         temp.append(color)
                #         s.append((colors_count, temp))

    solution = min_nodes_color

    nodeCount = min_colors
    # prepare the solution in the specified output format
    outputData = str(nodeCount) + ' ' + str(1) + '\n'
    outputData += ' '.join(map(str, solution))

    return outputData


def ps():
    if len(sys.argv) > 1:
        fileLocation = sys.argv[1].strip()
        inputDataFile = open(fileLocation, 'r')
        inputData = ''.join(inputDataFile.readlines())
        inputDataFile.close()
        print solveIt(inputData)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'



import sys

if __name__ == '__main__':
    profile.run('ps()')
    #ps()
