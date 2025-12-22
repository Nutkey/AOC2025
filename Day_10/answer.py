import argparse
import pdb
import math
import sys
import re
from functools import reduce
from itertools import combinations, combinations_with_replacement
import z3
parser = argparse.ArgumentParser()
parser.add_argument("inputfile")
parser.add_argument("--two", help="part two", action="store_true")
args = parser.parse_args()

def parseButton(b):
	b = b.strip("()")
	decimal = list(map(int, b.split(",")))
	# Convert a set of values to binary
	binary =  reduce(lambda acc,v: acc + (1 << v), decimal, 0)
	
	return (binary, decimal)

# Load machines


# We'll need a regex for one set of square brackets, multiple parentheses, one set of curl 
light_pattern = r"\[([\.#]*)\] "
button_pattern = r"((?:\([\d,]+\) ?)+)"
joltage_pattern = r".*\{([\d,]+)\}"
p = re.compile(light_pattern + button_pattern + joltage_pattern)
 
machines = []

with open(args.inputfile, "r+") as data:
	# Machine format is 
	# Each line contains a single indicator light diagram in [square brackets], 
	#		one or more button wiring schematics in (parentheses)
	#	    and joltage requirements in {curly braces}.
	for l in data:
		m = p.match(l)
		(ls, bs, js) = m.groups()
		# We have .#..  - convert to binary
		lsb = ls.replace('#', '1')
		lsb = lsb.replace('.', '0')
		lights = int(lsb[::-1], 2)
		
		# Also parse joltage  counters for part 2
		counters = list(map(int, js.split(',')))
		
		# Buttons in the form: (3) (1,3) (2) (2,3) (0,2) (0,1) 
		# Now parse entries of (...)
	
		buttons = [parseButton(b) for b in bs.strip().split(' ')]
		decimal = [b[1] for b in buttons]
	
		# Construct a matrix where each row indicates how a light is affected by that button
		buttonMatrix = []
	
		# Generate a matrix which can be multiplied by presses to yield a result, therefore in the form
		# [b1l1 b2l1 .... ], (where b1l1 is 1 or 0 depending on if b1 affects l1)
		# [b1l2 ..... ]
		# The shape is therefore num buttons wide, num lights high
		for l in range(0, len(counters)):
			row = [1 if l in decimal[i] else 0 for i in range(0, len(buttons))]
			buttonMatrix.append(row)
		
		machines.append((lights, buttons, counters, buttonMatrix))
		
# Part 1

# For each machine work out how to get the lights on, which means the shortest combo where the xor of all
# presses equals the target value. Start with single presses and work up
numPresses = 0
for (lights, buttons, _, _) in machines:
	done = False
	for i in range(1, len(buttons) + 1):
		for presses in combinations(buttons, i):
			if reduce(lambda acc, button: acc ^ button[0],presses, 0) == lights:
				numPresses += i
				done = True
				break
		if done:
			break		
	if not done:
		print("Failed to solve")
	
print(numPresses)
	
# Part 2
# We have partially complete linear equations, so use Z3. Once we have a solution, look for a smaller solution, until
# we fail to find one
def solve(cnts, btt):
	# Generate a variable for each button
	characters = "abcdefghijklmnopqrstuvwxyz"
	variables = [z3.Int(characters[b]) for b in range(0, len(buttons))]
	s = z3.Solver()
	for variable in variables:
		s.add(variable >= 0)
	while True:
		for effect, solution in zip(btt, cnts):
			affectedVariables = [variables[b] * effect[b] for b in range(0, len(buttons))]		
			s.add(reduce(lambda acc,x: acc + x, affectedVariables, 0) == solution)
		if s.check() == z3.sat:
			answer = s.model()
			presses = sum([answer[v].as_long() for v in variables])
			# Look for a smaller answer
			s.add(reduce(lambda acc,x: acc + x, variables, 0) < presses)
		else:
			return presses
	
	
num = 0
total = 0
for (_, buttons, counters, buttonMatrix) in machines:
	num += 1
	presses = solve(counters, buttonMatrix)
	total += presses
	
print(total)
