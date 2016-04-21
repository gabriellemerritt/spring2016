from homework3 import *

if __name__ == '__main__':
    # tp = create_tile_puzzle(3, 3)
    # print tp.successors()
    # b = [[1,2,3],[4,5,6],[7,0,8]]
    # b = [[1, 2, 3],
    # 	 [4, 0, 8],
    # 	 [7, 6, 5]]
    # b = [[1, 2, 3], [4, 0, 5], [6, 7, 8]]
    b = [[4,1,2], [0,5,3], [7,8,6]]
    p = TilePuzzle(b)
    # # print list(p.find_solutions_iddfs())
    # # print p.calculate_distance(b)
    print p.find_solution_a_star()
    # scene = [[False, False],
    #          [False, False]]
    # print scene.
    # print find_path((0,0),(1,1), scene) 
    # b = [1,0,2,0]
    print solve_distinct_disks(5,2)
    # b = [[False] * 3 for i in range(3)]
    # g = DominoesGame(b)
    # # g.perform_move(0, 1, True)
    # # print g.get_best_move(False, 1)
    # print g.get_best_move(True, 2)
    # for m, new_g in g.successors(True):
    # 	print m, new_g.get_board()

