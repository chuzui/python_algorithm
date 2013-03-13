from enum import *
from Queue import Queue
from GraphFile import *
NUM_LENGTH = 4
class MatrixGraph:
    def __init__(self, v, isDirectred):
        self._v = v
        self._matrix = [[0 for x in range(v)] for y in range(v)]

        self._isDirected = isDirectred
        self._str2index = {}
        self._strList = [None for x in range(v)]

    def __str__(self):
        firstline =  '\b'*NUM_LENGTH + ''.join([str(i) + '\b'*(NUM_LENGTH-len(str(i))) for i in range(self._v)]) + '\n'
        lines = [str(i) + '\b'*(NUM_LENGTH-len(str(i))) + ''.join([str(self._matrix[i][j]) + '\b'*(NUM_LENGTH - len(str(self._matrix[i][j]))) for j in range(self._v)]) +'\n' for i in range(self._v)]
        return firstline + ''.join(lines)

    def addEdge(self,u,v):
        self._matrix[u][v] = 1
        if not self._isDirected:
            self._matrix[v][u] = 1

    def addStrEdge(self,u,v):
        u_index = self._add_Vertex(u)
        v_index = self._add_Vertex(v)
        self.addEdge(u_index, v_index)

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

    def DFS(self):
        self._isSimple = True
        n = self._v
        self._pre = [0 for i in range(n)]
        self._d = [0 for i in range(n)]
        self._f = [0 for i in range(n)]
        self._color = [Color.WHITE for i in range(n)]
        self._time = 0
        for i in range(n):
            if self._color[i] == Color.WHITE:
                self._dfs_visit(i)
        print self._isSimple

    def PathCount(self, u, v):
        self._is_to_v = [False for i in range(self._v)]
        self._is_to_v[self._str2index[v]] = True
        self._color = [Color.WHITE for i in range(self._v)]
        self._pathcount = 0
        self._path_search_dfs(self._str2index[u])
        print self._pathcount

    def _path_search_dfs(self,index):
        self._color[index] = Color.GRAY
        for column_num,i in enumerate(self._matrix[index]):
            if i == 1 and self._is_to_v[column_num] == True:
                self._pathcount += 1
            if i == 1 and self._color[column_num] == Color.WHITE:
                self._path_search_dfs(column_num)
            if i == 1 and self._is_to_v[column_num] == True:
                self._is_to_v[index] = True
        self._color[index] = Color.BLACK

    def _dfs_visit(self,index):
        self._color[index] = Color.GRAY
        self._time += 1
        self._d[index] = self._time
        for column_num,i in enumerate(self._matrix[index]):
            if i == 1 and self._color[column_num] == Color.WHITE:
                self._dfs_visit(column_num)
            if i == 1 and self._color[column_num] == Color.BLACK:
                self._isSimple = False
        self._color[index] = Color.BLACK
        self._time += 1
        self._f[index] = self._time
        print self._strList[index]

    def _add_Vertex(self, name):
        if not self._str2index.has_key(name):
            n = len(self._str2index)
            self._strList[n] = name
            self._str2index[name] = n
        return self._str2index[name]


ma = MatrixGraph(14, True)

for tuple in getEdges('graph.txt'):
    ma.addStrEdge(tuple[0], tuple[1])


ma.PathCount('p','v')
#ma.transpose()
print ma


