# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util, sys

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        score = 0
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        return 0
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        ghostsPosition = successorGameState.getGhostPositions()

        #works 100% if ou don't have walls
        for ghostPos in ghostsPosition :
            manDist = manhattanDistance(newPos, ghostPos)
            if manDist < 2: return -100000

        distToFood =[manhattanDistance(newPos,(i,j)) for i in range(newFood.width) for j in range(newFood.height) if newFood[i][j] == True ]
        distToFood.append(1000)
        minDistToFood = min(distToFood)

        if minDistToFood != 1000:
            return ( (-80) * newFood.count(True) + (-100) * minDistToFood )
        else:
            return 0


def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
        #print "NR agenti :" + str(gameState.getNumAgents())
        gameStates = []
        for action in gameState.getLegalActions(0):
            newGS = gameState.generateSuccessor(0, action)
            x = self.minimax(newGS,self.depth,1)
            gameStates.append((x,action))

        optimalAction = max(gameStates, key=lambda t: t[0])
        return optimalAction[1]
        util.raiseNotDefined()

    def minimax(self,gameState,depth,agentIdx):
        gameStates = []
        nextAgentIdx = 0
        nextDepth = depth
        if agentIdx == gameState.getNumAgents() - 1:
            nextAgentIdx = 0
            nextDepth = depth - 1

        else:
            nextAgentIdx = agentIdx + 1

        if depth <= 0:
            return (self.evaluationFunction(gameState))

        for action in gameState.getLegalActions(agentIdx):
            #print action
            newGS = gameState.generateSuccessor(agentIdx, action)
            x = self.minimax(newGS, nextDepth, nextAgentIdx)
            gameStates.append(x)

        if len(gameStates)==0:
            return self.evaluationFunction(gameState)
        if agentIdx == 0:
            return max(gameStates)
        else:
            return min(gameStates)

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        gameStates = []
        maxOptim = -sys.maxint
        minOptim = sys.maxint
        _,optimalAction = self.MaxNodeAlg(gameState,maxOptim,minOptim,0,self.depth)
        return optimalAction



    def MaxNodeAlg(self, gameState, maxOptim, minOptim, agentIdx, depth):
        val = - sys.maxint
        optimalAction = None
        gameStates = []
        nextAgentIdx = 0
        nextDepth = depth

        if agentIdx == gameState.getNumAgents() - 1:
            nextAgentIdx = 0
            nextDepth = depth - 1
        else:
            nextAgentIdx = agentIdx + 1

        if depth <= 0:
            return (self.evaluationFunction(gameState), None)

        actions = [action for action in gameState.getLegalActions(agentIdx)]
        if len(actions) == 0:
            return (self.evaluationFunction(gameState), None)

        for action in actions:
            newGS = gameState.generateSuccessor(agentIdx, action)
            v,_ = self.MinNodeAlg(newGS, maxOptim, minOptim, nextAgentIdx, nextDepth)
            val = max(v, val)

            if val > minOptim:
                return (val,None)

            if val > maxOptim:
                maxOptim = val
                optimalAction = action

        return (val, optimalAction)

    def MinNodeAlg(self, gameState, maxOptim, minOptim, agentIdx, depth):
        val = sys.maxint
        gameStates = []
        nextAgentIdx = 0
        nextDepth = depth
        optimalAction = None

        if agentIdx == gameState.getNumAgents() - 1:
            nextAgentIdx = 0
            nextDepth = depth - 1
        else:
            nextAgentIdx = agentIdx + 1

        if depth <= 0:
            return (self.evaluationFunction(gameState), None)

        actions = [action for action in gameState.getLegalActions(agentIdx)]
        if len(actions) == 0:
            return (self.evaluationFunction(gameState), None)

        for action in actions:
            newGS = gameState.generateSuccessor(agentIdx, action)

            if nextAgentIdx == 0: # pacman node that means it is a max node
                v,_ = self.MaxNodeAlg(newGS, maxOptim, minOptim, nextAgentIdx, nextDepth)
            else:
                v,_ = self.MinNodeAlg(newGS, maxOptim, minOptim, nextAgentIdx, nextDepth)
            val = min(val, v)

            if val < maxOptim:
                return (v,None)

            if val < minOptim:
                minOptim = v
                optimalAction = action

        return (val, optimalAction)


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        gameStates = []
        for action in gameState.getLegalActions(0):
            newGS = gameState.generateSuccessor(0, action)
            x = self.minimax(newGS, self.depth, 1)
            gameStates.append((x, action))

        optimalAction = max(gameStates, key=lambda t: t[0])
        return optimalAction[1]

    def minimax(self, gameState, depth, agentIdx):
        gameStates = []
        nextAgentIdx = 0
        nextDepth = depth
        if agentIdx == gameState.getNumAgents() - 1:
            nextAgentIdx = 0
            nextDepth = depth - 1

        else:
            nextAgentIdx = agentIdx + 1

        if depth <= 0:
            return (self.evaluationFunction(gameState))

        for action in gameState.getLegalActions(agentIdx):
            # print action
            newGS = gameState.generateSuccessor(agentIdx, action)
            x = self.minimax(newGS, nextDepth, nextAgentIdx)
            gameStates.append(x)

        if len(gameStates) == 0:
            return self.evaluationFunction(gameState)
        if agentIdx == 0:
            return max(gameStates)
        else:
            return float(sum(gameStates))/len(gameStates)


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from a GameState (pacman.py)
    successorGameState = currentGameState
    newPos = successorGameState.getPacmanPosition()
    newFood = successorGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghostsPosition = successorGameState.getGhostPositions()

    # works 100% if ou don't have walls
    for ghostPos in ghostsPosition:
        manDist = manhattanDistance(newPos, ghostPos)
        if manDist < 2: return -100000

    distToFood = [manhattanDistance(newPos, (i, j)) for i in range(newFood.width) for j in range(newFood.height) if
                  newFood[i][j] == True]
    distToFood.append(1000)
    minDistToFood = min(distToFood)

    if minDistToFood != 1000:
        return (-100) * newFood.count(True) + (-1) * minDistToFood
    else:
        return 0
# Abbreviation
better = betterEvaluationFunction

