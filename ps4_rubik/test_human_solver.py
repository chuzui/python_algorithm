#!/usr/bin/python
import unittest
import solver
import rubik

class TestHumanSolver(unittest.TestCase):
    def testHuman(self):
        position = rubik.input_configuration()
        path = solver.shortest_path(position, rubik.I)
        instructions = [rubik.quarter_twists_names[move] for move in path]

        prompt = "solver.shortest_path gives the following move sequence:\n" +\
                 str(instructions) +\
                 "\nSolve the cube." +\
                 "\nEnter 1 if you solved the cube. Enter 0 otherwise: "
        ans = raw_input(prompt)
        self.assertEqual(ans, '1')

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestHumanSolver)
    unittest.TextTestRunner(verbosity=2).run(suite)
