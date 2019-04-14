from __future__ import print_function

class node: # node will hold current state of puzzle as well as potential next states 

	def __init__(self, _state = []):
		self.nodeState = _state
		self.up = None
		self.down = None
		self.left = None
		self.right = None
		self.next = None 
		self.cost = None # cost of current state from goal node
		self.space = None # self.state[space] represents empty space in puzzle state 

		for i in range(len(self.nodeState)): #initialize space attribute, in puzzle space = 0
			if self.nodeState[i] == '0':
				self.space = i

	def nodePrintSpace(self): # will print space index of state array in node
		print(self.down)

	def nodePrint(self): # prints current state of node
		"""will print state array in 3x3 matrix format"""
		index = 0
		line = 0
		for i in range(3):
			for i in range(3):
				print(self.nodeState[index] + ' ', end = '')
				index += 1
			print('')
			line += 1

		if line == 3:
			print('')

	def moveUp(self):
		#will move space up in the puzzle and add new state to 'up' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState
		swap = self.space - 3 # index in state array where space will end up

		if 0 <= swap <= len(self.nodeState): # check if move is valid
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.up = nextState



	def moveDown(self):
		#will move space down in the puzzle and add new state to 'down' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState
		swap = self.space + 3 # index in state array where space will end up

		if 0 <= swap <= len(self.nodeState): # check if move is valid
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.down = nextState

	def moveLeft(self):
		#will move space left in the puzzle and add new state to 'left' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState
		swap = self.space - 1 # index in state array where space will end up

		if 0 <= swap <= len(self.nodeState): # check if move is valid
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.left = nextState

	def moveRight(self):
		#will move space right in the puzzle and add new state to 'right' attribute - DOES NOT CHANGE nodeState
		nextState = self.nodeState
		swap = self.space + 1 # index in state array where space will end up

		if 0 <= swap <= len(self.nodeState): # check if move is valid
			temp = nextState[self.space]
			nextState[self.space] = nextState[swap]
			nextState[swap] = temp
			self.right = nextState

	def search(self, debug = None):
		#will search all possible next states of current state and set 'up', 'down', 'left', 'right'
		self.moveUp()
		self.moveDown()
		self.moveLeft()
		self.moveRight()

		if debug == 1:
			print(self.up)
			print(self.down)
			print(self.left)
			print(self.right)

class tree: # this will be the search tree that looks for goal state

	def __init__(self, _root = node()):
		self.root = _root



def Read(input_file):

	#stores initial and goal states
	inputState = []
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

	input_file = open('input2.txt', 'r')
	
	inputState = [] #stores initial state
	goalState = [] #stores goal state

	inputState, goalState = Read(input_file) #grabs initial and goal states from file

	inputNode = node(inputState)
	goalNode = node(goalState)

	inputNode.nodePrint()
	inputNode.moveDown()
	inputNode.nodePrintSpace()


main()