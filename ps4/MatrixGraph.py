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

ma = MatrixGraph(12, True)

ma.addEdge(3,5)
ma.addEdge(6,7)
ma.transpose()
print ma


