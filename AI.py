from __future__ import print_function #better print function
from Queue import PriorityQueue #will globaly keep track of cheapest states
import sys

class node(object): # node will hold current state of puzzle as well as potential next states 

	def __init__(self, _state = []):
		self.nodeState = _state # state array
		self.up = None # tuple(state array, space index)
		self.down = None # tuple(state array, space index)
		self.left = None # tuple(state array, space index)
		self.right = None # tuple(state array, space index)
		self.next = None  #tuple(up, down, left, right)
		self.space = None # self.state[space] represents empty space in current puzzle state 

		for i in range(len(self.nodeState)): #initialize space attribute. in puzzle, space is represented with 0
			if self.nodeState[i] == '0':
				self.space = i

	def nodePrintSpace(self): # will print space index of state array in node, mostly for debug
		print(self.space)

	def nodePrint(self, myFile = sys.stdout): # prints current state of node in 3x3 matix format, default output is stdout
		
		state = self.nodeState
		index = 0
		line = 0
		for i in range(3):
			for i in range(3):
				print(state[index] + ' ', end = '', file = myFile)
				index += 1
			print('', file = myFile)
			line += 1
		if line == 3:
			print('', file = myFile)

	def moveUp(self):
		#will move space up in the puzzle and add new state to 'up' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState[:]
		swap = self.space - 3 # index in state array where space will end up

		if ((0 <= swap < len(self.nodeState)) and (self.space != 0) and (self.space != 1) and (self.space != 2)):
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.up = (nextState, swap, 'U')
			return True
		else:
			self.up = (None, swap)
			return False
			

	def moveDown(self):
		#will move space down in the puzzle and add new state to 'down' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState[:]
		swap = self.space + 3 # index in state array where space will end up

		if ((0 <= swap < len(self.nodeState)) and (self.space != 6) and (self.space != 7) and (self.space != 8)):
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.down = (nextState, swap, 'D')
			return True
		else:
			self.down = (None, swap)
			return False

	def moveLeft(self):
		#will move space left in the puzzle and add new state to 'left' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState[:]
		swap = self.space - 1 # index in state array where space will end up

		if ((0 <= swap < len(self.nodeState)) and (self.space != 0) and (self.space != 3) and (self.space != 6)): # check if move is valid
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.left = (nextState, swap, 'L')
			return True
		else:
			self.left = (None, swap)
			return False

	def moveRight(self):
		#will move space right in the puzzle and add new state to 'right' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState[:]
		swap = self.space + 1 # index in state array where space will end up

		if ((0 <= swap < len(self.nodeState)) and (self.space != 2) and (self.space != 5) and (self.space != 8)):
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.right = (nextState, swap, 'R')
			return True
		else:
			self.right = (None, swap)
			return False

	def stateSearch(self):
		#will search next states of current state and set 'up', 'down', 'left', 'right'
		up, down, left, right = None, None, None, None

		if self.moveUp():
			up = self.up[:]
		if self.moveDown():
			down = self.down[:]
		if self.moveLeft():
			left = self.left[:]
		if self.moveRight():
			right = self.right[:]

		self.next = (up, down, left, right)

class PuzzleSearchTree(object): # this will be the search tree that looks for goal state

	def __init__(self, _root = node(), _goal = node()):
		self.root = _root
		self.goal = _goal
		self.goalMap = {} # hash mash map of index and values of goal state array 
		self.nextNode = _root # this is the next node to be chosen according to cost function, starts at root
		self.level = 0
		self.moves = ''
		self.movesCost = ''
		self.seen = {} # seen[state] = cost
		self.globalSeen = PriorityQueue() #keeps track of global min state 

		for i in range(len(self.goal.nodeState)): # sets goalMap
			self.goalMap[str(self.goal.nodeState[i])] = i

	def getRow(self, pieceIndex): #given index of single piece in state array, returns the row it's in
	
		if 0 <= pieceIndex <=2:
			return 0
		elif 3 <= pieceIndex <=5:
			return 1
		elif 6 <= pieceIndex <=8:
			return 2

	def getColumn(self, pieceIndex): #given index of single piece in state array, returns the column it's in
	
		if (pieceIndex == 0 or pieceIndex == 3 or pieceIndex == 6):
			return 0
		elif (pieceIndex == 1 or pieceIndex == 4 or pieceIndex == 7):
			return 1
		elif (pieceIndex == 2 or pieceIndex == 5 or pieceIndex == 8):
			return 2
	
	def cost(self, state, heuristic): # calculates cost of state - heuristics function

		index = 0
		cost = 0 # cost of state to be returned

		for i in range(3): #calculates array index difference between current state and node

			for j in range(3):

				if state[index] != '0': #not counting space in state cost calculation
					stateDiff = abs((self.getRow(self.goalMap[state[index]]) - i)) + abs(((self.goalMap[state[index]] % 3) - j)) #get state diff
				else:
					stateDiff = 0

				cost += stateDiff
				index += 1

		if (heuristic == '0'): 
			return cost  #cost of state, no linear conflic
		elif (heuristic == '1'): 
			return cost #cost of state + (2 * linear conflic)
		else: 
			quit()


 
	def search(self, heuristic = '0'):

		self.movesCost = str(self.cost(self.root.nodeState, heuristic)) + ' ' #add cost of initial state to moves cost string
		
		while (self.nextNode.nodeState != self.goal.nodeState): #while node state != goal state

			self.nextNode.stateSearch() #start next state search of current node
			self.level += 1 #incriment level, done at every state search/expansion of node

			for i in range(len(self.nextNode.next)): #loop through node's next states, check for None states

				if(self.nextNode.next[i] != None): # if not an invalid state
					state = self.nextNode.next[i][0]

					if (str(state) not in self.seen):
						self.seen[str(state)] =  (self.cost(state, heuristic) + self.level) #add state to seen along with it's cost
						self.globalSeen.put((self.seen[str(state)], self.nextNode.next[i]))

			#PRINT OUTPUT FOR DEBUG
			#print(self.nextNode.nodeState)
			#count = 0
			#while (count < len(self.nextNode.next)):
			#	if self.nextNode.next[count] != None:
			#		print(self.nextNode.next[count], end = ' ')
			#		print(self.cost(self.nextNode.next[count][0]))
			#	count += 1
			#print('')
			#PRINT OUT PUT END

			nodeNext = self.globalSeen.get() #get global minimum costly state out of those seen
			print(nodeNext[1], end = ' ') #debug
			print(nodeNext[0]) #debug
			print('')
			self.nextNode = node(nodeNext[1][0]) 
			self.moves = self.moves + nodeNext[1][2] + ' ' #add move to moves line
			self.movesCost = self.movesCost + str(nodeNext[0]) + ' ' #add move cost to moves line, includes depth

		#print(self.nextNode.nodeState) #debug 

def Read(input_file):
	
	inputState = [] #stores initial and goal states
	goalState = [] 
	lineCount = 1; #keeps track of how many lines read to distiguish input and goal states in file

	for line in input_file.readlines(): # iterate line by line
		for char in line:
			if (char != ' ') and (char != '\r') and (char != '\n'):
				if lineCount <= 3:
					inputState.append(char)
				else:
					goalState.append(char)

		lineCount += 1

	return inputState, goalState #returns both states as tuple, easier for assignment in calling function

def main():

	if (len(sys.argv) > 1): # if input file arg exists

		input_file = open(sys.argv[1] + '.txt', 'r') #opens input file
		inputState, goalState = Read(input_file) #grabs initial and goal states from file

		inputNode = node(inputState) #creates node object from input state
		goalNode = node(goalState) #creates node object from goal state

		searchTree = PuzzleSearchTree(inputNode, goalNode) #creates search tree object from input and goal states
		
		if (len(sys.argv) > 2): #will start search, defaults to manhattan distance heuristic (no linear conflict)
			searchTree.search(sys.argv[2])
		else:
			searchTree.search()

		output_file = open(sys.argv[1] + "_output.txt", "w+") #creates output file
		#next 6 lines write output to output_file
		inputNode.nodePrint(output_file)
		goalNode.nodePrint(output_file)
		print(searchTree.level, file = output_file)
		print(len(searchTree.seen), file = output_file)
		print(searchTree.moves, file = output_file)
		print(searchTree.movesCost, file = output_file)

	else:
		print("can't run without a file bud. try: python AI.py 'file.txt' ")

main()
