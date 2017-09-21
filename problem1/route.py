#!/usr/bin/env python
"""
Authors: Chris Falter, Johny Rufus John, and Xing Liu
"""

from mapInfo import gpsInfo, roadInfo
from algorithm import CostFunction
from bfs import BFS
from dfs import DFS
from uniform import Uniform
from astar import AStar
import sys

def getRouteInfo(solutionPath, roadDf):
    '''
    returns a list of each stage of solution path, from start to finish
    each list element is a list consisting of start city, destination city, travel time (in hours), distance (in miles), and highway name
    '''
    result = []
    for i in range(len(solutionPath) - 1):
        # find the row in roadDf for the segment from solutionPath[i] tp solutionPath[i + 1]
        # row = roadDf.find(....)
        result.append([row.Start, row.End, row.Time, row.Distance, row.RoadName])
    return result

def printSolution(solution, routeInfo):
    '''
    prints the solution per requirements
    solution = instance of Solution class, returned by the search() function
    routeInfo = list of segments from start to finish that got returned by getRouteInfo()
    '''
    pass

def main():
    # set up map info
    gpsDf = gpsInfo('.')
    roadDf = roadInfo('.')
    
    # process command-line args
    start = sys.argv[1]
    goal = sys.argv[2]
    costArg = sys.argv[4]
    if costArg == 'segments':
        costFunc = CostFunction.Segments
    elif costArg == 'distance':
        costFunc = CostFunction.Distance
    elif costArg == 'time':
        costFunc = CostFunction.Time
        
    routingArg = sys.argv[3]
    if routingArg == 'bfs':
        algorithm = BFS(gpsDf, roadDf, start, goal, costFunc)
    elif routingArg == 'uniform':
        algorithm = Uniform(gpsDf, roadDf, start, goal, costFunc)
    elif routingArg == 'dfs':
        algorithm = DFS(gpsDf, roadDf, start, goal, costFunc)
    elif routingArg == 'astar':
        algorithm = AStar(gpsDf, roadDf, start, goal, costFunc)
        
    # perform the search
    solution = algorithm.search()
    
    # print the results
    routeInfo = getRouteInfo(solution.path, roadDf)
    printSolution(solution, routeInfo)
    
if __name__ == '__main__':
    main()
    
    
