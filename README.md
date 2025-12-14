# AOC2025
This year (2025) I noticed my friend and colleague Nick was committing regularly to a project repository I didn't recognise - "aoc-2025". On asking, I discovered 
[Advent of Code 2025](https://adventofcode.com/2025), and spent quite a few fun hours going through the problems. 

My solutions are largely in Python, though I did implement some in C++ or Java.

# Structure

Every folder `dayN` contains an

* `answer.py` which is the python script that can be executed to solve the problem for a provided input set of data
* `analysis.txt` - if present, discusses the complexity of the problem.
* `sample.txt` - the same input provided in the problem
* `input.txt` - the full input provided in the problem

To run the solver, execute the following shell commands
```
python -mvenv .venv
. ./.venv/bin/activate
pip install -rrequirements.txt
python answer.py <input file> [--two]
```
