import argparse
import pdb
import math
import sys
from functools import reduce

parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
parser.add_argument("--two", help="part two", action="store_true")
args = parser.parse_args()

# Load tile positions 
tiles = []
with open(args.inputfile, "r+") as data:
	tiles = [list(map(int, l.split(','))) for l in data]

def isInsideRectFormedBy(i, j, pos):
	# To be inside, must have x between xi and xj (inclusive). Same for y
	x1 = tiles[i][0]
	x2 = tiles[j][0]
	y1 = tiles[i][1]
	y2 = tiles[j][1]
	maxx = max(x1, x2)
	minx = min(x1, x2)
	maxy = max(y1, y2)
	miny = min(y1, y2)
	
	x = pos[0]
	y = pos[1]
	
	return minx < x and x < maxx and miny < y and y < maxy
	

def normalize(v):
	if v == 0:
		return v
	if v < 0:
		return -1
	else:
		return 1
	
# For two tiles i and j, check that every point in the external path is inside he rect formed by them.


def check(t1, t2):
	# Provided that the boundary line has no segments that fall inside the test rectangle, we are okay
		
	# Step around each tile pair
	last = tiles[-1]
	for t in tiles:		
		# Does the line between this tile and the last intercept our rectangle?
		prev = last
		last = t
		dx = t[0] - prev[0]
		(xi,yi) = t1
		(xj,yj) = t2
		(v_x, h_y) = t
		
		# Generate the min and max bounds. Inset them, because we only care if any of the rectangle is OUTSIDE the
		# boundary - the boundary itself is valid for inclusion.
		minx = min(xi,xj) + 1
		maxx = max(xi,xj) - 1
		miny = min(yi, yj) + 1
		maxy = max(yi,yj) - 1
		
		if dx == 0:
			min_v_y = min(h_y, prev[1])
			max_v_y = max(h_y, prev[1])
			
			# X is constant, so vertical. Compare to vertical boundaries
			if not minx <= v_x <= maxx:
				continue

			# Our line intercepts on the x-coord. Do either the top or the bottom fall inside the rect?
			if  min_v_y < miny < max_v_y or min_v_y <  maxy < max_v_y:
				return False
			
		else:
			min_h_x = min(v_x, prev[0])
			max_h_x = max(v_x, prev[0])

			# Y is constant, so horizontal
			if not miny <= h_y <= maxy:
				continue
				
			# Our line intercepts the rectangle. Is it all above or all below?
			if  min_h_x <= minx <= max_h_x or min_h_x <= maxx <= max_h_x:
				return False

		
	return True	



# Find two tiles with max value of dX * dY


# Build a set of posssible rects
rects = []
maxA = 0

from itertools import combinations

for t1,t2 in combinations(tiles, 2):
	dX = abs(t1[0] - t2[0]) +1
	dY = abs(t1[1] - t2[1]) +1
	A = abs(dX * dY)
	if args.two and not check(t1,t2):
		continue
	maxA = max(A, maxA)

print(maxA)