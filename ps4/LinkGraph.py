NUM_LENGTH = 4
class LinkGraph:
    def __init__(self,v,isDirected):
        self._matrix = [Node(x) for x in range(v)]
        self._isDirected = isDirected
        self._v = v

    def __str__(self):
        n = self._v
        matrix = self._matrix
        lines = [str(i) + '\b'*(NUM_LENGTH-len(str(i))) + ':' +
                 ''.join([str(node.getIndex()) + '\b'*(NUM_LENGTH-len(str(node.getIndex())))
                          for node in matrix[i]]) +'\n' for i in range(n)]
        return ''.join(lines)

    def addEdge(self,u,v):
        self._addToEdge(u, v)
        if not self._isDirected:
            self._addToEdge(v,u)

    def _addToEdge(self,u,v):
        node = self._matrix[u]
        while node.getNext():
            node = node.getNext()
        node.setNext(Node(v))

class Node:
    def __init__(self,index):
        self._index = index
        self._next = None
        self._cur_node = self

    def __iter__(self):
        return self

    def next(self):
        if self._cur_node:
            tmp = self._cur_node
            self._cur_node = self._cur_node.getNext()
            return tmp
        else:
            self._cur_node = self
            raise StopIteration

    def getIndex(self):
        return self._index

    def setNext(self,next_node):
        self._next = next_node

    def getNext(self):
        return self._next

ma = LinkGraph(12, True)

ma.addEdge(3,5)
ma.addEdge(6,7)
#ma.transpose()
print ma
print ma