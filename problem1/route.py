# Author: Xing Liu

# 

import sys
import numpy as np
import copy
from heapq import heappush, heappop 
from geopy.distance import great_circle


def succ_paths(path):
	succ = []
	for s in segments_hash_table[path[-1]]:
		# avoid revisit
		if s[0] not in visited_city:
			tmp = copy.deepcopy(path)
			tmp.append(s[0])
			succ.append(tmp)
			visited_city[s[0]] = 1
	return succ

def succ_paths_uniform(path, cost_func):
	succ = []
	for s in segments_hash_table[path[-1]]:
		tmp = copy.deepcopy(path)
		tmp.append(s[0])
		# update path cost information
		if cost_func == 'distance':
			tmp[0] += float(s[1])
		elif cost_func == 'time':
			tmp[0] += float(s[1])/float(s[2])
		# append to path successor, only allow revisit if it decreases the cost
		if s[0] not in minnow_hash_table:
			minnow_hash_table[s[0]] = tmp[0]
			succ.append(tmp)
		elif s[0] in minnow_hash_table and tmp[0] < minnow_hash_table[s[0]]:
			minnow_hash_table[s[0]] = tmp[0]
			succ.append(tmp)
		
	return succ


def succ_paths_astar(path, cost_func, end_city):
	succ = []
	for s in segments_hash_table[path[-1]]:
		tmp = copy.deepcopy(path)
		tmp.append(s[0])
		# update g(s) h(s) information
		if cost_func == 'distance':
			tmp[1] += float(s[1])
			distance_count(tmp, end_city)
			tmp[0] = tmp[1] + tmp[2]
		elif cost_func == 'time':
			tmp[1] += float(s[1])/float(s[2])
			time_count(tmp, end_city)
			tmp[0] = tmp[1] + tmp[2]
		# append to path successor
		succ.append(tmp)
	return succ


def distance_count(path, end_city):
	# error handle, city not found in gps database
	if path[-1] not in gps_hash_table or path[-2] not in gps_hash_table:
		return
	# calculate direct distrance in miles
	pos1 = tuple(gps_hash_table[path[-1]])
	pos2 = tuple(gps_hash_table[end_city])
	path[2] = great_circle(pos1, pos2).miles


def time_count(path, end_city):
	# error handle, city not found in gps database
	if path[-1] not in gps_hash_table or path[-2] not in gps_hash_table:
		return
	# calculate direct distrance in miles
	pos1 = tuple(gps_hash_table[path[-1]])
	pos2 = tuple(gps_hash_table[end_city])
	path[2] = great_circle(pos1, pos2).miles/max_speed_lim


# use priority queue
def ASTAR(start_city, end_city, cost_func):
	fringe = []
	# first value is g(s) + h(s), 2nd value is g(s), 3rd value is h(s)
	heappush(fringe, [0, 0, 0, start_city])

	while len(fringe) > 0:
		path = heappop(fringe)
		for s in succ_paths_astar(path, cost_func, end_city):
			if s[-1] == end_city:
				return s
			heappush(fringe, s)


# use priority queue
def UNIFORM(start_city, end_city, cost_func):
	fringe = []
	heappush(fringe, [0, start_city])

	minnow_hash_table[start_city] = 0;

	while len(fringe) > 0:
		path = heappop(fringe)
		for s in succ_paths_uniform(path, cost_func):
			if s[-1] == end_city:
				return s
			heappush(fringe, s)


# use FIFO queue
def BFS(start_city, end_city):
	visited_city[start_city] = 1
	fringe = [[start_city]]
	while len(fringe) > 0:
		path = fringe.pop(0)
		for s in succ_paths(path):
			if s[-1] == end_city:
				return s
			fringe.append(s)


# use stack
def DFS(start_city, end_city):
	visited_city[start_city] = 1
	fringe = [[start_city]]
	while len(fringe) > 0:
		path = fringe.pop()
		for s in succ_paths(path):
			if s[-1] == end_city:
				return s
			fringe.append(s)


if __name__ == '__main__':
	visited_city = {}
	gps_hash_table = {}
	segments_hash_table = {}
	minnow_hash_table = {}
	max_speed_lim = 0

	# load data
	with open('./city-gps.txt','r') as city_gps_f:
		for line in city_gps_f:
			a = line.replace('\n','').split(" ")
			gps_hash_table[a[0]] = [a[1], a[2]]

	with open('./road-segments.txt','r') as road_seg_f:
		for line in road_seg_f:
			a = line.replace('\n','').split(" ")
			if len(a[3]) < 2:
				a[3] = 45
			if float(a[3]) > max_speed_lim:
				max_speed_lim = float(a[3])
			if a[0] not in segments_hash_table:
				segments_hash_table[a[0]] = [ a[1:] ]
			else:
				segments_hash_table[a[0]].append(a[1:])
			if a[1] not in segments_hash_table:
				segments_hash_table[a[1]] = [ [a[0],a[2],a[3],a[4]] ]
			else:
				segments_hash_table[a[1]].append([a[0],a[2],a[3],a[4]])

	# get parameter
	start_city = sys.argv[1]
	end_city = sys.argv[2]
	route_alg = sys.argv[3]
	assert route_alg in ['bfs','uniform','dfs','astar'], 'Algorithm %s not defined'%route_alg
	cost_func = sys.argv[4]
	assert cost_func in ['segments','distance','time'], "Routing option %s not defined"%cost_func

	# print segments_hash_table[start_city]

	# bfs
	if route_alg == 'bfs':
		path = BFS(start_city, end_city)

	# dfs
	if route_alg == 'dfs':
		path = DFS(start_city, end_city)

	# uniform
	if route_alg == 'uniform':
		if cost_func == 'segments':
			# if cost is number of segments then same with BFS
			path = BFS(start_city, end_city)
		else:
			path = UNIFORM(start_city, end_city, cost_func)
		
	# astar
	if route_alg == 'astar':
		if cost_func == 'segments':
			path = BFS(start_city, end_city)
		else:
			path = ASTAR(start_city, end_city, cost_func)
			path = [path[1]] + path[3:]

	print path
	
