__author__ = 'Administrator'

from numpy import *
import operator

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0,0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffmat = tile(inX, (dataSetSize, 1)) - dataSet
    sqDiffMat = diffmat ** 2
    sqDistance = sqDiffMat.sum(axis = 1)
    distance = sqDistance ** 0.5
    sortedDistIndicies = distance.argsort()

    classCount = {}
    for i in range(k):
        votelLabel = labels[sortedDistIndicies[i]]
        classCount[votelLabel] = classCount.get(votelLabel, 0) + 1
    sortedDistIndicies = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedDistIndicies[0][0]

def file2matrix(filename):
    fr = open(filename)
    arrayLines = fr.readlines()
    numOfLines = len(arrayLines)
    returnMat = zeros((numOfLines, 3))
    classLabelVector = {}
    index = 0

    for line in arrayLines:
        l = line.strip().split('\t')
        returnMat[index, :] = l[0:3]
        classLabelVector.append(int(l[-1]))
        index += 1
    return returnMat, classLabelVector


group, labels = createDataSet()
print classify0([0, 0], group, labels, 3)