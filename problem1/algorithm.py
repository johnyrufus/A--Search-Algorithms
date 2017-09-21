# -*- coding: utf-8 -*-
"""
Authors: Chris Falter, Johny Rufus John, and Xing Liu
"""

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
        '''
        Common initialization routine for all search implementation classes. 
        Cost function instances/logic could be initialized here. 
        '''
        self.gpsDf, self.roadDf = gpsDf, roadDf
        self.start = start
        self.goal = goal
        self.costFunc
        
    def search():
        '''
        In theory, any logic common to all the search implementations could be coded here;
        then a child class could call this function (SearchAlgorithm.search(self))
        before continuing with its particular logic. However, this seems unlikely.
        Probably this will just remain a stub, and all the logic will be 
        implemented in the search() function of child classes
        '''
        pass
    



        