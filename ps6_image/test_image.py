#!/usr/bin/python
import unittest
import sys
import ResizeableImage

if sys.hexversion < 0x02050000:
    print "6.006 code was designed for Python 2.5, and you are running " + \
          "an older version. http://python.org/download"
    sys.exit()

class TestImage(unittest.TestCase):

    def test1_small(self):
        """small test"""
        self.image_test('sunset_small.png', 23147)

    def test2_large(self):
        """large test"""
        self.image_test('sunset_full.png', 26010)

    def image_test(self, filename, cost):
        im = ResizeableImage.ResizeableImage(filename)
        seam = im.best_seam()
        seam.sort(lambda x,y: cmp(x[1],y[1])) # Sort by height.
        self.assertEqual(im.height, len(seam), 'Seam wrong size.')
        for i in range(1, len(seam)):
            self.assertTrue(abs(seam[i][0]-seam[i-1][0]) <= 1, \
                            'Not a proper seam.')
            self.assertEqual(i, seam[i][1], 'Not a proper seam.')
        
        total = sum([im.energy(coord[0], coord[1]) for coord in seam])
        self.assertEqual(total, cost)
            
if __name__ == '__main__':
    unittest.main(argv = unittest.sys.argv + ['--verbose'])
