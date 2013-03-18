import copy
class Direction:
    LeftTop = 1
    Left = 2
    Top = 3

def lcs_length(l1, l2):
    m = len(l1)
    n = len(l2)

    b = [[0 for i in range(n+1)] for j in range(m+1)]
    c = [[0 if i==0 or j == 0 else None for i in range(n+1)] for j in range(m+1)]
    for i in range(1, m+1):
        for j in range(1, n+1):
            if l1[i - 1] == l2[j - 1]:
                c[i][j] = c[i-1][j-1] + 1
                b[i][j] = Direction.LeftTop
            else:
                if c[i][j-1] > c[i-1][j]:
                    c[i][j] = c[i][j-1]
                    b[i][j] = Direction.Left
                else:
                    c[i][j] = c[i-1][j]
                    b[i][j] = Direction.Top

    print c[m][n]
    print_lcs(b, l1, m, n)

def print_lcs(b,l1, i, j):
    if i == 0 or j == 0:
        return
    if b[i][j] == Direction.LeftTop:
        print_lcs(b, l1, i-1,j-1)
        print l1[i-1],
    elif b[i][j] == Direction.Top:
        print_lcs(b, l1, i-1,j)
    else:
        print_lcs(b, l1, i, j-1)

def long(l):
    m = len(l)
    b = [0 for i in range(m)]
    b[0] = 1
    for i in range(1, m):
        mid = binary_search(l, 0, i -1, l[i])
        if mid != None:
            b[i] = b[mid] + 1
        else:
            b[i] = 1
    print b[m - 1]

def binary_search(l, i, j, key):
    if j - i == 1:
        if key >= l[j]:
            return j
        if key >= l[i]:
            return i
        return None
    if j == i:
        if key >= l[i]:
            return i
        return None
    mid = (i + j) / 2
    if key >= l[mid]:
        return binary_search(l, mid, j, key)
    else:
         return binary_search(l,i, mid-1, key)




l1 = [1,0,0,1,0,1,0,1]
l2 = copy.copy(l1)
l2.sort()
lcs_length(l1, l2)

