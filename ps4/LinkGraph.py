from enum import Color
from Queue import Queue
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

    def BFS(self, index):
        n = self._v
        matrix = self._matrix
        color = [Color.WHITE for i in range(n)]
        #d = [None for i in range(n)]
        queue = Queue();
        color[index] = Color.GRAY
        queue.put(index)
        while queue.qsize() > 0:
            cur_index = queue.get()
            print cur_index
            for node in matrix[cur_index].next():
                if color[node.getIndex()] == Color.WHITE:
                    queue.put(node.getIndex())
                    color[node.getIndex()] = Color.GRAY
# for column_num,i in enumerate(self._matrix[cur_index]):
            #     if i == 1 and color[column_num] == Color.WHITE:
            #         queue.put(column_num)
            #         color[column_num] = Color.GRAY
            color[node.getIndex()] = Color.BLACK

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

ma = LinkGraph(5, False)

ma.addEdge(0,1)
ma.addEdge(0,4)
ma.addEdge(1,2)
ma.addEdge(1,3)
ma.addEdge(1,4)
ma.addEdge(2,3)
ma.addEdge(3,4)
ma.BFS(0)
#ma.transpose()
print ma