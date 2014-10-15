from engines import Engine
from copy import deepcopy
import time

#set values
timed = { -1 : 0, 1 : 0 }
corners = [(0,0),(0,7),(7,0),(7,7)]

disk_square_table=[
   [ 120, -20, 20, 5, 5, 20, -20,  120],
   [-20, -40,  1, 1, 1,  1, -40, -25],
   [ 10,   1,  5, 2, 2,  5,   1,  20],
   [  5,   1,  2, 1, 1,  2,   1,   5],
   [  5,   1,  2, 1, 1,  2,   1,   5],
   [ 10,   1,  5, 2, 2,  5,   1,  20],
   [-20, -40,  1, 1, 1,  1, -40, -20],
   [ 120, -20, 20, 5, 5, 20, -20,  120],
]

endgame=[
   [ 30, -1000, 10, 5, 5, 10, -1000,  30],
   [-1000, -25,  1, 1, 1,  1, -25, -25],
   [ 10,   1,  5, 2, 2,  5,   1,  10],
   [  5,   1,  2, 1, 1,  2,   1,   5],
   [  5,   1,  2, 1, 1,  2,   1,   5],
   [ 10,   1,  5, 2, 2,  5,   1,  10],
   [-1000, -25,  1, 1, 1,  1, -25, -1000],
   [ 30, -1000, 10, 5, 5, 10, -1000,  30],
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
        self.DEPTH = 4
        self.node = 0
        self.duplicate = {}
        self.branching_factor = 0
        self.times = []
        self.beginning = True

    def get_move(self, board, color, move_num=None,
                 time_remaining=None, time_opponent=None):
        timed[color] = time_remaining
        timed[color * -1] = time_opponent 
        board.display(timed)
        start = time.time()


        # beginning = time_remaining
        if time_remaining < 30:
            self.DEPTH = 4
        if time_remaining < 10:
            self.DEPTH = 3
        if time_remaining < 5:
            self.DEPTH = 2
        if time_remaining < 2:
            self.DEPTH = 0

        if self.alpha_beta:
            answer = self._do_alpha_beta_minimax(board,color)
        else:
            # answer = self._do_minimax(board,color)
            answer = self._do_alpha_beta_minimax1(board,color)

        # print "The best move is {0}".format(answer)
        # print self.node
        # print self.count(self.duplicate)
        # print self.branching_factor
        #print float(self.branching_factor)/float(self.node)
        # print self.times
        self.times.append(time.time()-start)
        return answer

    def _do_minimax(self, board, color):
        moves = board.get_legal_moves(color)
        for move in moves:
            if move in corners:
                return move
        # print moves
        return max(moves, key=lambda move: self._get_cost(board, color, color, move,self.DEPTH))

    def _get_cost(self, board, color, current, move, depth):
        # Create a deepcopy of the board to preserve the state of the actual board
        newboard = deepcopy(board)
        #base case
        if depth == 0 or self.total_board(board) == 64:
            # Return the difference in number of pieces
            num_pieces_op = len(newboard.get_squares(color*-1))
            num_pieces_me = len(newboard.get_squares(color))
            return num_pieces_me - num_pieces_op
        

        #recursive case
        newboard.execute_move(move, current)
        moves = newboard.get_legal_moves(current)
        
        #check to see if you cannot make any more moves
        if len(moves)==0:
            if len(newboard.get_legal_moves(current * -1)) == 0:
            # Return the difference in number of pieces
                num_pieces_op = len(newboard.get_squares(color*-1))
                num_pieces_me = len(newboard.get_squares(color))
                return num_pieces_me - num_pieces_op 
            else:
                return self._get_cost(newboard,color,current*-1,move,depth)

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
        self.branching_factor += len(moves)
        
        #beginning steps
        self.beginning = True
        if self.total_board(board) > 10 or color == -1 or True:
            self.beginning = False
        if self.beginning:
            temp = self.beginning_phase(moves,board,color)
            if self.beginning:
                return temp
                
        arr = []
        arr1 = []
        arr2 = []
        for move in moves:
            if move in corners:
                arr.append(move)
            boolean = self.prelim_check(move, board, color)
            if boolean[0]:
                if boolean[1]:
                    arr.append(move)
                else:
                    arr2.append(move)
            if mid[move[0]][move[1]] == 1:
                arr1.append(move)
        if arr:
            return max(arr, key=lambda move: self._get_ab_cost(True,board, color, color, 
            move,self.DEPTH,float("-inf"),float("inf")))
        elif arr2:
            return max(arr2, key=lambda move: self._get_ab_cost(True,board, color, color, 
            move,self.DEPTH,float("-inf"),float("inf")))
        else:
            if not arr1:
                arr1 = moves
            return max(arr1, key=lambda move: self._get_ab_cost(False,board, color, color, move,self.DEPTH,float("-inf"),float("inf")))
   
    def prelim_check(self, move, board, color):
        if not self.on_edge(move):
            return (False,False)
        newboard = deepcopy(board)
        newboard.execute_move(move, color)
        boolean = self.dominate_edge(board,newboard,move,color)
        if boolean[0]:
            op_move = newboard.get_legal_moves(color*-1)
            for item in corners:
                if item in op_move:
                    return (False,False)
            return (True,boolean[1])
        return (False,False)

    def dominate_edge(self, board, newboard, move, color):
        #find out which edge and determine if there are any adjacent opponent pieces
        danger = [2,6]
        #left hand side
        boolean = True
        take_piece = False
        num = 0
        if move[0] == 0:
            if newboard[0][0] == color and newboard[0][7] == color:
                if move[1] == 1 or move[1] == 6:
                    return (True,True)
            # if move[1] in danger:
            #     count = 0
            #     for i in range(7):
            #         if newboard[0][i] != 0:
            #             count +=1
            #         if count > 1:
            #             return False
            for i in range(7):
                if newboard[0][i] != 0:
                    num += 1
                if newboard[0][i] == -1 * color:
                    boolean = False
                    if (newboard[0][i-1] == color) or (newboard[0][i+1] == color):
                        return (False, boolean)
                if newboard[0][i] == 0:
                    if (newboard[0][i-1] == color) and (newboard[0][i+1] == color):
                        return (False, boolean)
                if newboard[0][i] == color and board[0][i] == -1 * color:
                    take_piece = True 
            if take_piece:
                return (True,True)
            return (True,False)

        #right hand side
        if move[0] == 7:
            if newboard[7][0] == color and newboard[7][7] == color:
                if move[1] == 1 or move[1] == 6:
                    return (True,True)
            for i in range(7):
                if newboard[7][i] != 0:
                    num += 1
                if newboard[7][i] == -1 * color:
                    boolean = False
                    if (newboard[7][i-1] == color) or (newboard[7][i+1] == color):                        
                        if move[1] == i-1 or move[1] == i+1:
                            return (False, boolean)

                if newboard[7][i] == 0:
                    if (newboard[7][i-1] == color) and (newboard[7][i+1] == color):
                        return (False, boolean)
                if newboard[7][i] == color and board[7][i] == -1 * color:
                    take_piece = True
            if take_piece:
                return (True,True)
            return (True,False)
        
        #top
        if move[1] == 0:
            if newboard[0][0] == color and newboard[7][0] == color:
                if move[0] == 1 or move[0] == 6:
                    return (True,True)
            for i in range(7):
                if newboard[i][0] != 0:
                    num += 1
                if newboard[i][0] == -1 * color:
                    boolean = False
                    if (newboard[i-1][0] == color) or (newboard[i+1][0] == color):                       
                        return (False, boolean)
                if newboard[i][0] == 0:
                    if (newboard[i-1][0] == color) and (newboard[i+1][0] == color):
                        return (False, boolean)
                if newboard[i][0] == color and board[i][0] == -1 * color:
                    take_piece = True 
                    # print "Got here"
            if take_piece:
                return (True,True)
            return (True,False)

        #bottom
        if move[1] == 7:
            if newboard[0][7] == color and newboard[7][7] == color:
                if move[0] == 1 or move[0] == 6:
                    return (True,True)
            for i in range(7):
                if newboard[i][7] != 0:
                    num += 1
                if newboard[i][7] == -1 * color:
                    boolean = False
                    if (newboard[i-1][7] == color) or (newboard[i+1][7] == color):
                        return (False, boolean)                 
                if newboard[i][7] == 0:
                    if (newboard[i-1][7] == color) and (newboard[i+1][7] == color):
                        return (False, boolean)
                if newboard[i][7] == color and board[i][7] == -1 * color:
                    take_piece = True 
            if take_piece:
                return (True,True)
            return (True,False)
        #should never reach here
        return False

    def on_edge(self, move):
        edges = [0,7]
        if (move[0] in edges) or (move[1] in edges):
            return True
        else: 
            return False

    def _get_ab_cost(self, e, board, color, current, move, depth, alpha, beta):
        #stats
        self.node += 1
        str_rep = self.stringrep(board) 
        if str_rep in self.duplicate:
            self.duplicate[str_rep] += 1
        else:
            self.duplicate[str_rep] = 0

        if move in corners:
            return float("inf")

        newboard = deepcopy(board)
        newboard.execute_move(move, current)

        ###base case###
        if depth == 0 or self.total_board(newboard) == 64:
            return self.calculate_cost(e,newboard,color,current,move)
        
        ###recursive case###
        moves = newboard.get_legal_moves(current)
        
        #stats
        self.branching_factor += len(moves)

        #check to see if you cannot make any more moves
        if len(moves) == 0:
            if len(newboard.get_legal_moves(current*-1)) == 0:
                return self.calculate_cost(e,newboard,color,current,move)
            else: 
                return self._get_ab_cost(e,newboard, color, current*-1, move, depth, alpha, beta)
        #maximizing agent
        if color == current:
            for move in moves:
                value = self._get_ab_cost(e, newboard,color,current*-1,move,depth-1,alpha,beta)
                if value > alpha:
                    alpha = value
                if (beta <= alpha):
                    break
            return alpha

        #minimizing agent
        else:
            for move in moves:
                value = self._get_ab_cost(e,newboard,color,current*-1,move,depth-1,alpha,beta)
                if value < beta:
                    beta = value
                if (beta <= alpha):
                    break
            return beta

    def calculate_cost(self,e,newboard,color,current,move):
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
                if e:
                    total += endgame[i][j] * newboard[i][j] * color   
                else:
                    total += disk_square_table[i][j] * newboard[i][j] * color    
        #print "Move: ({0},{1}) Count:{2} Value:{3} Total:{4}".format(move[0],move[1],count,total,count+total)
        return total + 2 * count
    
    def total_board(self, board):
        return len(board.get_squares(-1))+len(board.get_squares(1))    

    def check_move(self, board, color):
        moves = board.get_legal_moves(color)
        for move in moves:
            newboard = deepcopy(board)
            newboard.execute_move(move,color)
            if len(newboard.get_squares(color*-1)) == 0:
                return False
        return True
    def count(self,dictionary):
        count = 0
        for item in dictionary:
            if dictionary[item] > 0:
                count += 1
        return count
    #create string representation of dictionary
    def stringrep(self,board):
        ans=''
        for i in range(0,7):
            for j in range(0,7):
                ans += str(board[i][j])
        return ans

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
        # print best
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
            return len(newboard.get_squares(color * -1)) - len(newboard.get_squares(color)) 

engine = StudentEngine
