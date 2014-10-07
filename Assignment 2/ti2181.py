from engines import Engine
from copy import deepcopy

class StudentEngine(Engine):
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = False
        self.DEPTH = 3
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        answer = self._do_minimax(board,color)
        return answer

    def _get_cost(self, board, color, current, move ,depth):
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, current)
        
        moves = newboard.get_legal_moves(current)
        #base case
        if depth == 0 or len(moves)==0:
            # Return the difference in number of pieces
            num_pieces_op = len(newboard.get_squares(color*-1))
            num_pieces_me = len(newboard.get_squares(color))
            return num_pieces_me - num_pieces_op
        
        #recursive case
        best_solution = []

        #maximizing agent
        if color == current:
            for move in moves:
                best_solution.append(self._get_cost(newboard,color,current*-1,move,depth-1))
            return max(best_solution)
        #minimizing agent
        else:
            for move in moves:
                best_solution.append(self._get_cost(newboard,color,current*-1,move,depth-1))
            return min(best_solution)


    def _do_minimax(self, board, color):
        moves = board.get_legal_moves(color)
        print moves
        return max(moves, key=lambda move: self._get_cost(board, color, color*-1, move,self.DEPTH))

engine = StudentEngine
