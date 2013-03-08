from collections import deque
from AmnesiacRollingHash import AmnesiacRollingHash
class RollingHash(AmnesiacRollingHash):
    def __init__(self, *args):
        AmnesiacRollingHash.__init__(self, *args)
        self.data = deque()

    def append(self,value):
        AmnesiacRollingHash.append(self, value)
        self.data.append(value)

    def skip(self):
        AmnesiacRollingHash.skip(self, self.data.popleft())

    def get_value(self):
        return self.hash_value