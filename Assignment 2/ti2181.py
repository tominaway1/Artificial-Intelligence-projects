from engines import Engine
from copy import deepcopy

#set values
game_time=10000
time = { -1 : game_time, 1 : game_time }
corners = [(0,0),(0,7),(7,0),(7,7)]

disk_square_table=[
   [ 30, -25, 10, 5, 5, 10, -25,  30],
   [-25, -25,  1, 1, 1,  1, -25, -25],
   [ 10,   1,  5, 2, 2,  5,   1,  10],
   [  5,   1,  2, 1, 1,  2,   1,   5],
   [  5,   1,  2, 1, 1,  2,   1,   5],
   [ 10,   1,  5, 2, 2,  5,   1,  10],
   [-25, -25,  1, 1, 1,  1, -25, -25],
   [ 30, -25, 10, 5, 5, 10, -25,  30],
]

beginning=[
   [ 1, -1,-1, -1, -1, -1, -1,  1],
   [ -1, -1,-1, -1, -1, -1, -1,-1],
   [ -1, -1,1, 1, 1, 1, -1, -1],
   [ -1, -1,1, 1, 1, 1, -1, -1],
   [ -1, -1,1, 1, 1, 1, -1, -1],
   [ -1, -1,1, 1, 1, 1, -1, -1],
   [ -1, -1,-1, -1, -1, -1, -1,-1],
   [ 1, -1,-1, -1, -1, -1, -1,  1],
]

class StudentEngine(Engine):
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = False
        self.DEPTH = 3
        self.beginning = True
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
        for move in moves:
            if move in corners:
                return move
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
        if self.total_board(board,color) > 30:
            self.beginning = False
        if self.beginning:
            temp = self.beginning_phase(moves,board,color)
            if self.beginning:
                return temp
        for move in moves:
            if move in corners:
                return move
        return max(moves, key=lambda move: self._get_ab_cost(board, color, color, 
            move,self.DEPTH,float("-inf"),float("inf")))

    def _get_ab_cost(self, board, color, current, move, depth, alpha, beta):
        newboard = deepcopy(board)
        newboard.execute_move(move, current)
        moves = newboard.get_legal_moves(current)
        
        ###base case###
        if depth == 0 or len(moves) == 0:
            return self.calculate_cost(newboard,color,current)
        
        ###recursive case###
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

    def calculate_cost(self,newboard,color,current):
        # Return the difference in number of pieces
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color))    

        return num_pieces_me - num_pieces_op

        # if num_pieces_op == 0:
        #     return float("-inf")
        # count = num_pieces_me - num_pieces_op

        # #get total points
        # total = 0
        # for i in range(0,7):
        #     for j in range(0,7):
        #         total += disk_square_table[i][j] * newboard[i][j]
        # print total+count
        # return total + count
    
    def total_board(self, board,color):
        return len(board.get_squares(color*-1))+len(board.get_squares(color))    

    def beginning_phase(self, moves,board,color):
        arr=[]
        for move in moves:
            if move in corners:
                return move
            if beginning[move[0]][move[1]] == 1:
                arr.append(move)
        best = float("-inf")
        best_move = None
        for item in arr:
            newboard = deepcopy(board)
            newboard.execute_move(item, color)
            temp = self.get_begin_cost(item,newboard,color)
            if temp > best:
                best = temp
                best_move = item

        print best
        if not best_move:
            self.beginning = False
        else:
            return best_move

    def get_begin_cost(self, move,board,color):
        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        #check if opponent can win next turn
        if not self.check_move(newboard,color*-1):
            return float("-inf")
        else:
            return len(newboard.get_squares(color*-1)) - len(newboard.get_squares(color)) 
    def check_move(self, board, color):
        moves = board.get_legal_moves(color)
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            if len(newboard.get_squares(color*-1)) == 0:
                return False
        return True



engine = StudentEngine
