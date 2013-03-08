def parent(i):
    return i/2

def left(i):
    return 2*i

def right(i):
    return 2*i+1

class heap:
    """
    Python implementation of minheap, using 1-based indexing.
    Adapted from CLRS.
    """

    def __init__(self):
        self.A = [None] # To make the heap 1-based, None is stuck in slot 0.
        self.heapsize = 0
        
    def __getitem__(self, i):
        return self.A[i]

    def min_heapify(self, i):
        l = left(i)
        r = right(i)
        smallest = i
        if l <= self.heapsize and self.A[l] < self.A[i]:
            smallest = l
        if r <= self.heapsize and self.A[r] < self.A[smallest]:
            smallest = r
        if smallest != i:
            self._swap(i, smallest)
            self.min_heapify(smallest)

    def decrease_key(self, i, key):
        if key > self.A[i]:
            print "error: new key is larger than current key"
            return
        self.A[i] = key
        while i > 1 and self.A[parent(i)] > self.A[i]:
            self._swap(i, parent(i))
            i = parent(i)

    def insert(self, key):
        self.heapsize += 1
        self.A.append(positive_infinity())
        self.decrease_key(self.heapsize, key)

    def extract_min(self):
        if self.heapsize < 1:
            print "error: empty heap"
            return
        min = self.A[1]
        self.A[1] = self.A[self.heapsize]
        self.heapsize -= 1
        self.A.pop()
        self.min_heapify(1)
        return min
    
    def _swap(self, index1, index2):
        self.A[index1],self.A[index2] = self.A[index2],self.A[index1]


class positive_infinity:
    "bigger than any object other than itself"
    def __cmp__(self, other):
        if isinstance(other, self.__class__):
            return 0
        return 1

class negative_infinity:
    "smaller than any object other than itself"
    def __cmp__(self, other):
        if isinstance(other, self.__class__):
            return 0
        return -1
