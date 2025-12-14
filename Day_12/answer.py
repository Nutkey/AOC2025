# Solves Day 12 part 1
# If it runs to completion, prints the answer
import argparse
import pdb
import sys
from functools import reduce
from enum import Enum

parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
parser.add_argument("--two", help="part two", action="store_true")
args = parser.parse_args()


# Describes the layout of each shape, as a 3x3 array of 1's and 0's
shapes = []

# Describes the layout of each space, as a tuple of (width, height)
spaces = []

# For each space (rows), record an array (columns) of the number of presents of each type which need to fit into the space
presentsToFit = []

presentSquares = []
shapesParsed = 0
NUM_SHAPES = 6

class State(Enum):
	ShapeIdentifier = 1
	ShapeRow = 2
	Space = 3
	
	
state = State.ShapeIdentifier
with open(args.inputfile, "r+") as data:
	for l in data:
		l = l.strip()
		match state:
			case  State.ShapeIdentifier:
				shapeLayouts = []
				squares = 0
				state = State.ShapeRow
			
			case State.ShapeRow:
				# Read three rows of shape, then blank line
				if l == "":				
					presentSquares.append(squares)
					shapesParsed += 1
					if shapesParsed == NUM_SHAPES:
						state = State.Space
					else:
						state = State.ShapeIdentifier
						
				# Count how many squares are used in this row, and accumulate
				squares += reduce(lambda acc, c: acc + int(c == '#'), l, 0)
				
			case State.Space:			
				(space, presents) = l.split(':')
				(width, height) = [int(x) for x in space.split("x")]
				presents = [int(p) for p in presents.strip().split(" ")]
				spaces.append((width, height))
				presentsToFit.append(presents)

		
# Count squares to see what can possibly fit. If a space fits all the specified presents, 
# then it's a sufficientSpace. 
sufficientSpaces = 0
for i in range(0, len(spaces)):
	area = spaces[i][0] * spaces[i][1]
	squaresNeeded = 0
	for shapeNumber in range(0, NUM_SHAPES):		
		squaresNeeded += presentSquares[shapeNumber] * presentsToFit[i][shapeNumber]
		
	if squaresNeeded <= area:
		sufficientSpaces += 1
print(sufficientSpaces)
	
		
			
			
		
			
