#!/usr/bin/python

import ImageMatrix

class ResizeableImage(ImageMatrix.ImageMatrix):
    def best_seam(self):
        return 'NOT_IMPLEMENTED'

    def remove_best_seam(self):
        self.remove_seam(self.best_seam())
