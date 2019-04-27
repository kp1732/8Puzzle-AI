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
	
	def getConflicts(self, state): # finds linear conflicts between state and goal state

		conflict_cnt = 0

		#first row conflicts
		pair_01 = (state[0], state[1]) #pair_(index)(index)
		pair_02 = (state[0], state[2])
		pair_12 = (state[1], state[2])

		if (self.getRow(self.goalMap[pair_01[0]]) == 0 and self.getRow(self.goalMap[pair_01[1]]) == 0):
			if (self.goalMap[pair_01[0]] > self.goalMap[pair_01[1]]):
				#print("CONFLICT 01")
				conflict_cnt += 1

		if (self.getRow(self.goalMap[pair_02[0]]) == 0 and self.getRow(self.goalMap[pair_02[1]]) == 0):
			if (self.goalMap[pair_02[0]] > self.goalMap[pair_02[1]]):
				#print("CONFLICT 02")
				conflict_cnt += 1

		if (self.getRow(self.goalMap[pair_12[0]]) == 0 and self.getRow(self.goalMap[pair_12[1]]) == 0):
			if (self.goalMap[pair_12[0]] > self.goalMap[pair_12[1]]):
				#print("CONFLICT 12")
				conflict_cnt += 1

		#second row conflicts
		pair_34 = (state[3], state[4]) #pair_(index)(index)
		pair_35 = (state[3], state[5])
		pair_45 = (state[4], state[5])

		if (self.getRow(self.goalMap[pair_34[0]]) == 1 and self.getRow(self.goalMap[pair_34[1]]) == 1):
			if (self.goalMap[pair_34[0]] > self.goalMap[pair_34[1]]):
				#print("CONFLICT 34")
				conflict_cnt += 1

		if (self.getRow(self.goalMap[pair_35[0]]) == 1 and self.getRow(self.goalMap[pair_35[1]]) == 1):
			if (self.goalMap[pair_35[0]] > self.goalMap[pair_35[1]]):
				#print("CONFLICT 35")
				conflict_cnt += 1

		if (self.getRow(self.goalMap[pair_45[0]]) == 1 and self.getRow(self.goalMap[pair_45[1]]) == 1):
			if (self.goalMap[pair_45[0]] > self.goalMap[pair_45[1]]):
				#print("CONFLICT 45")
				conflict_cnt += 1

		#third row conflicts
		pair_67 = (state[6], state[7]) #pair_(index)(index)
		pair_68 = (state[6], state[8])
		pair_78 = (state[7], state[8])

		if (self.getRow(self.goalMap[pair_67[0]]) == 2 and self.getRow(self.goalMap[pair_67[1]]) == 2):
			if (self.goalMap[pair_67[0]] > self.goalMap[pair_67[1]]):
				#print("CONFLICT 67")
				conflict_cnt += 1

		if (self.getRow(self.goalMap[pair_68[0]]) == 2 and self.getRow(self.goalMap[pair_68[1]]) == 2):
			if (self.goalMap[pair_68[0]] > self.goalMap[pair_68[1]]):
				#print("CONFLICT 68")
				conflict_cnt += 1

		if (self.getRow(self.goalMap[pair_78[0]]) == 2 and self.getRow(self.goalMap[pair_78[1]]) == 2):
			if (self.goalMap[pair_78[0]] > self.goalMap[pair_78[1]]):
				#print("CONFLICT 78")
				conflict_cnt += 1

		#first column conflicts
		pair_03 = (state[0], state[3]) #pair_(index)(index)
		pair_06 = (state[0], state[6])
		pair_36 = (state[3], state[6])

		if (self.getColumn(self.goalMap[pair_03[0]]) == 0 and self.getColumn(self.goalMap[pair_03[1]]) == 0):
			if (self.goalMap[pair_03[0]] > self.goalMap[pair_03[1]]):
				#print("CONFLICT 03")
				conflict_cnt += 1

		if (self.getColumn(self.goalMap[pair_06[0]]) == 0 and self.getColumn(self.goalMap[pair_06[1]]) == 0):
			if (self.goalMap[pair_06[0]] > self.goalMap[pair_06[1]]):
				#print("CONFLICT 06")
				conflict_cnt += 1

		if (self.getColumn(self.goalMap[pair_36[0]]) == 0 and self.getColumn(self.goalMap[pair_36[1]]) == 0):
			if (self.goalMap[pair_36[0]] > self.goalMap[pair_36[1]]):
				#print("CONFLICT 36")
				conflict_cnt += 1

		#second column conflicts
		pair_14 = (state[1], state[4]) #pair_(index)(index)
		pair_17 = (state[1], state[7])
		pair_47 = (state[4], state[7])

		if (self.getColumn(self.goalMap[pair_14[0]]) == 1 and self.getColumn(self.goalMap[pair_14[1]]) == 1):
			if (self.goalMap[pair_14[0]] > self.goalMap[pair_14[1]]):
				#print("CONFLICT 03")
				conflict_cnt += 1

		if (self.getColumn(self.goalMap[pair_17[0]]) == 1 and self.getColumn(self.goalMap[pair_17[1]]) == 1):
			if (self.goalMap[pair_17[0]] > self.goalMap[pair_17[1]]):
				#print("CONFLICT 06")
				conflict_cnt += 1

		if (self.getColumn(self.goalMap[pair_47[0]]) == 1 and self.getColumn(self.goalMap[pair_47[1]]) == 1):
			if (self.goalMap[pair_47[0]] > self.goalMap[pair_47[1]]):
				#print("CONFLICT 36")
				conflict_cnt += 1

		#third column conflicts
		pair_25 = (state[2], state[5]) #pair_(index)(index)
		pair_28 = (state[2], state[8])
		pair_58 = (state[5], state[8])

		if (self.getColumn(self.goalMap[pair_25[0]]) == 2 and self.getColumn(self.goalMap[pair_25[1]]) == 2):
			if (self.goalMap[pair_25[0]] > self.goalMap[pair_25[1]]):
				#print("CONFLICT 03")
				conflict_cnt += 1

		if (self.getColumn(self.goalMap[pair_28[0]]) == 2 and self.getColumn(self.goalMap[pair_28[1]]) == 2):
			if (self.goalMap[pair_28[0]] > self.goalMap[pair_28[1]]):
				#print("CONFLICT 06")
				conflict_cnt += 1

		if (self.getColumn(self.goalMap[pair_58[0]]) == 2 and self.getColumn(self.goalMap[pair_58[1]]) == 2):
			if (self.goalMap[pair_58[0]] > self.goalMap[pair_58[1]]):
				#print("CONFLICT 36")
				conflict_cnt += 1

		return conflict_cnt

	def cost(self, state, heuristic): # calculates cost of state - heuristics function

		index = 0
		cost = 0 # cost of state to be returned

		for i in range(3): #calculates array index difference between current state and node
			for j in range(3):
				if state[index] != '0': #not counting space in state cost calculation
					#stateDiff = horizontal moves + vertival moves
					stateDiff = abs((self.getRow(self.goalMap[state[index]]) - i)) + abs(((self.getColumn(self.goalMap[state[index]])) - j))
				else:
					stateDiff = 0

				cost += stateDiff
				index += 1

		if (heuristic == '-m'): 
			return cost  #cost of state, no linear conflic

		elif (heuristic == '-l'): 
			conflict_cnt = self.getConflicts(state)
			return cost + (2 * conflict_cnt) #cost of state + (2 * linear conflic)

		else: 
			print("INVALID HEURISTIC SELECTION")
			quit()


 
	def search(self, heuristic = '-m'):

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
			#		print(self.cost(self.nextNode.next[count][0], heuristic))
			#	count += 1
			#print('')
			#PRINT OUT PUT END

			nodeNext = self.globalSeen.get() #get global minimum costly state out of those seen
			#print(nodeNext[1], end = ' ') #debug
			#print(nodeNext[0]) #debug
			#print('') #debug
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
		
		if (len(sys.argv) > 2): #pass cmd line argument and set heuristic_name for output file
			searchTree.search(sys.argv[2])
			if (sys.argv[2] == '-l'):
				heuristic_name = 'linear_conflict'
			else:
				heuristic_name = 'manhattan'
		else:
			searchTree.search()
			heuristic_name = 'manhattan'

		output_file = open(sys.argv[1] + '_output_' + heuristic_name + '.txt', 'w+') #creates output file

		#next 6 lines write output to output_file
		inputNode.nodePrint(output_file)
		goalNode.nodePrint(output_file)
		print(searchTree.level, file = output_file)
		print(len(searchTree.seen), file = output_file)
		print(searchTree.moves, file = output_file)
		print(searchTree.movesCost, file = output_file)

	else:
		print("can't run without a file. try: python AI.py 'file.txt' ")

main()
