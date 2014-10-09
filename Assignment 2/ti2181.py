from engines import Engine
from copy import deepcopy
game_time=100000
time = { -1 : game_time, 1 : game_time }

class StudentEngine(Engine):
    print "Penis696"
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = False
        self.DEPTH = 4
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        board.display(time)
        if self.alpha_beta:
            answer = self._do_alpha_beta_minimax(board,color)
        else:
            answer = self._do_minimax(board,color)
        print answer
        return answer

    def _do_minimax(self, board, color):
        moves = board.get_legal_moves(color)
        print moves
        return max(moves, key=lambda move: self._get_cost(board, color, color, move,self.DEPTH))

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


    def _do_alpha_beta_minimax(self, board, color):
        moves = board.get_legal_moves(color)
        print moves
        return max(moves, key=lambda move: self._get_ab_cost(board, color, color, 
            move,self.DEPTH,float("-inf"),float("inf")))

    def _get_ab_cost(self, board, color, current, move, depth, alpha, beta):
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        newboard.execute_move(move, current)
        moves = newboard.get_legal_moves(current)
        #base case
        if depth == 0 or len(moves) == 0:
            # Return the difference in number of pieces
            num_pieces_op = len(newboard.get_squares(color*-1))
            num_pieces_me = len(newboard.get_squares(color))
            return num_pieces_me-num_pieces_op
        
        #recursive case
        #maximizing agent
        if color == current:
            for move in moves:
                value = self._get_ab_cost(newboard,color,current*-1,move,depth-1,alpha,beta)
                if value > alpha:
                    alpha = value
                if (beta <= alpha):
                    break
            return alpha
        #minimizing agent
        else:
            for move in moves:
                value = self._get_ab_cost(newboard,color,current*-1,move,depth-1,alpha,beta)
                if value < beta:
                    beta = value
                if (beta <= alpha):
                    break
            return beta
engine = StudentEngine
