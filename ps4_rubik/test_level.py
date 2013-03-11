#!/usr/bin/python
import unittest
import level
import rubik
import time
import sys

if sys.hexversion < 0x02050000:
    print "6.006 code was designed for Python 2.5, and you are running " + \
          "an older version. http://python.org/download"
    sys.exit()

class TestLevel(unittest.TestCase):
    def testLevel0(self):
        self.level_test(0, 1)

    def testLevel1(self):
        self.level_test(1, 6)

    def testLevel2(self):
        self.level_test(2, 27)

    def testLevel3(self):
        self.level_test(3, 120)

    def testLevel4(self):
        self.level_test(4, 534)

    def testLevel5(self):
        self.level_test(5, 2256)

    def testLevel6(self):
        self.level_test(6, 8969)

    def testLevel7(self):
        self.level_test(7, 33058)

    def testLevel8(self):
        self.level_test(8, 114149)

    def testLevel9(self):
        self.level_test(9, 360508)

    def testlevel10(self):
        self.level_test(10, 930588)

### It is recommended that you use a machine with 1GB of RAM if you
### want to run the following tests.
#     def testlevel11(self):
#         self.level_test(11, 1350852)

#     def testlevel12(self):
#         self.level_test(12, 782536)

#     def testlevel13(self):
#         self.level_test(13, 90280)

#     def testlevel14(self):
#         self.level_test(14, 276)

#     def testlevel15(self):
#         self.level_test(15, 0)

    def level_test(self, l, solution):
        start_time = time.time()
        ans = level.positions_at_level(l)
        end_time = time.time()

        self.assertEqual(ans, solution)
        print 'time for level', l, end_time - start_time, 'seconds'

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestLevel)
    unittest.TextTestRunner(verbosity=2).run(suite)
