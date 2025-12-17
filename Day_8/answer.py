import argparse
import pdb
import math
import sys
from functools import reduce
parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
parser.add_argument("--two", help="part two", action="store_true")
args = parser.parse_args()

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
# Build initial circuit set
for i in range(0, len(jbs)):
	circuits.append({i})

def range2(jb1, jb2):
	dx = jb1[0] - jb2[0]
	dy = jb1[1] - jb2[1]
	dz = jb1[2] - jb2[2]
	return dx*dx + dy*dy + dz*dz

def computeDists(jbs):
	dists = []
	for i in range(0, len(jbs) - 1):
		for j in range(i+1, len(jbs)):
			r = range2(jbs[i], jbs[j])
			dists.append((i, j, r))
	# Now sort them
	dists.sort(key = lambda item: item[2])
	return dists
	

nextPick = 0
def findClosest(jbs, dists):
	global nextPick
	while True:
		(i,j, r) = dists[nextPick]
		nextPick += 1
		iCircuit = circuitFor(i)
		jCircuit = circuitFor(j)
		return (iCircuit, jCircuit, i, j)
								
def circuitFor(i):
	for c in range(0, len(circuits)):
		if i in circuits[c]:
			return c

dists = computeDists(jbs)

def connect():
	# Finding closest JBs is O(n2) - but live with that for the moment
	(iCircuit,jCircuit, i, j) = findClosest(jbs, dists)	
	# Join j to i if not already in same circuit
	if iCircuit != jCircuit:
		jCirc = circuits[jCircuit]
		# circuits[jCircuit] = []	
		for k in circuits[jCircuit]:
			circuits[iCircuit].add(k)
		del circuits[jCircuit]
	return (i,j)
					
	
n = 1000
print(len(jbs))
if args.two:
	
	while True:
		(i,j) = connect()
		remaining = len(jbs) -  len(circuits[0])
		# print(f"{reduce(lambda x,y: x+len(y), circuits, 0)} {len(circuits)}")
		# print(circuits)
		if remaining == 0:
			x1 = jbs[i][0]
			x2 = jbs[j][0]
			print(x1*x2)
			sys.exit(0)
else:
	for _ in range(n):
		connect()			
	
	# Sort circuits list by number of elements
	circuits.sort(key=len)
	circuits.reverse()
	# Multiply first 3 elements
	print(circuits)
	s = reduce(lambda acc,x: acc * len(x), circuits[0:3], 1)
	print(s)
	
	
	