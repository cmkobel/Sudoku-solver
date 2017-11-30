import random
import time
random.seed("vivoksnekanogsåværebange")

'''
??
* undgå flere instantieringer! (tidbesparelse) ? -Det er vel ikke muligt hvis alle muligheder skal undersøges?
* tupler eller lister?
'''

debug = False
single_solution = True
time_start = time.time()


# En representation af et sudoku-grid
class Sudoku_grid():
	def __init__(self, problem=None, row_pointer = 0, col_pointer = 0):
		self.problem = problem
		self.row_pointer = row_pointer
		self.col_pointer = col_pointer


	# pretty-printer
	def __str__(self): 
		result = "\nSolution: "
		for row in range(9):
			if row % 3 == 0: # separer kvadrater lodret
				result += "\n"
			for col in range(9):
				if col % 3 == 0:
					result += "  " # separer kvadrater vandret
				result += str(self.problem[row][col]) + " " # indsæt tal
			result += "\n" # skift linje efter hver række
		return result

	
	# Finder koordinatet for det første nul.
	def first_empty_pos(self):
		for row in range(9):
			for col in range(9):
				if self.problem[row][col] == 0:
					return (row, col)
		return (9, 9)


	# These three related helper functions gather main structures for rule checking
	# Return the row designated by the row_pointer
	def row(self, row_in):
		return (i for i in self.problem[row_in])
	# Return the column
	def column(self, col_in):		
		return (self.problem[i][col_in] for i in range(9))
	# Return the 3x3 square
	def square(self, coord_in):
		# build list:
		list = ((self.problem[int(coord_in[0]/3)*3 + row][int(coord_in[1]/3)*3 + col] for col in range(3)) for row in range(3))
		# flatten. (the 2d structure is not important)
		return (item for sublist in list for item in sublist)


	# Candidate gives the set of candidates for the pointed cell
	def candidates(self):
		# remove the numbers in the row, column and square. Left is the possible numbers for the spot
		result = {i for i in range(1, 10)}
		result -= set(tuple(self.row(self.row_pointer)))
		result -= set(tuple(self.column(self.col_pointer))) 
		result -= set(tuple(self.square([self.row_pointer, self.col_pointer])))
		return result


	# Returns true if all values are valid
	def valid(self):
		for row_i in range(9):
			for col_i in range(9): # er det ikke nok at gå diagonalt ned igennem?
				# fjern nuller fra listerne
				row = (val for val in self.row(row_i) if val != 0)
				col = (val for val in self.column(col_i) if val != 0)
				square = (val for val in self.square([row_i, col_i]) if val != 0)
				def has_duplicates(list):
					# hvis længden af en liste er det samme som længden af settet af listen, kan der ikke være duplikater
					return len(list) != len(set(list))
				if has_duplicates(row) or has_duplicates(col) or has_duplicates(square):
					return False
		# Hvis loopet har kørt igennem uden at finde nogle duplikater, må sudokuen være valid
		return True


	# depth first tree search
	def search(self):
		# When sudoku is created, first check if it is solved and valid (technically, invalid sudokus should be impossible at this stage)
		if self.first_empty_pos() == (9, 9) and self.valid: # sudokuen er løst, base case
			print(self)
			if single_solution: quit()
			return # og her vil jeg så gerne stoppe de andre
		# update pointer in the new sudoku_grid-object
		zero_coord = self.first_empty_pos()
		self.row_pointer, self.col_pointer = zero_coord[0], zero_coord[1]
		if self.candidates() == set():
			if debug: print(" Empty set, halting.", end="")
			return #halt
		candidates_list = self.candidates()
		for candidate in random.sample(candidates_list, len(candidates_list)): # først herefter det skal være rekursivt.
			#debug
			if debug: print("\nCandidate", candidate, "of", self.candidates(), "in coordinate:", [self.row_pointer, self.col_pointer], end="")
			# overfør grid og erstat candidate
			child_problem = tuple(tuple(candidate if (i==self.row_pointer and j==self.col_pointer) else self.problem[i][j] for j in range(9)) for i in range(9))
			#child_problem[self.row_pointer][self.col_pointer] = candidate # overfør kandidat til grid
			Sudoku_grid(child_problem).search() # lav et nyt objekt for hver kandidat


def read_norvig2(input):
	# brug evt map, så jeg ikke skal 
	grid = tuple(tuple(int(input[row*9+col%9]) if input[row*9+col%9] != "." else 0 for col in range(9)) for row in range(9))
	return grid




# parent = Sudoku_grid(( # initial

# 	(7,1,0,  0,9,0,  0,2,0),
# 	(3,0,0,  0,0,0,  7,1,0),
# 	(0,4,5,  0,0,6,  0,8,3),
	  
# 	(0,0,0,  0,0,5,  0,0,0),
# 	(9,3,7,  2,4,8,  6,5,1),
# 	(0,0,0,  9,0,0,  0,0,0),
	  
# 	(1,6,0,  4,0,0,  3,9,0),
# 	(0,8,3,  0,0,0,  0,0,2),
# 	(0,7,0,  0,2,0,  0,0,5)))


# parent = Sudoku_grid(( # diabolical

# 	(0,7,0,  2,5,0,  4,0,0),
# 	(8,0,0,  0,0,0,  9,0,3),
# 	(0,0,0,  0,0,3,  0,7,0),
	
# 	(7,0,0,  0,0,4,  0,2,0),
# 	(1,0,0,  0,0,0,  0,0,7),
# 	(0,4,0,  5,0,0,  0,0,8),
	
# 	(0,9,0,  6,0,0,  0,0,0),
# 	(4,0,1,  0,0,0,  0,0,5),
# 	(0,0,7,  0,8,2,  0,3,0)))

# parent = Sudoku_grid(( # short 

#   (7,1,8,  3,9,4,  5,2,6), 
#   (3,9,6,  5,8,2,  7,1,4), 
#   (2,4,5,  1,7,6,  9,8,3), 

#   (6,2,1,  7,3,5,  8,4,9), 
#   (9,3,7,  2,4,8,  6,5,1), 
#   (8,5,4,  9,6,1,  2,3,7), 

#   (1,6,2,  4,5,7,  3,9,8), 
#   (0,0,0,  0,0,0,  0,0,0), 
#   (0,0,0,  0,0,0,  0,0,0)))


# parent = Sudoku_grid(( # short solution

#   (7,1,8,  3,9,4,  5,2,6), 
#   (3,9,6,  5,8,2,  7,1,4), 
#   (2,4,5,  1,7,6,  9,8,3), 

#   (6,2,1,  7,3,5,  8,4,9), 
#   (9,3,7,  2,4,8,  6,5,1), 
#   (8,5,4,  9,6,1,  2,3,7), 

#   (1,6,2,  4,5,7,  3,9,8), 
#   (5,8,3,  6,1,9,  4,7,2), 
#   (4,7,9,  8,2,3,  1,6,0))) 

# parent = Sudoku_grid(( # empty
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	(0,0,0, 0,0,0, 0,0,0,),
# 	))


parent = Sudoku_grid(read_norvig2(".....6....59.....82....8....45........3........6..3.54...325..6.................."))
parent.search()