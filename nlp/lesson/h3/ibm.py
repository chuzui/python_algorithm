from __future__ import division
import sys
import pickle
def readFile(path):
    l = []
    try:
        f = open(path, 'r')
        for line in f.readlines():
            l.append(line.split())

    except:
        sys.stderr.write('open path error')
    return l

def initT(srcList, desList):
    t = {}
    n = len(srcList)
    a = {}
    setSrcWord = set()
    for k in range(n):
        for desWord in desList[k]:
            for srcWord in srcList[k]:
                a.setdefault(desWord, set()).add(srcWord)
                setSrcWord.add(srcWord)

    for desWord in a.iterkeys():
        rate = 1 / len(a[desWord])
        for srcWord in a[desWord]:
            t.setdefault(srcWord, {})[desWord] = rate

    nullRate = 1 / len(setSrcWord)
    for srcWord in t.iterkeys():
        t[srcWord]['NULL'] = nullRate

    # for k in range(n):
    #     for i, srcWord in enumerate(srcList[k]):
    #         for j, desWord in enumerate(desList[k]):
    #             t.setdefault(srcWord, {})[desWord] = 0
    # for srcWord in t.iterkeys():
    #     rate = 1 / (len(t[srcWord]) + 1)
    #     for desWord in t[srcWord].iterkeys():
    #         t[srcWord][desWord] = rate
    #     t[srcWord]['NULL'] = rate

    return t

def initQ(srcList, desList):
    q = {}
    n = len(srcList)
    for k in range(n):
        l = len(desList[k])
        m = len(srcList[k])
        rate = 1 / (l + 1)
        if l == 0:
            continue
        for i in range(1, m+1):
            for j in range(l+1):
                q.setdefault(j, {})[i,l,m] = rate
    return q


def initC(c):
    for key in c.iterkeys():
        if not isinstance(c[key], dict):
            c[key] = 0
        else:
            for key2 in c[key].iterkeys():
                c[key][key2] = 0




def ibm1(srcList, desList):
    T = 5
    t = initT(srcList, desList)
    n = len(srcList)
    c = {}
    for p in range(T):
        initC(c)
        for k in range(n):
            for i, srcWord in enumerate(srcList[k]):
                if len(desList[k]) == 0:
                    continue
                s = 0
                for j, desWord in enumerate(desList[k]):
                    s += t[srcWord].get(desWord, 0)
                s += t[srcWord]['NULL']
                for j, desWord in enumerate(desList[k]):
                    beta = t[srcWord].get(desWord, 0) / s
                    c[desWord, srcWord] = c.get((desWord, srcWord), 0) +  beta
                    c[desWord] = c.get(desWord, 0) + beta
                beta = t[srcWord]['NULL'] / s
                c['NULL', srcWord] = c.get(('NULL', srcWord), 0) + beta
                c['NULL'] = c.get('NULL', 0) + beta

        for fWord in t.iterkeys():
            for eWord in t[fWord].iterkeys():
                t[fWord][eWord] = c[eWord, fWord] / c[eWord]
    return t

def ibm2(srcList, desList, t):
    T = 5
    q = initQ(srcList, desList)
    n = len(srcList)
    c = {}
    for p in range(T):
        initC(c)
        for k in range(n):
            l = len(desList[k])
            m = len(srcList[k])
            for i, srcWord in enumerate(srcList[k]):
                if len(desList[k]) == 0:
                    continue
                s = 0
                for j, desWord in enumerate(desList[k]):
                    s += q[j+1].get((i+1,l,m), 0) * t[srcWord].get(desWord, 0)
                s += q[0].get((i+1,l,m),0) * t[srcWord]['NULL']
                for j, desWord in enumerate(desList[k]):
                    beta = q[j+1].get((i+1,l,m), 0) * t[srcWord].get(desWord, 0) / s
                    c[desWord, srcWord] = c.get((desWord, srcWord), 0) +  beta
                    c[desWord] = c.get(desWord, 0) + beta
                    c.setdefault(j+1, {})[i+1, l, m] = c.setdefault(j+1, {}).get((i+1, l, m), 0) + beta
                    c[i+1, l, m] = c.get((i+1, l, m), 0) + beta
                beta = t[srcWord]['NULL'] / s
                c['NULL', srcWord] = c.get(('NULL', srcWord), 0) + beta
                c['NULL'] = c.get('NULL', 0) + beta
                c.setdefault(0, {})[i+1, l, m] = c.setdefault(0, {}).get((i+1, l, m), 0) + beta
                c[i+1, l, m] = c.get((i+1, l, m), 0) + beta

        for fWord in t.iterkeys():
            for eWord in t[fWord].iterkeys():
                t[fWord][eWord] = c[eWord, fWord] / c[eWord]
        for j in q.iterkeys():
            for (i, l, m) in q[j].iterkeys():
                q[j][(i, l, m)] = c[j][i, l, m] / c[i,l,m]

    return t, q

def trans(srcList, desList, t):
    n = len(srcList)
    for k in range(n):
        l = []
        for i, iWord in enumerate(srcList[k]):
            a = 0
            maxP = t[iWord]['NULL']
            for j, jWord in enumerate(desList[k]):
                rate = t[iWord].get(jWord, 0)
                if rate > maxP:
                    a = j + 1
                    maxP = rate
            if a != 0:
                l.append([a, i+1])
        l.sort()
        for pair in l:
            print str(k+1) + ' ' + str(pair[0]) + ' ' + str(pair[1])

def trans_IBM2(srcList, desList, t, q):
    n = len(srcList)
    for k in range(n):
        pair_l = []
        l = len(desList[k])
        m = len(srcList[k])
        for i, iWord in enumerate(srcList[k]):
            a = 0
            maxP = t[iWord]['NULL'] * q[0][i+1, l, m]
            for j, jWord in enumerate(desList[k]):
                rate = t[iWord].get(jWord, 0) * q[j+1][i+1,l,m]
                if rate > maxP:
                    a = j + 1
                    maxP = rate
            if a != 0:
                pair_l.append([a, i+1])
        pair_l.sort()
        for pair in pair_l:
            print str(k+1) + ' ' + str(pair[0]) + ' ' + str(pair[1])
    pass


if __name__ == '__main__':
    corpusEsList = readFile('corpus.es')
    corpusEnList = readFile('corpus.en')
    t = ibm1(corpusEsList, corpusEnList)
    t, q = ibm2(corpusEsList, corpusEnList, t)

    rv_t = ibm1(corpusEnList, corpusEsList)
    rv_t, rv_q = ibm2(corpusEnList, corpusEsList, rv_t)

    l = [t, q, rv_t, rv_q]
    f = open("data", 'w')
    pickle.dump(l, f)

    #devEs = readFile('test.es')
    #devEn = readFile('test.en')
    #trans_IBM2(devEs, devEn, t, q)


