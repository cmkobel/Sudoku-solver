import random
import time
random.seed("vivoksnekanogsåværebange")

# Author: CMK

'''
~ todo ~
* tuples or lists?

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
			if row % 3 == 0: # seperate 3x3 squares horizontally
				result += "\n"
			for col in range(9):
				if col % 3 == 0:
					result += "  " # seperate 3x3 squares vertically
				result += str(self.problem[row][col]) + " " # write number
			result += "\n" # return after each of the rows
		return result

	
	# Finds the coordinate for the first zero (empty field)
	def first_empty_pos(self):
		for row in range(9):
			for col in range(9):
				if self.problem[row][col] == 0:
					return (row, col)
		return (9, 9) # (9, 9) doesn't exist as counting starts at 0. (9, 9) is simply a sign that there is no empty positions at all.


	# These three related helper functions gather main structures for rule checking
	# Return the row designated by the row_pointer (1x9)
	def row(self, row_in):
		return (i for i in self.problem[row_in])
	# Return the column (9x1)
	def column(self, col_in):		
		return (self.problem[i][col_in] for i in range(9))
	# Return the square (3x3)
	def square(self, coord_in):
		# build two dimensional list:
		list = ((self.problem[int(coord_in[0]/3)*3 + row][int(coord_in[1]/3)*3 + col] for col in range(3)) for row in range(3))
		# flatten. (the 2d structure is not important)
		return (item for sublist in list for item in sublist)


	# candidate() gives the set of possible candidates to fill in the pointed cell
	def candidates(self):
		# remove the numbers in the row, column and square. Left is the possible numbers for the spot
		result = {i for i in range(1, 10)} # numbers 0 .. 9
		result -= set(tuple(self.row(self.row_pointer))) # remove all numbers found in the associated row,
		result -= set(tuple(self.column(self.col_pointer))) # column,
		result -= set(tuple(self.square([self.row_pointer, self.col_pointer]))) # and square.
		return result


	# Returns true if all values are valid
	# It is strictly only necessary to call this method in the beginning of the search, as the algorithm should not be able to insert in-valid entries.
	def valid(self):
		for row_i in range(9):
			for col_i in range(9):
				# remove zeroes, as zero denotes a blank field.
				row = (val for val in self.row(row_i) if val != 0)
				col = (val for val in self.column(col_i) if val != 0)
				square = (val for val in self.square([row_i, col_i]) if val != 0)
				def has_duplicates(list):
					# If the length of a list is the same as the length of the set of the list, no duplicates can exist
					return len(list) != len(set(list))
				if has_duplicates(row) or has_duplicates(col) or has_duplicates(square):
					return False
		# If the loop has run throughout without the finding of any duplicates, the sudoku must be valid 
		return True


	# depth first tree next
	def next(self):
		# When sudoku is created, first check if it is solved and valid (technically, invalid sudokus should be impossible at this stage)
		if self.first_empty_pos() == (9, 9) and self.valid: # sudokuen er løst, base case
			print(self)
			if single_solution: quit()
			return # exit object in any case
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
			# transfer grid and insert proposed candidate
			child_problem = tuple(tuple(candidate if (i==self.row_pointer and j==self.col_pointer) else self.problem[i][j] for j in range(9)) for i in range(9))
			Sudoku_grid(child_problem).next() # A new object is spawned for every candidate proposed


def read_norvig2(input):
	# use map()?
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
parent.next()