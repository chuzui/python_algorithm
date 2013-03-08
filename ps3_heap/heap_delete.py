from heap import *

class heap_delete(heap):
    def delete(self, i):
        if self.heapsize < 1 or i > self.heapsize:
            print 'error'
        elif self.heapsize == 1:
            self.heapsize -= 1
            self.A.pop()
        else:
            self.A[i] = self.A.pop()
            self.heapsize -= 1
            self.min_heapify(i)


