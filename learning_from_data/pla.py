from __future__ import division
import random
import math

def innerproduct(v, w):
    sum = 0
    for i in range(len(w)):
        sum += v[i] * w[i]
    return sum
count = 0
cc = 0
for i in range(1000):
    a = (random.uniform(-1,1), random.uniform(-1,1))
    b = (random.uniform(-1,1), random.uniform(-1,1))
    points = []
    for j in range(100):
        point = (random.uniform(-1,1), random.uniform(-1,1))
        re = (point[0] - a[0]) * ((a[1] - b[1]) / (a[0] - b[0])) + a[1]
        if point[1] > re:
            points.append((point[0], point[1],1,  1))
        else:
            points.append((point[0], point[1], 1, -1))

    w = [0,0,0]
    while True:
        count += 1
        misPoints = []
        for j in range(100):
            sum = innerproduct(points[j][:-1], w)
            if sum > 0:
                if points[j][-1] == -1:
                    misPoints.append(points[j])
            else:
                if points[j][-1] == 1:
                    misPoints.append(points[j])

        if len(misPoints) == 0:
            break
        index = random.randint(0, len(misPoints)-1)
        w[0] += misPoints[index][-1] * misPoints[index][0]
        w[1] += misPoints[index][-1] * misPoints[index][1]
        w[2] += misPoints[index][-1] * misPoints[index][2]

    for i in range(10000):
        point = [random.uniform(-1,1), random.uniform(-1,1), 1]
        re = (point[0] - a[0]) * ((a[1] - b[1]) / (a[0] - b[0])) + a[1]
        if point[1] > re:
            point.append(1)
        else:
            point.append(-1)
        sum = innerproduct(w, point[:-1])
        if sum > 0:
            if point[-1] == -1:
                cc += 1
        else:
            if point[-1] == 1:
                cc += 1

print cc / (10000 * 1000)
print count
