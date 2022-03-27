from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
import numpy as np

possibleDirections = {(0,1) : "UP",
                      (0,-1): "DOWN",
                      (1, 0): "RIGHT",
                      (-1,0): "LEFT",
                      (1,1) : "DIAUR",
                      (1,-1) : "DIADR",
                      (-1,1) : "DIAUL",
                      (-1,-1): "DIADL"}


def initObjects():
    tileSize = 32
    gameMap = np.zeros((17,17))
    gameMap += 1
    gameMap[3:5,12:14] = 0
    gameMap[12:14,3:5] = 0
    gameMap[2:8, 2:4] = 0
    gameMap[2:4, 2:8] = 0

    gameMap[13:15, 9:15] = 0
    gameMap[9:15, 13:15] = 0

    gameMap = gameMap.astype(np.int0)

    indexToMap = {(i,j) : (-259 + i*tileSize, 259 - j*tileSize) for i in range(17) for j in range(17)}
    return gameMap, indexToMap


def AStar(gameMap, startPosition, endPosition):
    grid = Grid(matrix=gameMap)
    start = grid.node(startPosition[0], startPosition[1])
    end = grid.node(endPosition[0], endPosition[1])
    finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
    path, runs = finder.find_path(start, end, grid)
    return path


def pruningPath(astarPath, pathLen):
    astarPath = np.array(astarPath)
    waypoints = []
    waypoints.append(astarPath[0].tolist())
    initialDirection = possibleDirections[tuple((astarPath[1]-astarPath[0]).tolist())]
    direction = initialDirection
    for i in range(1,pathLen-1):
        direction = possibleDirections[tuple((astarPath[i+1]-astarPath[i]).tolist())]
        if direction != initialDirection:
            waypoints.append(astarPath[i].tolist())
            initialDirection = direction
    waypoints.append(astarPath[pathLen-1].tolist())
    return waypoints

def transformingWayPointsIntoVector(waypoints, position):
    consecutiveDirection = []
    changeDirectionPoint = []
    for i in range(len(waypoints)-1):
        start = position[tuple(waypoints[i])]
        end = position[tuple(waypoints[i+1])]
        direction = [end[0]-start[0], end[1]-start[1]]
        amplitude = (direction[0]**2 + direction[1]**2)**0.5
        normDirection  = [direction[0]/amplitude, direction[1]/amplitude]
    
        consecutiveDirection.append(normDirection)
        changeDirectionPoint.append(end)
    
    return consecutiveDirection

def convertIntoIndex(oldValue):
    OldRange = 550  
    NewRange = 16  
    NewValue = (((oldValue + 275) * NewRange) / OldRange)
    return NewValue



def goTo(gameMap, indexToMap, startPosition, endPosition):
    startIndex = [int(convertIntoIndex(startPosition[0])), 16 - int(convertIntoIndex(startPosition[1]))]
    endIndex =  [int(convertIntoIndex(endPosition[0])), 16 - int(convertIntoIndex(endPosition[1]))]
    #startIndex = max(startIndex, 16)
    #endIndex = max(endIndex, 17)
    aStarPath = AStar(gameMap, startIndex, endIndex)
    waypoints = pruningPath(aStarPath, len(aStarPath))
    directions = transformingWayPointsIntoVector(waypoints, indexToMap)
    directions = np.array([directions[0][0],directions[0][1],0])
    return directions