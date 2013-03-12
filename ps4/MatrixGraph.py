from enum import Color
from Queue import Queue
NUM_LENGTH = 4
class MatrixGraph:
    def __init__(self, v, isDirectred):
        self._v = v
        self._matrix = [[0 for x in range(v)] for y in range(v)]

        self._isDirectred = isDirectred

    def __str__(self):
        firstline =  '\b'*NUM_LENGTH + ''.join([str(i) + '\b'*(NUM_LENGTH-len(str(i))) for i in range(self._v)]) + '\n'
        lines = [str(i) + '\b'*(NUM_LENGTH-len(str(i))) + ''.join([str(self._matrix[i][j]) + '\b'*(NUM_LENGTH - len(str(self._matrix[i][j]))) for j in range(self._v)]) +'\n' for i in range(self._v)]
        return firstline + ''.join(lines)

    def addEdge(self,u,v):
        self._matrix[u][v] = 1
        if not self._isDirectred:
            self._matrix[v][u] = 1

    def transpose(self):
        n = self._v
        matrix = self._matrix
        for i in range(n):
            for j in range(i+1,n):
                tmp = matrix[i][j]
                matrix[i][j] = matrix[j][i]
                matrix[j][i] = tmp

    def BFS(self, index):
        n = self._v
        color = [Color.WHITE for i in range(n)]
        #d = [None for i in range(n)]
        queue = Queue();
        color[index] = Color.GRAY
        queue.put(index)
        while queue.qsize() > 0:
            cur_index = queue.get()
            print cur_index
            for column_num,i in enumerate(self._matrix[cur_index]):
                if i == 1 and color[column_num] == Color.WHITE:
                    queue.put(column_num)
                    color[column_num] = Color.GRAY
            color[cur_index] = Color.BLACK




ma = MatrixGraph(5, False)

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


