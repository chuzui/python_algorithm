#!/usr/bin/python
import unittest
import docdist7

class TestPS1(unittest.TestCase):
    def setUp(self):
        pass

    def test1(self):
        ans = docdist7.calculate_angle_from_files('t1.verne.txt', 't2.bobsey.txt')
        self.assertAlmostEqual(ans, 0.53338963892153224)

    def test2(self):
        ans = docdist7.calculate_angle_from_files('t2.bobsey.txt', 't9.bacon.txt')
        self.assertAlmostEqual(ans, 0.52464214746385918)

    def test3(self):
        ans = docdist7.calculate_angle_from_files('t8.shakespeare.txt', 't9.bacon.txt')
        self.assertAlmostEqual(ans, 0.55090929545369682)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPS1)
    unittest.TextTestRunner(verbosity=2).run(suite)
