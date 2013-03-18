#!/usr/bin/python
import unittest
import fib
import sys
import time

if sys.hexversion < 0x02050000:
    print "6.006 code was designed for Python 2.5, and you are running " + \
          "an older version. http://python.org/download"
    sys.exit()

class TestFib(unittest.TestCase):

    def test1_recursive(self):
        """test fib_recursive"""
        self.small_tests(fib.fib_recursive)

    def test2_memoize(self):
        """test fib_memoize"""
        sys.setrecursionlimit(5000) # Make sure enough recursion is allowed.
        self.small_tests(fib.fib_memoize)
        self.large_tests(fib.fib_memoize)

    def test3_bottom_up(self):
        """test fib_bottom_up"""
        sys.setrecursionlimit(100) # Make sure deep recursion is not allowed.
        self.small_tests(fib.fib_bottom_up)
        self.large_tests(fib.fib_bottom_up)

    def test4_in_place(self):
        """test fib_in_place"""
        sys.setrecursionlimit(100) # Make sure deep recursion is not allowed.
        self.small_tests(fib.fib_in_place)
        self.large_tests(fib.fib_in_place)

    def small_tests(self, fib_function):
        start_time = time.time()
        self.assertEqual(fib_function(0), 0)
        self.assertEqual(fib_function(1), 1) 
        self.assertEqual(fib_function(2), 1)
        self.assertEqual(fib_function(3), 2)
        self.assertEqual(fib_function(15), 610)
        self.assertEqual(fib_function(20), 6765)
        self.assertEqual(fib_function(25), 75025)
        self.assertEqual(fib_function(30), 832040)
        end_time = time.time()
        print ''
        print 'time for small tests', end_time - start_time, 'seconds'
        
    def large_tests(self, fib_function):
        start_time = time.time()
        self.assertEqual(fib_function(35), 9227465)
        self.assertEqual(fib_function(100), 354224848179261915075)
        self.assertEqual(fib_function(987), 83428786095010233039452893451168885358856822423517291331018551725755973092961397681432523209335078083037082049842613293369652888469867204072869026512035048078160170454915915213979475203909274364258193729858)
        self.assertEqual(fib_function(2087), 6422737898709979931698185025240532918461415553200326489780073605503409793507882339227136397178802669434420093418246414586034507375610234454421498261146222456582414960044238930314118576905246386789521246770359758476798924655758088726601598123264624920213749255725526625688355926823999551761016468767173987854830025878036541765098758698007373685759324661399621726508662032801196895014300604306898507806521047550259304102036066333050399633)
        end_time = time.time()
        print 'time for large tests', end_time - start_time, 'seconds'

if __name__ == '__main__':
    unittest.main(argv = unittest.sys.argv + ['--verbose'])
