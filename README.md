# 8Puzzle-AI

Simple AI script that solves the classic 8 puzzle problem in python. This is still in the works but the core search algorithm is now working. The cost function calculates the sum of manhattan distances of each piece in the "board" from their counterparts in the goal state and picks the minimum costly state to advance to next. Option for different heuristic function is coming soon.

Input file format:

nnn
nnn
nnn

mmm
mmm
mmm

***************************

Output file format:

nnn 
nnn 
nnn

mmm 
mmm 
mmm

d
N
A A A A A A A ... ... ... ... f f f f f f f f f f ........
