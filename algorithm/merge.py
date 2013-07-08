import math

count = 0

def merge(l, lo, mid, hi):
    global count
    global tempL
    count += 1
    for k in range(lo, hi+1):
        tempL[k] = l[k]
    i = lo
    j = mid + 1
    for k in range(lo, hi+1):
        if i > mid:
            l[k] = tempL[j]
            j += 1
        elif j > hi:
            l[k] = tempL[i]
            i+= 1
        elif tempL[i] > tempL[j]:
            l[k] = tempL[j]
            j += 1;
        else:
            l[k] = tempL[i]
            i += 1;


def mergeSort(l, lo, hi):
    if hi <= lo: return
    mid = lo + (hi - lo) / 2
    mergeSort(l, lo, mid)
    mergeSort(l, mid+1, hi)
    merge(l, lo, mid, hi)
    if count == 7:
        print l

def bottomSort(l):
    N = len(l)
    sz = 1
    while sz < N:
        for lo in range(0, N-sz, sz+sz):
            merge(l, lo, lo+sz-1, min(lo+sz+sz-1, N-1))
            if count == 7:
                print l
        sz = sz + sz


l = [99, 13, 61, 91, 53, 10, 58, 54, 40, 51, 72, 26]
l2 = [61, 83, 43, 56, 54, 63, 29, 27, 40, 42]
tempL = [0 for i in l]
bottomSort(l2)
print l2