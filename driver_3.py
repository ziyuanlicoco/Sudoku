#Ziyuan Li
#zl2824

import time
import sys
import math

ROW = "ABCDEFGHI"
COL = "123456789"
ROW1 = "ABC"
ROW2 = "DEF"
ROW3 = "GHI"

def print_board(board):
	"""Helper function to print board in a square."""
	print("-----------------")
	for i in ROW:
		row = ''
		for j in COL:
			row += (str(board[i + j]) + " ")
		print(row)


def board_to_string(board):
	"""Helper function to convert board dictionary to string for writing."""
	ordered_vals = []
	for r in ROW:
		for c in COL:
			ordered_vals.append(str(board[r + c]))
	return ''.join(ordered_vals)


def backtracking(board):
	global solved_board
	assignment_complete = False
	variable = select_unassigned_var(board)

	if len(variable) == 0:
		solved_board = board
		return 1 #if all grids are assigned, problem solved

	else:
		value = remain_value(board,variable)
		#using minimum remaining value heuristic
		min_list = []
		min_length = 99
		for vlist in value:
			if len(vlist)< min_length:
				min_length = len(vlist)
				min_list = []
				ind = value.index(vlist)
				min_list.append([variable[ind], vlist])
			if len(vlist) == min_length:
				min_list.append([variable[ind], vlist])

		item = min_list[0] #if there are more than one grid that have the mrv, just choose the first one
		r = item[0][0]
		c = item[0][1]
		valuelist = item[1]
		while len(valuelist)!= 0:
			v = valuelist[0]
			valuelist.remove(v)
			if forwardchecking(value,variable, v, r, c): #check with forward checking
				board[r+str(c)] = v #if no conflict, we assign the value first
				if backtracking(board): #then try to complete the rest of the board
					return 1 #if succeed, this assignment is correct
				else: #if not, that is the board has no solution in the end
					board[r+str(c)] = 0 #this value is not correct, we convert it into unassigned and check the next possible value
	return 0


def forwardchecking(value, variable, v, r, c):
	a = math.ceil(int(c)/3)*3-2
	b = math.ceil(int(c)/3)*3+1
	for rr in ROW:
		check = rr+str(c)
		if rr == r:
			continue
		if check not in variable:
			continue
		index = variable.index(rr+c)
		current_list = value[index]
		if len(current_list) == 1:
			if current_list[0] == v:
				return 0 #if any unassigned grid in the column has no value in domain, this assinment is not valid
		else:
			current_list.append(v)

	for cc in COL:
		check = r+str(cc)
		if cc == c:
			continue
		if check not in variable:
			continue
		index = variable.index(r+cc)
		current_list = value[index]
		if len(current_list) == 1:
			if current_list[0] == v:
				return 0 #if any unassigned grid in the row has no value in domain, this assinment is not valid

	if r in ROW1:
		for rrr in ROW1:
			for ccc in range(a,b):
				check = rrr+str(ccc)
				if rrr == r and ccc == c:
					continue
				if check not in variable:
					continue
				index = variable.index(rrr+str(ccc))
				current_list = value[index]
				if len(current_list) == 1:
					if current_list[0] == v:
						return 0 #if any unassigned grid in the box has no value in domain, this assinment is not valid
			
	if r in ROW2:
		for rrr in ROW2:
			for ccc in range(a,b):
				check = rrr+str(ccc)
				if rrr == r and ccc == c:
					continue
				if check not in variable:
					continue
				index = variable.index(rrr+str(ccc))
				current_list = value[index]
				if len(current_list) == 1:
					if current_list[0] == v:
						return 0

	if r in ROW3:
		for rrr in ROW3:
			for ccc in range(a,b):
				check = rrr+str(ccc)
				if rrr == r and ccc == c:
					continue
				if check not in variable:
					continue
				index = variable.index(rrr+str(ccc))
				current_list = value[index]
				if len(current_list) == 1:
					if current_list[0] == v:
						return 0

	return 1 #if no conflict is caused, this value is possible and should not be eliminated

def select_unassigned_var(board): #find all grids that has not been assigned a value
	unassigned = []
	for r in ROW:
		for c in COL:
			if board[r+c] == 0:
				unassigned.append(r+c) #the list stores the dictionary of the unassigned grids
	return unassigned

def remain_value(board,variable): #find all possible values for unasigned grids
	remain = []
	for rc in variable:
		r = rc[0]
		c = rc[1]
		a = math.ceil(int(c)/3)*3-2
		b = math.ceil(int(c)/3)*3+1
		value_List = [1,2,3,4,5,6,7,8,9] #start with all numbers from 1 to 9
		for cc in COL: #remove all numbers exists in the same row
			key = board[r+cc]
			if key in value_List:
				value_List.remove(key)
		for rr in ROW: #remove all numbers exists in the same column
			key = board[rr+c]
			if key in value_List:
				value_List.remove(key)
		
		if r in ROW1:
			for rrr in ROW1:
				for ccc in range(a,b): #find the 3x3 box the grid is in
					key = board[rrr+str(ccc)]
					if key in value_List:
						value_List.remove(key) #remove all numbers exists in the box
		if r in ROW2:
			for rrr in ROW2:
				for ccc in range(a,b):
					key = board[rrr+str(ccc)]
					if key in value_List:
						value_List.remove(key)
		if r in ROW3:
			for rrr in ROW3:
				for ccc in range(a,b):
					key = board[rrr+str(ccc)]
					if key in value_List:
						value_List.remove(key)
		remain.append(value_List)

	return remain


if __name__ == '__main__':
	startboard = sys.argv[1]
	#  Read boards from source.
	#src_filename = 'sudokus_start.txt'
	#try:
		#srcfile = open(src_filename, "r")
		#sudoku_list = srcfile.read()
	#except:
		#print("Error reading the sudoku file %s" % src_filename)
		#exit()

	# Setup output file
	out_filename = 'output.txt'
	outfile = open(out_filename, "w")

	# Solve each board using backtracking
	#for line in sudoku_list.split("\n"):
		
	start_time = time.process_time();

	#if len(startboard) < 9:
		#continue

	# Parse boards to dict representation, scanning board L to R, Up to Down
	board = { ROW[r] + COL[c]: int(startboard[9*r+c])
			  for r in range(9) for c in range(9)}

	#print_board(board)

	# Solve with backtracking
	backtracking(board)
	process_time = time.process_time() - start_time

	#print_board(solved_board)
	#print(process_time)


	# Write board to file
	outfile.write(board_to_string(solved_board))
	#outfile.write('\n')


	print("Finishing all boards in file.")