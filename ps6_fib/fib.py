#!/usr/bin/python

def fib_recursive(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib_recursive(n - 1) + fib_recursive(n - 2)


def fib_memoize(n, mem={}):
    if mem.has_key(n):
        return mem[n]
    if n == 0:
        mem[0] = 0
        return 0
    elif n == 1:
        mem[1] = 1
        return 1
    else:
        re = fib_memoize(n - 1,mem) + fib_memoize(n-2, mem)
        mem[n] = re
        return re


def fib_bottom_up(n):
    return 'NOT_IMPLEMENTED'

def fib_in_place(n):
    return 'NOT_IMPLEMENTED'
