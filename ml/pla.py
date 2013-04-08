import random
globalcount = 0
def innerProdct(v1, v2):
    sum = 0
    for i in range(len(v1)):
        sum += v1[i] * v2[i]
    return sum

def calculateOutput(v1, v2):
    sum = innerProdct(v1,v2)
    if sum > 0:
        return 1
    else:
        return -1

LEARNING_RATE = 0.1
MAX_ITERATION = 100000
def pla(randomList, w):
    count = 0
    globalError = 1
    global globalcount
    while globalError != 0 and count <= MAX_ITERATION:
        globalError = 0
        count += 1
        globalcount += 1
        for v in randomList:
            output = calculateOutput(w, v)
            localError = v[-1] - output
            w[0] += localError * v[0] / 2
            w[1] += localError * v[1] / 2
            w[2] += localError * v[2] / 2
            globalError += (localError*localError)
    return w


for i in range(1000):
    randomList = []
    for i in range(100):
        v = (random.uniform(-1, 1), random.uniform(-1, 1))
        randomList.append((v[0], v[1], 1 , 1 if v[0] > 0 else -1))
    pla(randomList, [random.random(), random.random(), random.random()])
print globalcount
