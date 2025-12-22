import pdb
import math
import sys
from functools import reduce
import itertools
import common.nutkey
import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("inputfile")
	parser.add_argument("--two", help="part two", action="store_true")
	args = parser.parse_args()
	return args


# Find distance in 3D between two (x,y,z) tuples.
# We calculate the range squared - it makes no difference to 
# sort orders.
def range2(jb1, jb2):
	dx = jb1[0] - jb2[0]
	dy = jb1[1] - jb2[1]
	dz = jb1[2] - jb2[2]
	return dx*dx + dy*dy + dz*dz

# Compute the distance between every pair of JBs, and return sorted by furthest first
def computeDists(jbs):
	dists = []
	for (i,j) in itertools.combinations(range(0, len(jbs)), 2):
		r = range2(jbs[i], jbs[j])
		dists.append((i, j, r))

	# Now sort them by distance in reverse order
	# By sorting in reverse order, we can just pop the closest pair off the end of the list,"
	dists.sort(key = lambda item: -item[2])
	return dists
	
	
def findClosest(jbs, dists):
	while True:
		(i,j, r) = dists.pop()
		iCircuit = circuitFor(i)
		jCircuit = circuitFor(j)
		return (iCircuit, jCircuit, i, j)
								
def circuitFor(i):
	for c in range(0, len(circuits)):
		if i in circuits[c]:
			return c

def connect():
	# Finding closest JBs is O(n2) - but live with that for the moment
	(iCircuit,jCircuit, i, j) = findClosest(jbs, dists)	
	# Join j to i if not already in same circuit
	if iCircuit != jCircuit:
		jCirc = circuits[jCircuit]
		for k in circuits[jCircuit]:
			circuits[iCircuit].add(k)
		del circuits[jCircuit]
	return (i,j)
					



args = nutkey.parse_args()

# Have a list of JBs and their positions in 3D
# Want to connect Bs so every JB can be reached
# Would like to connect pairs that are close
# So - identify the closest JBs and connect them. Repeatedly
jbs = []

with open(args.inputfile, "r+") as data:
	for jb in data.readlines():
		coords = [int(x) for x in jb.split(',')]
		jbs.append(coords)

# Keep track of all circuits (connected sets of JBs) that have been formed.
# This includes sets of size 1 (a JB not connected to any others)
circuits = []

# Build initial circuit set, where each circuit contains just one JB
for i in range(0, len(jbs)):
	circuits.append({i})

dists = computeDists(jbs)	
if args.two:	
	while True:
		(i,j) = connect()
		remaining = len(jbs) -  len(circuits[0])
		if remaining == 0:
			x1 = jbs[i][0]
			x2 = jbs[j][0]
			print(x1*x2)
			sys.exit(0)
else:
	for _ in range(1000):
		connect()			
	
	# Sort circuits list by number of elements
	circuits.sort(key=len)
	circuits.reverse()
	# Multiply first 3 elements
	s = reduce(lambda acc,x: acc * len(x), circuits[0:3], 1)
	print(s)
	
	
	