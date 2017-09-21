# -*- coding: utf-8 -*-
"""
Authors: Chris Falter, Johny Rufus, and Xing Liu
"""

import pandas as pd

class gpsInfo():
    '''
    manages gps info for map search problem, assignment 1 problem 1
    sample code:
        folder_with_data = '/path/to/folder'
        gpsData = gpsInfo(folder_with_data)
        gpsDf = gpsData.df
        # fetch/manipulate data in the DataFrame
    '''

    def __init__(self, folder_path):
        '''
        loads the file city-gps.txt from the path into a Pandas dataframe. 
        Columns: Location (string), Lat (float), Lon (float), City (string), StateProvince (string)
        Index: Location
        Note that City and StateProvince are derived by parsing the location string
        '''
        pass
        # self.df = 

class roadInfo():
    '''
    manages road segment info for map search problem, assignment 1 problem 1
    '''
    
    def __init__(self, folder_path):
        '''
        loads the file road-segment.txt from the path into a Pandas DataFrame.
        Columns: Start (string), End (string), Miles (int), SpeedLimit (int), RoadName (string), Time (float)
        Index: default (row number)
        Note that Time is measured in minutes and is derived from Miles / SpeedLimit
        '''
        pass
        # self.df = 


