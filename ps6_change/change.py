#!/usr/bin/python
class Node:
    def __init__(self, size,coin, parent):
        self._size = size
        self._parent = parent
        self._coin = coin

def make_change(denominations, C):
    l = [None for i in range(C + 1)]
    l[0] = Node(0,0,None)
    l[1] = Node(1,1,None)
    for i in range (2, C+1):
        max_size = C
        for coin in denominations:
            if i - coin > 0:
                if l[i-coin]._size + 1 < max_size:
                    max_size = l[i-coin]._size + 1
                    parent = l[i - coin]
                    select_coin = coin
            elif i-coin == 0:
                max_size = 1
                parent = None
                select_coin = coin
        l[i] = Node(max_size, select_coin, parent)

    re = []
    node = l[C]
    while node is not None:
        re.append(node._coin)
        node = node._parent
    return re



print make_change([1, 5, 10, 17], 4)
