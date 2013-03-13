def getEdges(path):
    f = open(path)
    for line in f.readlines():
        yield line.split()


