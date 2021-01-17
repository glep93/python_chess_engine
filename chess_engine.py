import chess
import chess.polyglot
import time
import numpy as np

def default_evaluate_board(board):

    if board.is_checkmate():
        if board.turn:
            return -np.inf
        else:
            return np.inf
    if board.is_stalemate():
        return 0
    if board.is_insufficient_material():
        return 0
    if board.is_fivefold_repetition():
        return 0
    if board.is_repetition(3):
        return 0

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    material = 100*(wp-bp)+320*(wn-bn)+330*(wb-bb)+500*(wr-br)+900*(wq-bq)

    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq= pawnsq + sum([-pawntable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq= sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq= bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                                    for i in board.pieces(chess.KING, chess.BLACK)])

    eval = material + pawnsq + knightsq + bishopsq+ rooksq+ queensq + kingsq


    if board.turn:
        return eval
    else:
        return eval

pawntable = [
 0,  0,  0,  0,  0,  0,  0,  0,
 5, 10, 10,-20,-20, 10, 10,  5,
 5, -5,-10,  0,  0,-10, -5,  5,
 0,  0,  0, 20, 20,  0,  0,  0,
 5,  5, 10, 25, 25, 10,  5,  5,
10, 10, 20, 30, 30, 20, 10, 10,
50, 50, 50, 50, 50, 50, 50, 50,
 0,  0,  0,  0,  0,  0,  0,  0]

knightstable = [
-50,-40,-30,-30,-30,-30,-40,-50,
-40,-20,  0,  5,  5,  0,-20,-40,
-30,  5, 10, 15, 15, 10,  5,-30,
-30,  0, 15, 20, 20, 15,  0,-30,
-30,  5, 15, 20, 20, 15,  5,-30,
-30,  0, 10, 15, 15, 10,  0,-30,
-40,-20,  0,  0,  0,  0,-20,-40,
-50,-40,-30,-30,-30,-30,-40,-50]

bishopstable = [
-20,-10,-10,-10,-10,-10,-10,-20,
-10,  5,  0,  0,  0,  0,  5,-10,
-10, 10, 10, 10, 10, 10, 10,-10,
-10,  0, 10, 10, 10, 10,  0,-10,
-10,  5,  5, 10, 10,  5,  5,-10,
-10,  0,  5, 10, 10,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10,-10,-10,-10,-10,-20]

rookstable = [
  0,  0,  0,  5,  5,  0,  0,  0,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
 -5,  0,  0,  0,  0,  0,  0, -5,
  5, 10, 10, 10, 10, 10, 10,  5,
 0,  0,  0,  0,  0,  0,  0,  0]

queenstable = [
-20,-10,-10, -5, -5,-10,-10,-20,
-10,  0,  0,  0,  0,  0,  0,-10,
-10,  5,  5,  5,  5,  5,  0,-10,
  0,  0,  5,  5,  5,  5,  0, -5,
 -5,  0,  5,  5,  5,  5,  0, -5,
-10,  0,  5,  5,  5,  5,  0,-10,
-10,  0,  0,  0,  0,  0,  0,-10,
-20,-10,-10, -5, -5,-10,-10,-20]

kingstable = [
 20, 30, 10,  0,  0, 10, 30, 20,
 20, 20,  0,  0,  0,  0, 20, 20,
-10,-20,-20,-20,-20,-20,-20,-10,
-20,-30,-30,-40,-40,-30,-30,-20,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30,
-30,-40,-40,-50,-50,-40,-40,-30]



class chess_engine():
    def __init__(self):
        self.board =  chess.Board()
        self.eval = default_evaluate_board
        self.hist = {}
        self.book = chess.polyglot.MemoryMappedReader("bookfish.bin")

    def get_eval(self):
        return self.eval (self.board)

    def minmax(self, depth):
        if depth ==0 or self.board.is_game_over():
            return self.get_eval(), chess.Move.null()

        maxval = -np.inf
        beast_move = chess.Move.null()
        for move in self.board.legal_moves:
            self.board.push(move)
            val = -self.minmax(depth-1)[0]
            self.board.pop()
            if val > maxval:
                maxval = val
                beast_move = move
        return maxval, beast_move


    def alphabeta(self,alpha = -np.inf, beta = +np.inf, depth = 4):
        if depth ==0 or self.board.is_game_over():
            return self.get_eval(), chess.Move.null()

        if alpha >= beta:
            beast_move = self.board.move_stack[-1]
            return alpha, beast_move

        beast_move = chess.Move.null()
        maxval = -np.inf

        for move in self.board.legal_moves :
            self.board.push(move)
            val = -self.alphabeta(  -beta, -alpha, depth -1)[0]
            self.board.pop()

            if val > maxval:
                maxval = val
                beast_move = move

            alpha = max( alpha , maxval)

            if alpha >= beta:
                return maxval, beast_move
        return maxval, beast_move


    def MT(self,gamma, depth, root = True):

        lower, upper, move, hist_depth = self.hist.get(self.board.fen(),(-np.inf, np.inf,chess.Move.null(), 0) )

        if hist_depth >= depth:
            if lower > gamma:
                return lower, move
            if upper < gamma:
                return upper,move

        if depth ==0 or self.board.is_game_over():
            g = self.get_eval()

            upper = g
            lower = g

            if root == False:
                self.hist[self.board.fen()]  = lower, upper, move ,depth
            return g, move

        else:
            g = -np.inf
            for i in self.board.legal_moves:
                self.board.push(i)
                next_val = -self.MT(-gamma, depth -1)[0]
                self.board.pop()

                if next_val > g:
                    g = next_val
                    move = i

                if g> gamma:
                    break

            if g < gamma:
                upper = g
            else:
                lower = g
            if root == False:
                self.hist[self.board.fen()] = lower, upper, move ,depth
            return g,move


    def MTD_bi(self,depth):
        g = np.inf
        bound = 0
        lower, upper = -np.inf, np.inf
        while lower < upper:
            g,move = self.MT(bound, depth)
            if g >= bound:
                lower = g
            if g < bound:
                upper = g
            bound =  (lower+upper)/2 #-1
        return g, move


    def MTD_inf(self,depth):
        g = +10000 #np.inf
        bound = 'start'
        while g != bound:
            bound = g
            g,move = self.MT(bound, depth)
            #print(g, bound)
        return g, move


    def book_move(self):
        try:
            return self.book.weighted_choice(self.board).move.uci()
        except:
            return 'Not Found'
