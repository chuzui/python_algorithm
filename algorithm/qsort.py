__author__ = 'chuzui'

comp_count = 0

def q_partion(a, l, r):
    p = a[l]
    lp = l+1
    for i in range(l+1, r+1):
        if a[i] <  p:
            tmp = a[lp]
            a[lp] = a[i]
            a[i] = tmp
            lp += 1
    a[l] = a[lp - 1]
    a[lp - 1] = p
    return lp-1

def choosePivotRightest(a, l, r):
    swap(a, l, r)

def choosePivotMiddle(a, l, r):
    m = (l + r) / 2
    if a[l] > a[r]:
        if a[r] < a[m] < a[l]:
            swap(a, l, m)
        elif a[m] < a[r]:
            swap(a, l, r)
    else:
        if a[l] < a[m] < a[r]:
            swap(a, l, m)
        elif a[m] > a[r]:
            swap(a, l, r)

def swap(a, s1, s2):
    tmp = a[s1]
    a[s1] = a[s2]
    a[s2] = tmp


# def q_partion_f(a, l, r):
#     p = a[r]
#     lp = r-1
#     for i in range(r-1, l-1, -1):
#         if a[i] > p:
#             tmp = a[lp]
#             a[lp] = a[i]
#             a[i] = tmp
#             lp -= 1
#     a[r] = a[lp + 1]
#     a[lp + 1] = p
#     return lp+1

def qsort(a, l, r):
    global comp_count
    if r - l < 1:
        return
    comp_count += r - l
    if r - l > 1:
         choosePivotMiddle(a, l, r)

    m = q_partion(a, l, r)
    qsort(a, l, m-1)
    qsort(a, m+1, r)

# def qsortm(a, l, r):
#     global comp_count
#     if r - l < 1:
#         return
#     if r - l > 1:
#         mid = (r + l) / 2
#
#     comp_count += r - l
#     m = q_partion_f(a, l, r)
#     qsortm(a, l, m-1)
#     qsortm(a, m+1, r)


if __name__ == '__main__':
    global comp_count
    f = open('QuickSort.txt')
    a = []
    for line in f:
        a.append(int(line))
    #a = [3,8,2,5,1,4,7,6]
    qsort(a, 0, len(a) - 1)
    print comp_count
