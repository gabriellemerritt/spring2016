############################################################
# CIS 521: Homework 2
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import numpy
import math
import copy
import random
from collections import deque


############################################################
# Section 1: N-Queens
############################################################


def num_placements_all(n):
    result = math.factorial(n * n) / \
        (math.factorial(n) * math.factorial(n * n - n))
    return result


def num_placements_one_per_row(n):
    return n**n


def n_queens_valid(board):
    invalid_list = []
    count = 0
    for i, i_queen in enumerate(board):
        for j, j_queen in enumerate(board):
            if(i == j):
                continue
            if(i_queen == j_queen):
                count += 1
            if (abs(j_queen - i_queen) == abs(j - i)):
                count += 1
    if(count):
        return False
    # print invalid_list
    return True


def board_in_solution(board, solution):
    if(not solution):
        return False
    result = [elem for elem in solution if board == elem]
    if (not result):
        return False
    else:
        return True


def n_queens_helper(n, board):
    board += [0]
    new_queue = []
    for i in range(n):
        board[-1] = i
        if(n_queens_valid(board)):
            new_queue.append(copy.deepcopy(board))
    return new_queue


def search_combos(n, board_queue):
    ret_queue = []
    while(not board_queue or len(board_queue[-1]) < n):
        for board in board_queue:
            ret_queue += n_queens_helper(n, board)
            board_queue = ret_queue
        ret_queue = []
    return board_queue


def n_queens_solutions(n):
    board_list = [[]]
    board_list = search_combos(n, board_list)
    for board in board_list:
        yield board

############################################################
# Section 2: Lights Out
############################################################


class LightsOutPuzzle(object):

    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.m = len(board)
        self.n = len(board[0])

    def get_board(self):
        return self.board

    def set_state(self, row, col):
        self.board[row][col] = not self.board[row][col]

    def perform_move(self, row, col):
        cols = [elem[col] for elem in self.board]
        [(self.set_state(r, col)) for (r, tf) in enumerate(cols) if (
            r == row or r == row - 1 or r == row + 1)]
        [(self.set_state(row, c)) for (c, tf) in enumerate(self.board[row]) if(
            c == col - 1 or c == col + 1)]

    def scramble(self):
        for i in range(self.m):
            for j in range(self.n):
                if(random.random() < 0.5):
                    self.perform_move(i, j)

    def is_solved(self):
        for i in xrange(self.m): 
            for j in range(self.n): 
                if(self.board[i][j]):
                    return False
        # truth_idx = [x for x in range(self.m) if any(self.board[x]) is True]
        # if(truth_idx):
            # return False
        # else:
        #     return True
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        success = []
        for i in range(self.m):
            for j in range(self.n):
                new_b = self.copy()
                new_b.perform_move(i, j)
                success.append(((i, j), new_b))
        return success

    def solution_helper(self, visited, to_explore, bfs_level, node_num, parent):
        root = to_explore.pop(0)
        ml = []
        for move, state in root.successors():
            board_state = tuple(state.get_board())
            if(state.is_solved()):
                ml += [[move, parent, node_num]]
                # ml += [node_num]
                to_explore = []
                bfs_level[parent] = ml
                return bfs_level, visited, to_explore, node_num, True

            if(board_state not in visited):
                visited += [board_state]
                ml += [[move, parent, node_num]]
                # ml += [node_num]
                to_explore += [state]
            node_num += 1

        bfs_level[parent] = ml
        return bfs_level, visited, to_explore, node_num, False

    def find_solution(self):
        if(self.is_solved()):
            return None
        root = self.copy()
        result = []
        visited = []
        to_explore = [root]
        node_num = 1
        tree = {}
        parent = 0
        solved = False
        while(to_explore):
            (tree, visted, to_explore, node_num, solved) = \
                self.solution_helper(
                    visited, to_explore, tree, node_num, parent)
            parent += 1
        if(solved):
            result = tree[tree.keys()[-1]][-1]
            final_move = [result[0]]
            parent_idx = result[1]
            print parent_idx, final_move
            # print tree
            print
            # print tree
            print tree[tree.keys()[-1]]
            while (parent_idx != 0):
                for key in tree:
                    for item in tree[key]:
                        if(item[2] == parent_idx):
                            final_move.insert(0, item[0])
                            parent_idx = copy.deepcopy(item[1])
                            print item
                            break
            # final_move.pop(0)
            return final_move
        else:
            print "Not solvable"
            return None


def create_puzzle(rows, cols):
    puzzle = [[False for c in range(cols)] for r in range(rows)]
    return LightsOutPuzzle(puzzle)

############################################################
# Section 3: Linear Disk Movement
############################################################


def place_disk_order(graph, key, disk_num):
    # disk = [False, disk_num]
    graph[key] = copy.deepcopy(disk_num)


def place_disk_bool(graph, key, disk_num):
    # disk = [False, disk_num]
    graph[key] = True


def is_unordered_solved(graph, length, n):
    decrement = length - 1 - n
    if(not graph[length - 1]):
        return False
    for i in range(length - 1, decrement, -1):
        if(not graph[i]):
            return False
    return True


def disk_bfs(to_explore, visited, move_dict, length, n, parent, id_num):
    state = to_explore.pop(0)
    move_idxs = []
    state_set = valid_move_set(state, length, n)
    for move, s in state_set:
        if (is_unordered_solved(s, length, n)):
            visited += [move]
            move_idxs += [id_num]
            move_dict[parent] = move_idxs
            to_explore = []
            return id_num, to_explore, move_dict, visited, True
        elif s not in visited:
            visited += [move]
            move_idxs += [id_num]
            to_explore += [s]
        id_num += 1
    move_dict[parent] = move_idxs
    return id_num, to_explore, move_dict, visited, False


def valid_move_set(graph, length, n):
    state = copy.deepcopy(graph)
    state_set = []
    move_set = []
    move = ()
    for i, cell in enumerate(graph):
        if(cell):
            if(i + 2 < length and graph[i + 1] and not graph[i + 2]):
                state[i + 2] = True
                state[i] = False
                move = (i, i + 2)
            elif (i + 1 < length and not graph[i + 1]):
                state[i + 1] = True
                state[i] = False
                move = (i, i + 1)
            else:
                continue
            state_set += [[move, state]]
            state = copy.deepcopy(graph)
    # print move_set
    return state_set


def solve_identical_disks(length, n):
    graph = []
    graph += [False for i in range(length)]
    [[place_disk_bool(graph, i, num) for num in range(i + 1)]
     for i in range(length) if i < n]
    to_explore = [graph]
    visited = []
    move_dict = {}
    parent = 0
    id_num = 0
    solved = False
    while(to_explore):
        (id_num, to_explore, move_dict, visited, solved) = disk_bfs(
            to_explore, visited, move_dict, length, n, parent, id_num)
        parent += 1
    if(solved):
        last_key = move_dict.keys()[-1]
        last_idx = move_dict[last_key][-1]
        final_moves = [visited[last_idx]]
        while (last_key != 0):
            for keys in move_dict:
                for id_num in move_dict[keys]:
                    if(last_key == id_num):
                        final_moves.insert(0, visited[id_num - 1])
                        last_key = copy.deepcopy(keys)
        # final_moves.pop(0)
        print final_moves
        return final_moves
    else:
        return None
    # print move_dict


def ordered_move_set(graph, length, n):
    state = copy.deepcopy(graph)
    state_set = []
    move = ()
    for i, cell in enumerate(graph):
        if(cell):
            if(i + 2 < length and graph[i + 1] and not graph[i + 2]):
                state[i + 2] = copy.deepcopy(graph[i])
                state[i] = False
                move = (i, i + 2)
            elif (i - 1 > - 1 and not graph[i - 1]):
                state[i - 1] = copy.deepcopy(graph[i])
                state[i] = False
                move = (i, i -1 )
            elif (i + 1 < length and not graph[i + 1]):
                state[i + 1] = copy.deepcopy(graph[i])
                state[i] = False
                move = (i, i + 1)
            elif (i - 2 > -1 and graph[i - 1] and not graph[i - 2]):
                state[i - 2] = copy.deepcopy(graph[i])
                state[i] = False
                move = (i, i -2 )
            else:
                continue
            state_set += [[move, state]]
            state = copy.deepcopy(graph)
    # print move_set
    return state_set


def is_ordered_solved(graph, length, n):
    decrement = length - 1 - n
    if(not graph[length - 1]):
        return False
    j = 1
    for i in range(length - 1, decrement , -1): 
        if(not graph[i] or graph[i] != j):
                return False
        j+= 1 
    print "solveable"
    return True


def ordered_disk_bfs(to_explore, visited, move_dict,
                     length, n, parent, id_num, state_q):
    state = to_explore.pop(0)
    move_idxs = []
    state_set = ordered_move_set(state, length, n)
    for move, s in state_set:
        if (is_ordered_solved(s, length, n)):
            visited += [move]
            move_idxs += [id_num]
            move_dict[parent] = move_idxs
            to_explore = []
            state_q +=[s]
            return id_num, to_explore, move_dict, visited, True, state_q
        elif s not in visited:
            visited += [move]
            move_idxs += [id_num]
            to_explore += [s]
            state_q += [s]
        id_num += 1
    move_dict[parent] = move_idxs
    return id_num, to_explore, move_dict, visited, False, state_q


def solve_distinct_disks(length, n):
    graph = []
    graph += [False for i in range(length)]
    for i in range(n):
        graph[i] = i+1
    print graph
    to_explore = [graph]
    visited = []
    move_dict = {}
    parent = 0
    id_num = 0
    state_q = []
    solved = False
    while(to_explore):
        (id_num, to_explore, move_dict, visited, solved, state_q) = ordered_disk_bfs(
            to_explore, visited, move_dict, length, n, parent, id_num, state_q)
        parent += 1
    if(solved):
        # print move_dict
        id_nums = []
        # final_moves = []
        last_key = move_dict.keys()[-1]
        last_idx = move_dict[last_key][-1]
        id_nums += [last_idx-1]
        final_moves = [visited[(last_idx)]]
        # print state_q[last_idx -1]
        while(last_key != 0):
            for keys in move_dict: 
                for id_num in move_dict[keys]:
                    if(last_key == id_num):
                        final_moves.insert(0, copy.deepcopy(visited[(id_num -1)]))
                        last_key = copy.deepcopy(keys)
                        id_nums.insert(0,(id_num-1))
                        # print state_q[id_num -1]
        final_moves.pop(0)
        # print move_dict
        # print move_dict[last_key]
        # for x in id_nums: 
        #     print x, state_q[x], visited[x]
        # print
        # for y in id_nums: 
        #     print y+1 , state_q[y+1], visited[y+1]
        # print state_q[2]
        print final_moves
        # print visited
        return final_moves
    else:
        return None

############################################################
# Section 4: Feedback
############################################################

feedback_question_1 = """
12 hours
"""

feedback_question_2 = """
Still having a hard time getting used to python
"""

feedback_question_3 = """
I think this would have been great if it was one problem shorter 
"""


# def main():
#     # print n_queens_valid([1, 3, 0, 2])
#     # n = 5
#     # print n_queens_solutions(n)
#     # p = create_puzzle(4, 3)
#     # p.scramble()
#     # for row in range(2):
#     #     for col in range(3):
#     #         p.perform_move(row, col)
#     # print p.find_solution()
#     # print to_explore
#     # print move_list
#     # p.find_solution()
#     length = 4
#     n = 2
#     # graph = [False, False, 2, 1]
#     # print is_ordered_solved(graph, length, n)
#     # solve_identical_disks(length, n)
#     # solve_distinct_disks(length, n)


# if __name__ == '__main__':
#     main()
