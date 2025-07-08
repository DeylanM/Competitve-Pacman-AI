# myTeam.py
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


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint
import distanceCalculator
#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'MyOffensiveReflexAgent', second = 'MyDefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########





          


class MyOffensiveReflexAgent(CaptureAgent):
    
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  def getTeam(self, gameState):
    """
    Returns agent indices of your team. This is the list of the numbers
    of the agents (e.g., red might be the list of 1,3,5)
    """
    if self.red:
      return gameState.getRedTeamIndices()
    else:
      return gameState.getBlueTeamIndices()

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor

  def OffensiveEvalution(self, gameState, action):
        foodCost = 0
        foodBonus = 0
        enemyDistance = 0
        foodRecip = 0
        gdist = []
        fdist = []
      
        SuccessorGameState = self.getSuccessor(gameState, action)
        agentGameState = gameState.getAgentState(self.index)


        newPos = SuccessorGameState.getAgentPosition(self.index)
        width = SuccessorGameState.getWalls().width
        
        if SuccessorGameState.isOnRedTeam(self.index):
            foodGrid = SuccessorGameState.getBlueFood()
            newOtherTeamStates = SuccessorGameState.getBlueTeamIndices()
            capsuleLocations = SuccessorGameState.getBlueCapsules()
           
        else:
            foodGrid = SuccessorGameState.getRedFood()
            newOtherTeamStates = SuccessorGameState.getRedTeamIndices()
            capsuleLocations = SuccessorGameState.getRedCapsules()
            

                    
        enemyPos1 = gameState.getAgentPosition(newOtherTeamStates[0])
        enemyDistance1 = self.getMazeDistance(newPos, enemyPos1)
        enemyAgent1 = gameState.getAgentState(newOtherTeamStates[0])
        enemyScaredTimer1 = agentGameState.scaredTimer
        gdist.append(enemyDistance1)
        
        enemyPos2 = gameState.getAgentPosition(newOtherTeamStates[1])
        enemyDistance2 = self.getMazeDistance(newPos, enemyPos2)
        gdist.append(enemyDistance2)
            
            
        foodList = foodGrid.asList()
        listLength = len(foodList)
        
        closestCap = []
        capsuleBonus = 0
        for i in capsuleLocations:
            closestCap.append(self.getMazeDistance(newPos, i))
        if (closestCap != []) and (enemyScaredTimer1 == 0):
            minCap = min(closestCap)
            capsuleBonus = minCap * -1
                
                
            
        
        
        if len(gdist) > 0:
            minEnemy = min(gdist)
            if minEnemy == 0:
                enemyDistance = -10
            elif(enemyScaredTimer1 > 1):
                enemyRecip = 1/minEnemy * 10
                enemyDistance = enemyRecip
            else:
                enemyRecip = 1/minEnemy
                enemyDistance = enemyRecip * -1
        
        
        for i in range (0, len(foodList)):
            foodDistance = self.getMazeDistance(foodList[i], newPos)
            fdist.append(foodDistance)
            
        else:
            minfood = min(fdist)
            foodRecip = 1/minfood  * 7
            foodCost = foodRecip
            
        foodBonus = listLength * -10
        numCarrying = agentGameState.numCarrying
        
        
        scaredTimer = agentGameState.scaredTimer
        returnBonus = 0
        if self.getScore(SuccessorGameState) < 1:
            if numCarrying >= 3 and enemyScaredTimer1 <= 1:
                startPos = SuccessorGameState.getInitialAgentPosition(self.index)
                returnDist = self.getMazeDistance(newPos, startPos)
                if returnDist >= 0:
                    returnBonus = returnDist * -3
        else:
            if numCarrying >= 1 and enemyScaredTimer1 <= 1:
                startPos = SuccessorGameState.getInitialAgentPosition(self.index)
                returnDist = self.getMazeDistance(newPos, startPos)
                if returnDist >= 0:
                    returnBonus = returnDist * -3
            
                
            
        
        finalScore = foodCost + enemyDistance + foodBonus + returnBonus + capsuleBonus
        return finalScore

  def chooseAction(self, gameState):


    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
      actions = gameState.getLegalActions(self.index)
      foodLeft = len(self.getFood(gameState).asList())
      if foodLeft > 0:
            bestScore = -10000000
            for action in actions:
                score = self.OffensiveEvalution(gameState, action)                
                if score > bestScore:
                    bestAction = action
                    bestScore = score
            return bestAction
        
        
  
    


        

  


class MyDefensiveReflexAgent(CaptureAgent):
    
  def registerInitialState(self, gameState):
    self.start = gameState.getAgentPosition(self.index)
    CaptureAgent.registerInitialState(self, gameState)

  def getTeam(self, gameState):
    """
    Returns agent indices of your team. This is the list of the numbers
    of the agents (e.g., red might be the list of 1,3,5)
    """
    if self.red:
      return gameState.getRedTeamIndices()
    else:
      return gameState.getBlueTeamIndices()

  def getSuccessor(self, gameState, action):
    """
    Finds the next successor which is a grid position (location tuple).
    """
    successor = gameState.generateSuccessor(self.index, action)
    pos = successor.getAgentState(self.index).getPosition()
    if pos != nearestPoint(pos):
      # Only half a grid position was covered
      return successor.generateSuccessor(self.index, action)
    else:
      return successor
  
  def getScaredTimer(self, gameState, action):
      SuccessorGameState = self.getSuccessor(gameState, action)

      if SuccessorGameState.isOnRedTeam(self.index):
            newOtherTeamStates = SuccessorGameState.getBlueTeamIndices()
      else:
            newOtherTeamStates = SuccessorGameState.getRedTeamIndices()
      agentGameState = gameState.getAgentState(newOtherTeamStates[0])
      enemyScaredTimer1 = agentGameState.scaredTimer
      return enemyScaredTimer1
  
  def DefenciveEvalution(self, gameState, action):
      
        SuccessorGameState = self.getSuccessor(gameState, action)
        newPos = SuccessorGameState.getAgentPosition(self.index)
        width = SuccessorGameState.getWalls().width
        middle = width/2
        gdist = []
        if SuccessorGameState.isOnRedTeam(self.index):
            newOtherTeamStates = SuccessorGameState.getBlueTeamIndices()
        else:
            newOtherTeamStates = SuccessorGameState.getRedTeamIndices()

        enemyPos1 = gameState.getAgentPosition(newOtherTeamStates[0])
        enemyDistance1 = self.getMazeDistance(newPos, enemyPos1)
        gdist.append(enemyDistance1)
        
        enemyPos2 = SuccessorGameState.getAgentPosition(newOtherTeamStates[1])
        enemyDistance2 = self.getMazeDistance(newPos, enemyPos2)
        gdist.append(enemyDistance2)
        foodBonus = 0
        enemyDistance = 0
        agentGameState = gameState.getAgentState(newOtherTeamStates[0])
        scaredTimer = agentGameState.scaredTimer
        enemyScaredTimer1 = agentGameState.scaredTimer

        if len(gdist) > 0:
            minEnemy = min(gdist)
            if (scaredTimer == 0):
                if (SuccessorGameState.isOnRedTeam(self.index)):
                    if(enemyPos1[0] <= middle):
                        enemyDistance = minEnemy * -20
                    else:
                        enemyDistance = minEnemy * -.5
                        
                    if(enemyPos2[0] <= middle):
                        enemyDistance = minEnemy * -20
                    else:
                        enemyDistance = minEnemy * -.5

                else:
                    if(enemyPos1[0] > middle + 1):
                        enemyDistance = minEnemy * -20
                    else:
                        enemyDistance = minEnemy * -.5
                
                    if(enemyPos2[0] > middle + 1):
                        enemyDistance = minEnemy * -20
                    else:
                        enemyDistance = minEnemy * -.5
            else:
                if minEnemy == 0:
                    enemyDistance = -1000
                else:
                    enemyRecip = 1/minEnemy * -5
                    enemyDistance = enemyRecip

        
       

        
        returnBonus = 0
        if SuccessorGameState.isOnRedTeam(self.index):
            if newPos[0] >= middle - 1:
                returnBonus = -50
        else:
            if newPos[0] <= middle + 1:
                returnBonus = -50
        
        return enemyDistance + foodBonus + returnBonus
    
  def chooseAction(self, gameState):


    # You can profile your evaluation time by uncommenting these lines
    # start = time.time()
      
      actions = gameState.getLegalActions(self.index)
      foodLeft = len(self.getFood(gameState).asList())
      if foodLeft > 0:
            bestScore = -10000000
            for action in actions:
                if self.getScaredTimer(gameState, action) >= 30:
                    score = self.OffensiveEvalution(gameState, action)
                else:
                    score = self.DefenciveEvalution(gameState, action)
                if score > bestScore:
                    bestAction = action
                    bestScore = score
            if "Stop" in bestAction:
                bestAction = random.choice(gameState.getLegalActions(self.index))
            return bestAction
        
  def OffensiveEvalution(self, gameState, action):
        foodCost = 0
        foodBonus = 0
        enemyDistance = 0
        foodRecip = 0
        gdist = []
        fdist = []
      
        SuccessorGameState = self.getSuccessor(gameState, action)
        agentGameState = gameState.getAgentState(self.index)


        newPos = SuccessorGameState.getAgentPosition(self.index)
        width = SuccessorGameState.getWalls().width
        
        if SuccessorGameState.isOnRedTeam(self.index):
            foodGrid = SuccessorGameState.getBlueFood()
            newOtherTeamStates = SuccessorGameState.getBlueTeamIndices()
            capsuleLocations = SuccessorGameState.getBlueCapsules()
        else:
            foodGrid = SuccessorGameState.getRedFood()
            newOtherTeamStates = SuccessorGameState.getRedTeamIndices()
            capsuleLocations = SuccessorGameState.getRedCapsules()

                    
        enemyPos1 = gameState.getAgentPosition(newOtherTeamStates[0])
        enemyDistance1 = self.getMazeDistance(newPos, enemyPos1)
        enemyAgent1 = gameState.getAgentState(newOtherTeamStates[0])
        enemyScaredTimer1 = agentGameState.scaredTimer
        gdist.append(enemyDistance1)
        
        enemyPos2 = gameState.getAgentPosition(newOtherTeamStates[1])
        enemyDistance2 = self.getMazeDistance(newPos, enemyPos2)
        gdist.append(enemyDistance1)
            
            
        foodList = foodGrid.asList()
        listLength = len(foodList)
        
        closestCap = []
        capsuleBonus = 0
        for i in capsuleLocations:
            closestCap.append(self.getMazeDistance(newPos, i))
        if (closestCap != []) and (enemyScaredTimer1 == 0):
            minCap = min(closestCap)
            capsuleBonus = minCap * -.5
                
                
            
        
       
        
        
        if len(gdist) > 0:
            minEnemy = min(gdist)
            if minEnemy == 0:
                enemyDistance = -1000000
            elif(enemyScaredTimer1 > 1):
                enemyRecip = 1/minEnemy * 1
                enemyDistance = enemyRecip
            else:
                enemyRecip = 1/minEnemy
                enemyDistance = enemyRecip * -1
        
        
        for i in range (0, len(foodList)):
            foodDistance = self.getMazeDistance(foodList[i], newPos)
            fdist.append(foodDistance)
            
        else:
            minfood = min(fdist)
            foodRecip = 1/minfood  * 10
            foodCost = foodRecip
            
        foodBonus = listLength * -10
        numCarrying = agentGameState.numCarrying
        
        
        scaredTimer = agentGameState.scaredTimer
        
        returnBonus = 0    
        if numCarrying >= 3 and enemyScaredTimer1 <= 1:
            startPos = SuccessorGameState.getInitialAgentPosition(self.index)
            returnDist = self.getMazeDistance(newPos, startPos)
            if returnDist >= 0:
                returnBonus = returnDist * -3
                
            
        
        finalScore = foodCost + enemyDistance + foodBonus + returnBonus + capsuleBonus
        return finalScore
    





