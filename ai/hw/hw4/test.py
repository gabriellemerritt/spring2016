from homework4 import *
b = read_board("sudoku/hard2.txt")
e = read_board("sudoku/medium1.txt")
# for key in sorted(b):
#     print "%s: %s" % (key,b[key])
sudoku = Sudoku(e)
sudoku2 = Sudoku(b)
# print sorted(sudoku_arcs())
# print ((0,3),(0,0)) in sudoku_arcs()
# print sudoku.remove_inconsistent_values((0,3),(0,0))
# print sudoku.get_values((0,3))
# for col in [0, 1, 4]:
# 	    removed = sudoku.remove_inconsistent_values((0, 3), (0, col))
# 	    print removed, sudoku.get_values((0, 3))
# sudoku.find_neighbors((0,3),(0,0))
# solved,board = sudoku2.infer_with_guessing()
# for key in sorted(board):
# 	print "%s: %s" % (key, board[key])
# solved,board = sudoku.infer_improved()
#  # print sudoku.get_values((0,7))
# # sudoku.check_squares((0,7))
solved, board = sudoku2.infer_with_guessing()
for key in sorted(board):
	print "%s: %s" % (key, board[key])
    # for ch in iter(lambda: f.read(1), ''):