############################################################
# CIS 521: Homework 4
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import numpy
from Queue import Queue
import copy, random
from collections import deque

############################################################
# Section 1: Sudoku
############################################################
#maybe change from list 
def sudoku_cells():
    cell_list = []
    for i in range(9):
        for j in range(9):
            cell_list += [(i, j)]
    return cell_list

#constraints
def three_by_three(): 
    square_num = {0:set(), 1:set(), 2:set(), 3:set(), 4:set(), 5:set(), 6:set(), 7:set(), 8:set()}
    for i in range(9):
        for j in range(9):
            idx = 3*(i/3) + j/3
            square_num[idx].add((i,j))
    return square_num

def sudoku_arcs():
    #change to queue if not working
    arcs  = set()
    squares = three_by_three()
    cells = sudoku_cells()
    for cell in cells:
        idx = 3*(cell[0]/3) + cell[1]/3
        for square_cell in squares[idx]:
            arcs.add((cell, square_cell))
        for rest in range(9):
            arcs.add((cell,(cell[0], rest)))
            arcs.add((cell,(rest, cell[1])))
        arcs.remove((cell,cell))
    return arcs


            
def read_board(path):
    board_dic = {}
    i = 0
    j = 0
    # Looping through characters in file
    f = open(path, 'r')
    lines = f.readlines()
    b = [[ch for ch in l.strip() if (ch !='\r' or ch != '\n')] for l in lines]
    [[board_dic.update({(i,j):ch}) for j,ch in enumerate(l)]for i,l in enumerate(b)]
    for ch in iter(lambda: f.read(1), ''):
        if ch == '\r':
            j = 0
            i += 1
            continue
        if ch == '\n':
            continue
        # board_dic[(i, j)] = ch
        j += 1
    return board_dic


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    SQUARE = three_by_three()

    def __init__(self, board):
        # DO DIC STUFF IN HEUUR
        self.board = board
        if type(board[board.keys()[-1]]) is str:
            for key in board:
                if(board[key] == "*"):
                    board[key] = set([1, 2, 3, 4, 5, 6, 7, 8, 9])
                else:
                    board[key] = set([int(board[key])])

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        ## print len(self.board[cell1])
        ## print numpy.size(self.board[cell2])
        if(len(self.board[cell1]) > 1 and len(self.board[cell2]) > 1):
            return False
        if(len(self.board[cell1])  == 1 and len(self.board[cell2]) == 1):
            return False
        if(len(self.board[cell1])  == 1):
            constraint = self.board[cell1].pop()
            self.board[cell1].add(constraint)
            if(constraint in self.board[cell2]):
                self.board[cell2].remove(constraint)
            # self.board[cell2] -= self.board[cell1]
                return True
            # remove conflicting number from list
        else:
            constraint = self.board[cell2].pop()
            self.board[cell2].add(constraint)
            if(constraint in self.board[cell1]):
                self.board[cell1].remove(constraint)
            # self.board[cell1] -= self.board[cell2]
                return True
        return False
            # ONLY USE AC3

    def find_neighbors(self, cell, pop_cell): 
        neighbor = set()
        # squares = self.SQUARE
        idx = 3*(cell[0]/3) + cell[1]/3
        for square_cell in self.SQUARE[idx]:
                neighbor.add((square_cell, cell))
        for rest in range(9):
            neighbor.add(((cell[0], rest),cell))
            neighbor.add(((rest, cell[1]),cell))
        # neighbor.remove((pop_cell, cell))
        neighbor.remove((cell, cell))
        ## print "Number of Neighbors: ",len(neighbor)
        return neighbor

    def infer_ac3(self):
        # while (not self.ARCS.empty()):
        while (self.ARCS):
            cell_pair = self.ARCS.pop()
            # cell_pair = self.ARCS.get()
            try :
                (len(self.board[cell_pair[0]]))
            except KeyError:
                print cell_pair
                for key in sorted(self.board):
                    print "%s: %s" % (key,self.board[key])
            try:
                (len(self.board[cell_pair[1]]))
            except KeyError:
                print cell_pair
                for key in sorted(self.board):
                    print "%s: %s" % (key,self.board[key])
            if(len(self.board[cell_pair[0]]) == 1 and len(self.board[cell_pair[1]]) == 1):
                if(self.board[cell_pair[0]] == self.board[cell_pair[1]]):
                   # print self.board
                   # print "bad puzzle, same number in pair:%s and %s" %(cell_pair[0], cell_pair[1])
                    return False, self.board
            if(self.remove_inconsistent_values(cell_pair[0],cell_pair[1])):
                neighbors = self.find_neighbors(cell_pair[0],cell_pair[1])
                for neighbor_cells in neighbors:
                    if(neighbor_cells != cell_pair[1]):
                        self.ARCS.add(neighbor_cells)
                        # self.ARCS.add(neighbor_cells)
        return True, self.board

    def check_squares(self, cell):
        replace = False
        idx = 3*(cell[0]/3) + cell[1]/3
        if len(self.board[cell])  == 1: 
            return True 
        row_cells = set()
        col_cells = set()
        square_cells= set()
        [row_cells.update(self.board[(cell[0],cc)]) for cc in range(9) if cc != cell[1]]
        [col_cells.update(self.board[(cc, cell[1])]) for cc in range(9) if cc != cell[0]]
        ## print "CELL %s, CONSTRAINTS %s" % (cell, self.board[cell])
        [square_cells.update(self.board[s_cell]) for s_cell in self.SQUARE[idx] if s_cell != cell]
        ## print square_cells
        for constraint in self.board[cell]:
            if constraint not in row_cells:
                self.board[cell] = set([constraint])
                return True
            if constraint not in col_cells:
                self.board[cell] = set([constraint])
                return True
            if constraint not in square_cells:
                self.board[cell] = set([constraint])
                return True
        return False

    def infer_improved(self):
        # pass
        i = 0
        solution = {}
        solved = False
        replace = False
        repeating = False 
        conflict = True
        undetermined = Queue()
        self.infer_ac3()
        for key in self.board:
            if(len(self.board[key]) > 1):
                undetermined.put(key)
        # while (not undetermined.empty()):
       # print "am i stuck in improved?"
        original_size = undetermined.qsize()
        solution = copy.deepcopy(self.board)
        new_board = {}
        # while(not repeating and not undetermined.empty()):
        while(not undetermined.empty()):
            prev_size = copy.deepcopy(undetermined.qsize())
            cell = undetermined.get()
            solution = copy.deepcopy(self.board)
            if(self.check_squares(cell)):
                for neighbor_cells in self.find_neighbors(cell, cell):
                    self.ARCS.add(neighbor_cells)
                    # self.ARCS.put(neighbor_cells)
                conflict, new_board = self.infer_ac3()
                if(not conflict):
                    return False, self.board
                # if(solution == dummy):
                #     repeating = True
                # solution = copy.deepcopy(new_board)
                # solution = copy.deepcopy(self.board)

            else:
                ## print "CELL %s: BOARD %s " % (cell, self.board[cell])
                undetermined.put(cell)
            # if(prev_size == undetermined.qsize()):
            #     if(i > original_size*original_size):
            #         repeating = True
            #         # print "repeated how manytimes ",i 
            #         return False, self.board
            #     i+=1 
        if undetermined.empty():
            solved = True
       # print "Solved infer_1: ",solved
        return solved, self.board

    def infer_improved_2(self):
        i = 0 
        solution = {}
        solved = False
        replace = False
        repeating = False 
        conflict = True
        undetermined = Queue()
        self.infer_ac3()
        for key in self.board:
            if(len(self.board[key]) > 1):
                undetermined.put(key)
        # while (not undetermined.empty()):
       # print "am i stuck in improved?"
        original_size = undetermined.qsize()
        solution = copy.deepcopy(self.board)
        new_board = {}
        # while(not repeating and not undetermined.empty()):
        while(not undetermined.empty()):
            prev_size = copy.deepcopy(undetermined.qsize())
            cell = undetermined.get()
            solution = copy.deepcopy(self.board)
            if(self.check_squares(cell)):

                for neighbor_cells in self.find_neighbors(cell, cell):
                    self.ARCS.add(neighbor_cells)
                conflict, new_board = self.infer_ac3()
                if(not conflict):
                    return False, self.board
                if(solution == new_board):
                    return False, self.board


                #     repeating = True
                # solution = copy.deepcopy(new_board)
                # solution = copy.deepcopy(self.board)

            else:
                ## print "CELL %s: BOARD %s " % (cell, self.board[cell])
                undetermined.put(cell)
            if(prev_size == undetermined.qsize()):
                # print "Original %s : times %i" %(original_size,i)
                if(i > original_size*original_size):
                    return False, new_board
                i+=1 
            else:
                i = 0 
            if(solution == new_board and i > original_size):
                return False, new_board
        if undetermined.empty():
            solved = True
       # print "Solved infer_1: ",solved
        return solved, self.board


    def guess(self, undetermined, visited, solve):
        if(solve):
            solved, state_board = self.infer_improved_2()
            if(solved):
                return True, state_board
            if (len(undetermined) == 0):
                return False, state_board
        while(undetermined):
            cell = undetermined.popleft()
            for num in self.board[cell]:
                # rand = random.choice(list(self.board[cell]))
                new_game = Sudoku(copy.deepcopy(self.board))
                new_game.board[cell] = set([num])
                solved, child_board = new_game.guess(undetermined, visited, True)
                if(solved):
                    print "Solved!"
                    return True, child_board
                else:
                    print "NOpe" 
        visited = {}
       # print "confused"
        return False, self.board



    def infer_with_guessing(self):
        random.seed('rndom seed') 
        solved, state_board = self.infer_improved_2()
        if(solved):
            return True, self.board
        undetermined = deque()
        for key in self.board:
            if(len(self.board[key]) > 1):
                undetermined.append(key)
        return self.guess(undetermined, {}, False) 
############################################################
# Section 2: Feedback
############################################################

feedback_question_1 = """
10 hours 
"""

feedback_question_2 = """
Figuring out the inference for medium 
"""

feedback_question_3 = """
I like how we are focusing on one problem 
"""
