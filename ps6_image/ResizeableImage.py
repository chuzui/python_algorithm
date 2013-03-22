#!/usr/bin/python

import ImageMatrix

class ResizeableImage(ImageMatrix.ImageMatrix):

    def best_seam(self):
        dp = {}
        path={}
        for i in range(self.width):
            dp[i, 0] = self.energy(i, 0)
        #for j in range(self.height):
            #3dp[0, j] = self.energy(0, j)

        for j in range(1, self.height):
            for i in range(0,self.width):
                min_value = dp[i, j-1]
                p = i, j-1
                if dp.has_key((i-1, j-1)) and dp[i-1,j-1] < min_value:
                    min_value = dp[i-1,j-1]
                    p = i-1,j-1
                if dp.has_key((i+1,j-1)) and dp[i+1,j-1] < min_value:
                    min_value = dp[i+1,j-1]
                    p = i+1, j-1
                dp[i,j] = min_value + self.energy(i,j)
                path[i,j] = p

        min = dp[0,self.height-1]
        col = 0
        for i in range(self.width):
            if dp[i,self.height-1] < min:
                min = dp[i, self.height-1]
                col = i

        re = []
        cur = col,self.height-1
        re.append(cur)
        while path.has_key(cur):
            cur = path[cur]
            re.append(cur)
        return re

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
