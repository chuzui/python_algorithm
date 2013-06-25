# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

class Node:
    def __init__(self, state, action, parentNode, cost=0, costAndHeuristic=0):
        self._state  = state
        self._action = action
        self._parentNode = parentNode
        self._cost = cost
        self._costAndHeuristic = costAndHeuristic

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    closed = set()
    actions = []
    fringe = util.Stack()
    fringe.push(Node(problem.getStartState(), None, None))
    while not fringe.isEmpty():
        node = fringe.pop()
        if not node._state in closed:
            closed.add(node._state)
            #while len(actions) > 0 and node[2] != actions[len(actions) - 1][0]:
                #actions.pop(len(actions) - 1)
            #actions.append((node[0], node[1]))

            if problem.isGoalState(node._state):
                break

            for (successor, action, stepCost) in problem.getSuccessors(node._state):
                fringe.push(Node(successor, action, node))

    while not node._action == None:
        actions.insert(0,node._action)
        node = node._parentNode
    return actions


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    closed = set()
    actions = []
    fringe = util.Queue()
    fringe.push(Node(problem.getStartState(), None, None))
    while not fringe.isEmpty():
        node = fringe.pop()
        if not node._state in closed:
            closed.add(node._state)
            #while len(actions) > 0 and node[2] != actions[len(actions) - 1][0]:
            #actions.pop(len(actions) - 1)
          #actions.append((node[0], node[1]))

            if problem.isGoalState(node._state):
                break

            for (successor, action, stepCost) in problem.getSuccessors(node._state):
                fringe.push(Node(successor, action, node))

    while not node._action == None:
        actions.insert(0,node._action)
        node = node._parentNode
    return actions


def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    closed = {}
    actions = []
    fringe = util.PriorityQueue()
    fringe.push(Node(problem.getStartState(), None, None), 1)

    goalNode = None
    while not fringe.isEmpty():
        node = fringe.pop()
        #if hasGoal == True and closed[node._state]
        if goalNode != None and node._cost > goalNode._cost:
            break
        if (not node._state in closed) or node._cost < closed[node._state]:
            closed[node._state] = node._cost
            if problem.isGoalState(node._state):
                goalNode = node
            else:
                for (successor, action, stepCost) in problem.getSuccessors(node._state):
                    fringe.push(Node(successor, action, node, node._cost + stepCost), node._cost + stepCost)

    while not goalNode._action == None:
        actions.insert(0,goalNode._action)
        goalNode = goalNode._parentNode
    return actions
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    closed = {}
    actions = []
    fringe = util.PriorityQueue()
    fringeDict = {}
    startNode = Node(problem.getStartState(), None, None)
    fringe.push(startNode, 1)
    fringeDict[problem.getStartState()] = startNode
    goalNode = None
    # while not fringe.isEmpty():
    #     node = fringe.pop()
    #     if problem.isGoalState(node._state):
    #         goalNode = node
    #         break
    #     if (not node._state in closed) or node._cost< closed[node._state]:
    #         closed[node._state] = node._cost
    #         for (successor, action, stepCost) in problem.getSuccessors(node._state):
    #             costAndHeuristic = node._cost + stepCost + heuristic(successor, problem)
    #             fringe.push(Node(successor, action, node, node._cost + stepCost, costAndHeuristic),
    #                         costAndHeuristic)
    count = 0
    while not fringe.isEmpty():
        node = fringe.pop()
        if goalNode != None and node._costAndHeuristic >= goalNode._cost:
            break
        if problem.isGoalState(node._state):
            if goalNode != None and node._cost >= goalNode._cost:
                continue
            goalNode = node
            continue
        if not closed.has_key(node._state):
            for (successor, action, stepCost) in problem.getSuccessors(node._state):
                if not successor in closed:
                    costAndHeuristic = node._cost + stepCost + heuristic(successor, problem)
                    successorNode = Node(successor, action, node, node._cost + stepCost, costAndHeuristic)
                    fringe.push(successorNode,costAndHeuristic)

            closed[node._state] = node
        else:
            #print 'aaaaaaaaaaaa'
            pass
    while not goalNode._action == None:
        actions.insert(0,goalNode._action)
        goalNode = goalNode._parentNode
    return actions

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
