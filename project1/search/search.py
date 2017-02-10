# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
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
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.
    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:
    """
    fatherInfo = dict()
    visitedStates = set()
    path = []
    frontier = util.Stack()

    visitedStates.add(problem.getStartState())
    frontier.push(problem.getStartState())
    #explore graph
    while not frontier.isEmpty():
        curState = frontier.pop()
        visitedStates.add(curState)
        if problem.isGoalState(curState): break
        succesorsInfo = [x for x in problem.getSuccessors(curState) if x[0] not in visitedStates]
        for succInfo in succesorsInfo:
            state, direction, cost = succInfo
            frontier.push(state)
            fatherInfo[state] = (curState, direction)

    #backtrack the route from goal state to initial state
    while fatherInfo.get(curState):
        fatherState, direction = fatherInfo.get(curState)
        path.append(direction)
        curState = fatherState

    #return the  path
    path.reverse()
    return path

def breadthFirstSearch(problem):

    fatherInfo = dict()
    expandedStates = set()
    path = []
    frontier = util.Queue()

    frontier.push(problem.getStartState())
    #explore graph
    while not frontier.isEmpty():
        curState = frontier.pop()
        if curState in expandedStates: continue
        expandedStates.add(curState)
        if problem.isGoalState(curState):
            print "MOTHA FUKIN SUCCES"
            break
        succesorsInfo = [x for x in problem.getSuccessors(curState) if x[0] not in expandedStates]
        for succInfo in succesorsInfo:
            state, direction, cost = succInfo
            frontier.push(state)
            if not fatherInfo.get(state):
                fatherInfo[state] = (curState, direction)

    #backtrack the route from goal state to initial state
    while fatherInfo.get(curState):
        fatherState, direction = fatherInfo.get(curState)
        path.append(direction)
        curState = fatherState

    #return the  path
    path.reverse()
    return path

def uniformCostSearch(problem):

    path = []
    fatherInfo = dict()
    curState = problem.getStartState()
    expandedStates = set()
    frontier = util.PriorityQueue()

    frontier.push((curState, 0), 0)
    while not frontier.isEmpty():
        curState,curCost = frontier.pop()
        if curState in expandedStates: continue
        expandedStates.add(curState)
        if problem.isGoalState(curState): break
        succesorsInfo = [x for x in problem.getSuccessors(curState) if x[0] not in expandedStates]
        for succInfo in succesorsInfo:
            state, direction, cost = succInfo
            frontier.update((state, cost + curCost), cost + curCost)
            if not fatherInfo.get(state) or fatherInfo[state][2] > cost + curCost:
                fatherInfo[state] = (curState, direction, cost + curCost)

    while fatherInfo.get(curState):
        fatherState, direction, cost = fatherInfo.get(curState)
        path.append(direction)
        curState = fatherState

    path.reverse()
    return path

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    expandedStates = set()
    fatherInfo = dict()
    path = []
    frontier = util.PriorityQueue()

    frontier.push((problem.getStartState(), 0), 0)
    while not frontier.isEmpty():
        curState, curCost = frontier.pop()
        if curState in expandedStates: continue
        expandedStates.add(curState)
        if problem.isGoalState(curState): break
        succesorsInfo = [x for x in problem.getSuccessors(curState) if x[0] not in expandedStates]
        for succInfo in succesorsInfo:
            state, direction, cost = succInfo
            forwardCost = heuristic(state, problem)  # heuristic Cost
            backwardCost = curCost + cost
            frontier.update((state, backwardCost), backwardCost + forwardCost)
            if not fatherInfo.get(state) or fatherInfo.get(state)[2] > backwardCost:
                fatherInfo[state] = (curState, direction, backwardCost)

    while fatherInfo.get(curState):
        fatherState, direction, cost = fatherInfo.get(curState)
        path.append(direction)
        curState = fatherState

    path.reverse()
    return path

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
