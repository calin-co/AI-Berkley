# valueIterationAgents.py
# -----------------------
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


import mdp, util

from learningAgents import ValueEstimationAgent

class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """
    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter() # A Counter is a dict with default 0
        states = self.mdp.getStates()
        self.values_prev_it = util.Counter()
        self.values_cur_it = util.Counter()

        "*** YOUR CODE HERE ***"
        iteration = 1
        while iteration <= iterations:
            # calculez Vk
            # pentru fiecare state calculez Q_value cu o actiune anume dupa care iau cel mai mare Q value
            for state in states:
                actions = mdp.getPossibleActions(state)

                if  len(actions) < 1:
                    self.values_cur_it[state] = self.values_prev_it[state]
                    continue

                bestQvalue = float('-inf')

                #if self.mdp.isTerminal(state):
                 #   succesors = self.mdp.getTransitionStatesAndProbs(state, actions[0])
                  #  for succesor in succesors:
                   #     self.values_cur_it[state] = mdp.getReward(state, actions[0], succesor[1])
                    #continue

                for action in actions:
                    Qvalue = self.calcululateQValue(state, action, self.values_prev_it)
                    if Qvalue > bestQvalue:
                        bestQvalue = Qvalue

                self.values_cur_it[state] = bestQvalue

            self.values_prev_it = self.values_cur_it.copy()
            self.values_cur_it.clear()
            iteration += 1

        self.values = self.values_prev_it.copy()


    def calcululateQValue(self, state, action, Vk):
        """
        Calculate and return Q_value at an iteration l
        Vk is the calculated value iteration of k stepts
        discount_exponent is  k
        """
        Q_value = 0
        succesors = self.mdp.getTransitionStatesAndProbs(state, action)
        for nextState, prob in succesors:
            Q_value += prob * (self.mdp.getReward(state, action, nextState) + self.discount * Vk[nextState])
        return Q_value

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        "*** YOUR CODE HERE ***"
        Q_value = 0
        succesors = self.mdp.getTransitionStatesAndProbs(state,action)
        for nextState, prob in succesors:
            Q_value += prob * (self.mdp.getReward(state, action, nextState) + self.discount * self.values[nextState])
        return Q_value
        #util.raiseNotDefined()

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        "*** YOUR CODE HERE ***"
        bestAction = None
        bestValue =  float('-inf')
        if self.mdp.isTerminal(state):
            return None

        actions = self.mdp.getPossibleActions(state)
        if len(actions) < 1:
            return None

        for action in actions:
            curValue = 0
            succesors = self.mdp.getTransitionStatesAndProbs(state, action)
            for nextState, prob in succesors:
                curValue += self.values[nextState] * prob
            if curValue > bestValue:
                bestValue = curValue
                bestAction = action

        return bestAction
        util.raiseNotDefined()

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)
