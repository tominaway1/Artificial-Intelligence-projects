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

mid=[
[  1, -1, 1, 1, 1,  1, -1, 1],
[ -1, -1, 1, 1, 1,  1, -1,-1],
[  1,  1, 1, 1, 1,  1,  1, 1],
[  1,  1, 1, 1, 1,  1,  1, 1],
[  1,  1, 1, 1, 1,  1,  1, 1],
[  1,  1, 1, 1, 1,  1,  1, 1],
[ -1, -1, 1, 1, 1,  1, -1,-1],
[  1, -1, 1, 1, 1,  1, -1, 1],
]

class StudentEngine(Engine):
    """ Game engine that implements a simple fitness function maximizing the
    difference in number of pieces in the given color's favor. """
    def __init__(self):
        self.alpha_beta = True
        self.DEPTH = 4
        self.beginning = True
    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        board.display(time)
        if self.alpha_beta:
            answer = self._do_alpha_beta_minimax(board,color)
        else:
            answer = self._do_minimax(board,color)
        print "The best move is {0}".format(answer)
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
        if self.total_board(board) > 30:
            self.beginning = False
        if self.beginning:
            temp = self.beginning_phase(moves,board,color)
            if self.beginning:
                return temp
        arr = []
        arr1 = []
        for move in moves:
            if move in corners:
                return move
            if self.prelim_check(move, board, color):
                arr.append(move)
            if self.total_board(board) < 40:
                if mid[move[0]][move[1]] == 1:
                    arr1.append(move)
        if arr:
            return max(arr, key=lambda move: self._get_ab_cost(board, color, color, 
            move,self.DEPTH,float("-inf"),float("inf")))
        else:
            if not arr1:
                arr1 = moves
            return max(arr1, key=lambda move: self._get_ab_cost(board, color, color, move,self.DEPTH,float("-inf"),float("inf")))
    def prelim_check(self, move, board, color):
        if not self.on_edge(move):
            return False
        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        if self.dominate_edge(newboard,move,color):
            op_move = newboard.get_legal_moves(color*-1)
            for item in corners:
                if item in op_move:
                    return False
            return True
        return False

    def dominate_edge(self, newboard, move, color):
        #find out which edge and determine if there are any adjacent opponent pieces
        flag = True
        #left hand side
        if move[0] == 0:
            for i in range(7):
                if newboard[0][i] == -1 * color:
                    if (newboard[0][i-1] == color) or (newboard[0][i+1] == color):
                        return False
                if newboard[0][i] == 0:
                    if (newboard[0][i-1] == color) and (newboard[0][i+1] == color):
                        return False
            return True

        #right hand side
        if move[0] == 7:
            for i in range(7):
                if newboard[7][i] == -1 * color:
                    if (newboard[7][i-1] == color) or (newboard[7][i+1] == color):
                        return False
                if newboard[7][i] == 0:
                    if (newboard[7][i-1] == color) and (newboard[7][i+1] == color):
                        return False
            return True
        
        #top
        if move[1] == 0:
            for i in range(7):
                if newboard[i][0] == -1 * color:
                    if (newboard[i-1][0] == color) or (newboard[i+1][0] == color):
                        return False
                if newboard[i][0] == 0:
                    if (newboard[i-1][0] == color) and (newboard[i+1][0] == color):
                        return False
            return True


        #bottom
        if move[1] == 7:
            for i in range(7):
                if newboard[i][7] == -1 * color:
                    if (newboard[i-1][7] == color) or (newboard[i+1][7] == color):
                        return False
                if newboard[i][7] == 0:
                    if (newboard[i-1][7] == color) and (newboard[i+1][7] == color):
                        return False
            return True

        #should never reach here
        return False

    def on_edge(self, move):
        edges = [0,7]
        if (move[0] in edges) or (move[1] in edges):
            return True
        else: 
            return False

    def _get_ab_cost(self, board, color, current, move, depth, alpha, beta):
        if move in corners:
            return float("inf")

        newboard = deepcopy(board)
        newboard.execute_move(move, current)

        ###base case###
        if depth == 0 or self.total_board(newboard) == 64:
            return self.calculate_cost(newboard,color,current,move)
        
        ###recursive case###
        moves = newboard.get_legal_moves(current)
        if len(moves) == 0:
            if len(newboard.get_legal_moves(current*-1)) == 0:
                return self.calculate_cost(newboard,color,current,move)
            else: 
                return self._get_ab_cost(newboard, color, current*-1, move, depth, alpha, beta)
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

    def calculate_cost(self,newboard,color,current,move):
        # Return the difference in number of pieces
        num_pieces_op = len(newboard.get_squares(color*-1))
        num_pieces_me = len(newboard.get_squares(color)) 

        if (num_pieces_op == 0):
            return float("inf")

        #return num_pieces_me - num_pieces_op
        count = num_pieces_me - num_pieces_op

        #get total points
        total = 0
        for i in range(0,7):
            for j in range(0,7):
                total += disk_square_table[i][j] * newboard[i][j] * color    
        #print "Move: ({0},{1}) Count:{2} Value:{3} Total:{4}".format(move[0],move[1],count,total,count+total)
        if self.dominate_edge(newboard,move,color):
            total += 100
        return 2 * total + count
    
    def total_board(self, board):
        return len(board.get_squares(-1))+len(board.get_squares(1))    


    #handle beginning of the game
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
