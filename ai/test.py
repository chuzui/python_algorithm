class CornersState:
    def __init__(self, position, cornersVisted=[False, False, False, False]):
        self.position = position
        self.cornersVisted = cornersVisted

    def __copy__(self):
        s = CornersState(self.position, copy.copy(self.cornersVisted))
        return s

    def __eq__(self, other):
        if other == None:
            return False
        if self.position != other.position or self.cornersVisted != other.cornersVisted:
            return False
        return True

    def __hash__(self):
        base = (self.position[0] * 2 + self.position[1]) * 2
        for cor in self.cornersVisted:
            if cor == True:
                base += 1
            base *=2
        return hash(base)

a = {}
a[CornersState((1,2), [True, True, True, True])] = 2
a[CornersState((1,2), [True, True, True, True])] = 3
print a