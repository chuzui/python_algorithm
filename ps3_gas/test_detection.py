#!/usr/bin/python
import unittest

import cStringIO
import sys
import time
import re
import os

class TestDetection(unittest.TestCase):
  def setUp(self):
      # monkey-patch detection.py against "import mod"
      source = open('detection.py','r')
      source_lines = source.readlines()
      patched_source = open('patcheddetection.py', 'w')
      for line in source_lines:
          if (re.compile("^[^#]*import.*\sgas\s").search(line) is None):
              patched_source.write(line)
          else:
              patched_source.write("import gas\ngas.detect_collisions = detect_collisions\n")
      patched_source.close()
      global detection
      import patcheddetection as detection

  def tearDown(self):
      # remove the monkey-patched detection.py
      if os.path.exists('patcheddetection.pyc'):
          os.remove('patcheddetection.pyc')
      if os.path.exists('patcheddetection.py'):
        os.remove('patcheddetection.py')
  
  def timed_auto_simulate(self, test_name, number_balls, steps):
      "Runs the gas simulation in headless mode (timed)"
      start_time = time.time()
      return_value = self.auto_simulate(number_balls, steps)
      end_time = time.time()
      print 'Time for test', test_name + ':', end_time - start_time, 'seconds'
      return return_value

  def auto_simulate(self, number_balls, steps):
      "Runs the gas simulation in headless mode"      
      
      # monkey-patch the gas simulation to 'reboot'      
      detection.gas.balls = []                       # list of balls
      detection.gas.number_balls = number_balls               # number of balls
      detection.gas.speed = 24.0                     # world units per simulation step
      detection.gas.infrequent_display = False       # True if ball shown only once/second or so
                                       #    ('d' flips this), to save CPU time
                                       # -- automatically on if no GUI
      detection.gas.autopause_period = steps         # How often to pause automatically
      detection.gas.paused = False                   # True if steps are running
      detection.gas.total_collisions = 0             # total collisions counted
      detection.gas.total_steps = 0                  # total simulation steps
      detection.gas.full_screen = False              # Full-screen pygame video mode
      detection.gas.gui = detection.gas.GUI_NONE
            
      # supress program output so that stdout doesn't have garbage
      old_stdout = sys.stdout
      sys.stdout = cStringIO.StringIO()
       
      # simulate keyboard input by monkey-patching stdin
      old_stdin = sys.stdin
      sys.stdin = cStringIO.StringIO()
      sys.stdin.write(str(number_balls) + "\n" + str(steps) + "\n" + "q\n")
      sys.stdin.seek(0)
      
      detection.gas.main()
      
      # restore normal I/O
      sys.stdin = old_stdin
      sys.stdout = old_stdout
            
      return detection.gas.total_collisions
  
  def test_1_short(self):
      "Sanity check"
      answer = self.timed_auto_simulate("(20, 10)", 20, 10)
      self.assertEqual(answer, 18)

  def test_2_small(self):
      "Small test: 20 balls"
      answer = self.timed_auto_simulate("(20, 20)", 20, 20)
      self.assertEqual(answer, 29)
      answer = self.timed_auto_simulate("(20, 50)", 20, 50)
      self.assertEqual(answer, 64)
      answer = self.timed_auto_simulate("(20, 70)", 20, 70)
      self.assertEqual(answer, 86)
      answer = self.timed_auto_simulate("(20, 80)", 20, 80)
      self.assertEqual(answer, 95)

  # def test_3_medium(self):
  #     "Medium test: 200 balls"
  #     answer = self.timed_auto_simulate("(200, 20)", 200, 20)
  #     self.assertEqual(answer, 325)
  #     answer = self.timed_auto_simulate("(200, 50)", 200, 50)
  #     self.assertEqual(answer, 571)
  #     answer = self.timed_auto_simulate("(200, 70)", 200, 70)
  #     self.assertEqual(answer, 741)
  #     answer = self.timed_auto_simulate("(200, 80)", 200, 80)
  #     self.assertEqual(answer, 846)

  # def test_4_large(self):
  #     "Large test: 2000 balls"
  #     answer = self.timed_auto_simulate("(2000, 20)", 2000, 20)
  #     self.assertEqual(answer, 3277)
  #     answer = self.timed_auto_simulate("(2000, 50)", 2000, 50)
  #     self.assertEqual(answer, 5880)
  #     answer = self.timed_auto_simulate("(2000, 70)", 2000, 70)
  #     self.assertEqual(answer, 7612)
  #     answer = self.timed_auto_simulate("(2000, 80)", 2000, 80)
  #     self.assertEqual(answer, 8480)
    
if __name__ == '__main__':
  suite = unittest.TestLoader().loadTestsFromTestCase(TestDetection)
  unittest.TextTestRunner(verbosity=2).run(suite)
