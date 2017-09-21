# -*- coding: utf-8 -*-
"""
Authors: Chris Falter, Johny Rufus, and Xing Liu
"""

from mapInfo import gpsInfo, roadInfo
import pandas as pd
from enum import enum

class CostFunction(enum):
    Time = "Time"
    Distance = "Distance"
    Segments = "Segments"    

class Solution():
    '''
    Sample code:
        algorithm = bfs(gpsDf, roadDf, startLocation, goalLocation, CostFunction.Time)
        solution = algorithm.search()
        print solution.time solution.distance " ".join(solution.path)
    '''
    
    def __init__(self, distance, time, path):
        '''
        distance (int) = miles for the entire path from start to goal
        time (float) = time in hours to traverse entire path
        path (list) = list of location names representing nodes of the solution path
        '''
        self.distance = distance
        self.time = time
        self.path = path
        

class SearchAlgorithm():
    
    def __init__(self, gpsDf, roadDf, start, goal, costFunc):
        self.gpsDf, self.roadDf = gpsDf, roadDf
        self.start = start
        self.goal = goal
        self.costFunc
        
    def search():
        pass
    
class BFS(SearchAlgorithm):
    '''
    implements the breadth-first search algorithm
    '''
    
    def search():
        pass
    
class Uniform(SearchAlgorithm):
    '''
    implements the uniform search algorithm
    '''
    
    def search():
        pass

class DFS(SearchAlgorithm):
    '''
    implements the depth-first search algorithm
    '''
    
    def search():
        pass
    
class AStar(SearchAlgorithm):
    '''
    implements the A* search algorithm
    '''
    
    def search():
        pass




        