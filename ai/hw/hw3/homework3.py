############################################################
# CIS 521: Homework 3
############################################################

student_name = "Gabrielle Merritt"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.

import numpy
import math
import random
import copy
from Queue import PriorityQueue

############################################################
# Section 1: Tile Puzzle
############################################################


def create_tile_puzzle(rows, cols):
    board = [[cols * r + c + 1 for c in range(cols)] for r in range(rows)]
    board[-1][-1] = 0
    return TilePuzzle(board)


class TilePuzzle(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = numpy.size(board, 0)
        self.cols = numpy.size(board, 1)
        self.empty_r = None
        self.empty_c = None
        self.solved_state = self.solved_tile_puzzle()
        for i in range(self.rows):
            for j in range(self.cols):
                if(board[i][j] == 0):
                    self.empty_r = i
                    self.empty_c = j

    def get_board(self):
        return self.board

    def solved_tile_puzzle(self):
        board = [
            [self.cols * r + c + 1 for c in range(self.cols)] for r in range(self.rows)]
        board[-1][-1] = 0
        return board

    def swap_places(self, pos_r1, pos_c1):
        if(pos_r1 < 0 or pos_r1 >= self.rows or pos_c1 < 0 or pos_c1 >= self.cols):
            return False
        # print (pos_r1, pos_c1)
        value = self.board[pos_r1][pos_c1]
        self.board[self.empty_r][self.empty_c] = value
        self.board[pos_r1][pos_c1] = 0
        self.empty_r = pos_r1
        self.empty_c = pos_c1
        return True

    def perform_move(self, direction):
        valid_directions = ["up", "down", "left", "right"]
        if (direction == valid_directions[0]):
            return self.swap_places(self.empty_r - 1, self.empty_c)
        elif direction == valid_directions[1]:
            return self.swap_places(self.empty_r + 1, self.empty_c)
        elif direction == valid_directions[2]:
            return self.swap_places(self.empty_r, self.empty_c - 1)
        elif direction == valid_directions[3]:
            return self.swap_places(self.empty_r, self.empty_c + 1)
        else:
            return False

    def scramble(self, num_moves):
        valid_directions = ["up", "down", "left", "right"]
        for i in range(num_moves):
            move = random.choice(valid_directions)
            self.perform_move(move)

# TODO: if you 0 on bottom right?
    def is_solved(self):
        if(self.solved_state == self.get_board()):
            return True
        return False

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        valid_directions = ["up", "down", "left", "right"]
        valid_children = []
        for move in valid_directions:
            child_board = self.copy()
            # print child_board.empty_r, child_board.empty_c
            if(child_board.perform_move(move)):
                valid_children += [(copy.deepcopy(move),
                                    copy.deepcopy(child_board))]
        # print valid_children
        return valid_children

    # Required
    def puzzle_execute_moves(self, moves):
        puzzle = self.copy()
        for move in moves:
            puzzle.perform_move(move)
        if (puzzle.is_solved()):
            return True
        else:
            return False
    # ASK FOR HELP

    def iddfs_helper(self, p, limit, moves):
        if (p.is_solved()):
            return moves
        if (limit <= 0):
            return []
        ml = []
        for move, puzzle in p.successors():
            ret = self.iddfs_helper(puzzle, limit - 1, moves + [move])
            ml.extend(ret)
        return ml

    def find_solutions_iddfs(self):
        i = 0 
        looping = True
        while looping:
            moves = self.iddfs_helper(self, i, [])
            # if(moves is not None:
            if(moves):
                print i, moves
                looping = False
                yield moves
            i += 1

    # Required
    def calculate_distance(self, board, des_board):
        distance = 0
        for i in range(self.rows * self.cols):
            rc1 = [(r, c) for c in range(self.cols)
                   for r, rows in enumerate(board) if i == rows[c]]
            rc_sol = [(r, c) for c in range(self.cols)
                      for r, rows in enumerate(des_board) if i == rows[c]]
            distance += abs(rc1[0][0] - rc_sol[0][0]) + \
                abs(rc1[0][1] - rc_sol[0][1])
        return distance

    def find_solution_a_star(self):
        visited = []
        parent_nodes = PriorityQueue()
        to_explore = PriorityQueue()
        g_n = 0
        f_n = 0
        path = []
        new_path = []
        to_explore.put((f_n, g_n, path, self.copy()))
        while (not to_explore.empty()):
            current_node = to_explore.get()
            current_p = current_node[3].copy()
            if(current_p.is_solved()):
                return current_node[2]
            visited += [copy.deepcopy(current_p.get_board())]
            for move, puzzle in current_p.successors():
                if(puzzle.get_board() not in visited):
                    new_g = current_node[
                        1] + self.calculate_distance(puzzle.get_board(), current_p.get_board())
                    new_f = new_g + \
                        self.calculate_distance(
                            puzzle.get_board(), self.solved_state)
                    new_path = current_node[2] + [move]
                    to_explore.put((new_f, new_g, new_path, puzzle))
############################################################
# Section 2: Grid Navigation
############################################################


def dist_metric(current, goal):
    dist1 = (current[0] - goal[0])
    dist2 = ((current[1] - goal[1]))
    result = dist1 * dist1 + dist2 * dist2
    return math.sqrt(result)


def get_successors(node, valid_nodes):
    r = node[0]
    c = node[1]
    result = [n for n in valid_nodes if abs(r-n[0])<=1 and abs(c-n[1])<= 1 and node != n]
    return result


def free_nodes(scene):
    result = []
    for r, row in enumerate(scene):
        for c, value in enumerate(row):
            if (not value):
                result += [(r, c)]
    print "done making scene"
    return result


def init_nodes(node_list):
    non_visited = {}
    # [(non_visited[node]) for node in node_list]
    non_visited = dict(zip(node_list, node_list))
    return non_visited


def find_path(start, goal, scene):
    node_list = free_nodes(scene)
    to_explore = PriorityQueue()
    non_visited = init_nodes(node_list)
    visited = set()
    path = [start]
    g_n = 0
    f_n = 0
    i = 0
    to_explore.put((f_n, g_n, path, start))
    while(not to_explore.empty()):
        current_node = to_explore.get()
        if(current_node[-1] == goal):
            print "Visited Nodes:", numpy.size(visited)
            print "Path Length: ", numpy.size(current_node[2])
            return current_node[2]
        # visited[current_node[3]] = current_node[3]
        visited.add(current_node[3])
        non_visited.pop(current_node[3], None)
        for node in get_successors(current_node[-1], non_visited):
            if (node in visited):
                continue
            new_g = current_node[1] + dist_metric(current_node[-1], node)
            new_f = new_g + dist_metric(node, goal)
            to_explore.put((new_f, new_g, current_node[2] + [node], node))
        # print to_explore.qsize()
        # print "V size :",numpy.size(visited.keys())
        # if (i > 20):
        #     print visited
        #     break
        # i+= 1
    return None


############################################################
# Section 3: Linear Disk Movement, Revisited
############################################################
def solved_state(length, n):
    solved = []
    i = 0
    for cell in range(length):
        if(cell >= length - n):
            solved += [n - i]
            i += 1
        else:
            solved += [0]
    return solved


def move_disk(board, p1, p2, length):
    b = copy.deepcopy(board)
    if(p1 >= 0 and p1 < length and p2 >= 0 and p2 < length):
        temp = copy.deepcopy(board[p1])
        b[p1] = b[p2]
        b[p2] = temp
    return b


def valid_move(board, node_idx, direction, length):
    valid_dir_list = ["right", "left", "skip right", "skip left"]
    if(direction == valid_dir_list[0]):
        if(node_idx + 1 < length and not board[node_idx + 1]):
            new_b = move_disk(board, node_idx, node_idx + 1, length)
            return [(node_idx, node_idx + 1), new_b]
    elif (direction == valid_dir_list[1]):
        if (node_idx - 1 >= 0 and not board[node_idx - 1]):
            new_b = move_disk(board, node_idx, node_idx - 1, length)
            return [(node_idx, node_idx - 1), new_b]
    elif direction == valid_dir_list[2]:
        if(node_idx + 2 < length and board[node_idx + 1] and not board[node_idx + 2]):
            new_b = move_disk(board, node_idx, node_idx + 2, length)
            return [(node_idx, node_idx + 2), new_b]
    elif direction == valid_dir_list[3]:
        if(node_idx - 2 >= 0 and board[node_idx - 1] and not board[node_idx - 2]):
            new_b = move_disk(board, node_idx, node_idx - 2, length)
            return [(node_idx, node_idx - 2), new_b]
    return []


def disk_successors(board, length):
    b = copy.deepcopy(board)
    board_list = []
    valid_dir_list = ["right", "left", "skip right", "skip left"]
    for idx, cell in enumerate(board):
        if(cell):
            for direction in (valid_dir_list):
                child_board = valid_move(b, idx, direction, length)
                if(child_board):
                    board_list += [child_board]
    return board_list


def make_board(length, n):
    board = []
    for space in range(length):
        if (space < n):
            board += [(space + 1)]
        else:
            board += [0]
    return board


def disk_dist(goal_board, current_board, length):
    dist = 0
    for pos, num in enumerate(goal_board):
        d1 = [idx for idx, value in enumerate(
            current_board) if value == num and num]
        if(d1):
            dist += abs(d1[0] - pos)
    return dist


def a_star_disks(board, length, n):
    goal = solved_state(length, n)
    to_explore = PriorityQueue()
    visited = []
    g_n = 0
    f_n = 0
    path = []
    to_explore.put((f_n, g_n, path, board))
    while(not to_explore.empty()):
        current_node = to_explore.get()
        if(current_node[3] == goal):
            return current_node[2]
        visited += [copy.deepcopy(current_node[3])]
        for move, brd in disk_successors(current_node[3], length):
            if brd not in visited:
                g_new = current_node[1] + \
                    disk_dist(current_node[3], brd, length)
                f_new = g_new + disk_dist(goal, brd, length)
                to_explore.put((f_new, g_new, current_node[2] + [move], brd))
    return None


def solve_distinct_disks(length, n):
    board = make_board(length, n)
    path = a_star_disks(board, length, n)
    return path


############################################################
# Section 4: Dominoes Game
############################################################


def create_dominoes_game(rows, cols):
    new_b = [[False for c in range(cols)] for r in range(rows)]
    return DominoesGame(new_b)


class DominoesGame(object):

    # Required
    def __init__(self, board):
        self.board = board
        self.rows = numpy.size(board, 0)
        self.cols = numpy.size(board, 1)

    def get_board(self):
        return self.board

    def reset(self):
        self.board = [
            [False for c in range(self.cols)] for r in range(self.rows)]

    def is_legal_move(self, row, col, vertical):
        if(row >= 0 and row < self.rows and col >= 0 and col < self.cols):
            if(vertical):
                if (row + 1 < self.rows and not self.board[row][col] and not self.board[row + 1][col]):
                    return True
                return False
            else:
                if (col + 1 < self.cols and not self.board[row][col] and not self.board[row][col + 1]):
                    return True
                return False
        return False

    def legal_moves(self, vertical):
        for r in range(self.rows):
            for c in range(self.cols):
                if(self.is_legal_move(r, c, vertical)):
                    yield (r, c)

    def perform_move(self, row, col, vertical):
        self.board[row][col] = True
        if(vertical):
            self.board[row + 1][col] = True
        else:
            self.board[row][col + 1] = True

    def game_over(self, vertical):
        if(list(self.legal_moves(vertical))):
            return False
        return True

    def copy(self):
        return copy.deepcopy(self)

    def successors(self, vertical):
        child_list = []
        move_list = list(self.legal_moves(vertical))
        # print move_list
        for move in move_list:
            child_board = self.copy()
            child_board.perform_move(move[0], move[1], vertical)
            child_list += [tuple((move, child_board))]
        return child_list

    def evalution(self, current, opponent, vertical):
        # number of moves available to current minus opponent
        # print list(current.legal_moves(vertical))
        # print list(opponent.legal_moves(not vertical))
        # curr = len(list(current.legal_moves(vertical))) 
        # opp = len(list(opponent.legal_moves(not vertical)))
        # print curr, opp
        # result = curr - opp
        result = len(list(self.legal_moves(vertical))) - len(list(self.legal_moves(not vertical)))
        print result
        return result

    def get_random_move(self, vertical):
        move_list = list(self.legal_moves(vertical))
        rand_move = random.choice(move_list)
        return rand_move
    # Required
    # def mini_max(self, board, vertical, alpha, beta, max_player, limit, d):
    #     m = None
    #     values = PriorityQueue()
    #     print "Alpha Beta:" ,alpha, beta
    #     if (limit == 0 or self.game_over(vertical)):
    #         return (None, self.evalution(self, board, vertical), d)
    #     elif max_player:
    #         print "Max Player"
    #         v = alpha
    #         for move, child_board in board.successors(vertical):
    #             print "Max moves:", move
    #             c_m, child_v, d = self.mini_max(child_board, vertical, v, beta, False, limit - 1, d+1)
    #             # v = max(v, child_v)
    #             values.put((move,child_v))
    #             if(child_v > v):
    #                 v = child_v
    #             if (v >= beta):
    #                 print "Pruning Max"
    #                 break  
    #     else:
    #         v = beta
    #         print "Min Player"
    #         for move, child_board in board.successors(vertical):
    #             c_m, child_v, d = self.mini_max(child_board, vertical, alpha, v, True, limit - 1, d+1)
    #             # v = min(v, child_v)
    #             if(child_v < v):
    #                 v = child_v
    #                 m = move
    #             if (v <= alpha):
    #                 break
    #     return m, v, d

    def max_value(self, min_board, vertical, alpha, beta, limit, d):
        if(limit <= 0):
            return None, self.evalution(self, min_board, vertical), d+1
        elif(self.game_over(vertical)):
            "Game is over Max"
            return None, self.evalution(self, min_board, vertical), d
        v = -float("inf")
        for move, child_board in self.successors(vertical):
            (ml, child_v, d) = child_board.min_value(self.copy(), not vertical, alpha, beta, limit - 1, d)
            if(child_v > v):
                v = copy.deepcopy(child_v)
                m = move
            if (v > beta):
                return move, v, d
            alpha = max(alpha, v)

        return m, v, d

    def min_value(self, max_board, vertical, alpha, beta, limit, d):
        if(limit == 0):
            return None, self.evalution(max_board, self, not vertical),d+1
        if(self.game_over(vertical)):
            print "Game over min"
            return None, self.evalution(max_board, self, not vertical),d
        v = float("inf")
        for move, child_board in self.successors(vertical):
            ml, child_v ,d = child_board.max_value(self.copy(), not vertical, alpha, beta, limit - 1, d)
            if(child_v < v):
                v = copy.deepcopy(child_v)
                m = move
            if (v <  alpha):
                return move, v, d
            beta = min(beta, v)

        return m,v,d 

    def alpha_beta_search(self, vertical, explored, limit):
        move = "Wrong"
        move, v, l  = self.max_value(self,vertical, -float("inf"), +float("inf"), limit, 0)
        # move, v, l = self.mini_max(self.copy(), vertical, -float("inf"), float("inf"), True, limit, 0)
        return (move, v, l)

    def get_best_move(self, vertical, limit):
        print self.get_board()
        return self.alpha_beta_search(vertical,0, limit)

############################################################
# Section 5: Feedback
############################################################

feedback_question_1 = """
20+ hours, I really struggle with implementation
"""

feedback_question_2 = """
Literally just implementation, I've spent forever trying to figure out
why my A* is so slow for grid search 
"""

feedback_question_3 = """
I like graph search, I kind of am sick of reimplementing the same class structure
over and over again. But I'm slowly getting better at python??
"""
