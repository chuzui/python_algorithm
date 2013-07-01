# Please fill out this stencil and submit using the provided submission script.





## Problem 1
def myFilter(L, num): return [x for x in L if x % num != 0]



## Problem 2
def myLists(L): return [list(range(1,x+1)) for x in L]



## Problem 3
def myFunctionComposition(f, g): return {x:g[f[x]] for x in f.keys()}


## Problem 4
# Please only enter your numerical solution.

complex_addition_a = 5+3j
complex_addition_b = 1j
complex_addition_c = -1 + 0.001j
complex_addition_d = 0.001 + 9j



## Problem 5
GF2_sum_1 = 1
GF2_sum_2 = 0
GF2_sum_3 = 0


## Problem 6
def mySum(L):
    c = 0;
    for x in L:
        c += x
    return c



## Problem 7
def myProduct(L):
    c = 1;
    for x in L:
        c *= x
    return c



## Problem 8
def myMin(L):
    c = L[0];
    for x in L:
        if x < c:
            c = x
    return c



## Problem 9
def myConcat(L):
    l = ''
    for x in L:
        l += x
    return l



## Problem 10
def myUnion(L):
    u = set()
    for s in L:
        u |= s
    return u

