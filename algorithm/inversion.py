__author__ = 'Administrator'

def count(a, start, end):
    if start == end:
        return 0, [a[start]]
    n = (start + end) / 2
    c1, a1 = count(a, start, n)
    c2, a2 = count(a, n+1, end)
    c3, a3 = countSplitInv(a1, a2)
    return (c1+c2+c3, a3)

def countSplitInv(a,b):
    la = len(a)
    lb = len(b)
    n = len(a) + len(b)
    c = 0
    i = 0
    j = 0
    totalArray = []
    for k in range(n):
        if i == la:
            totalArray.append(b[j])
            j += 1
            continue

        if j == lb:
            totalArray.append(a[i])
            i +=1
            continue

        if a[i] <= b[j]:
            totalArray.append(a[i])
            i +=1
        else:
            totalArray.append(b[j])
            c += la - i
            j += 1
    return c, totalArray





def inversion(a):
    c,sortedArray = count(a, 0, len(a)-1)
    return c


if __name__ == '__main__':
    f = open('IntegerArray.txt')
    a = []
    for line in f:
        a.append(int(line))

    print inversion(a)
