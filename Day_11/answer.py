import argparse
import pdb
import math
import sys
import re
import functools

parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
parser.add_argument("--two", help="part two", action="store_true")
args = parser.parse_args()

connections = {}
with open(args.inputfile, "r+") as data:
	for l in data:
		# format is <name>: <conn> <conn> ....
		(name, conns) = l.split(":")
		connections[name] = (conns.strip().split(" "))



# In Part 2 we require that all paths pass through FFT and DAC. 

# If there are loops, the the number of paths is infinite and the problem is insoluble. Therefore there are no loops.
# That means we will only visit each mustVisit node once. So we just need to maintain a count of how many we have visited
# to know if we have visited all of them 	 
mustVisit = ["dac", "fft"]
@functools.cache
def countPaths(node, pathCount, state = 0, visited = 0):
	if node == "out":
		if args.two:
			if visited == len(mustVisit):
				return 1
			else:
				return 0
		else:
			return 1
	if args.two:
		if node in mustVisit:
			visited += 1
	ret = sum([countPaths(node, pathCount, state, visited) for node in connections[node]])
	if args.two:
		if node in mustVisit:
			visited -= 1
	return ret
				
				
if args.two:
	print(countPaths("svr", 1))
else:
	print(countPaths("you", 1))
