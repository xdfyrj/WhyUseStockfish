import chess

class ChessAI:
    def __init__(self):
        self.position_count = 0

        # Piece-Square Tables from Chess Programming Wiki
        self.pawnEvalWhite = [
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0],
            [5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0, 5.0],
            [1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0, 1.0],
            [0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5, 0.5],
            [0.0,  0.0,  0.0,  2.0,  2.0,  0.0,  0.0, 0.0],
            [0.5, -0.5, -1.0,  0.0,  0.0, -1.0, -0.5, 0.5],
            [0.5,  1.0,  1.0, -2.0, -2.0,  1.0,  1.0, 0.5],
            [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, 0.0]
        ]
        self.pawnEvalBlack = self.pawnEvalWhite[::-1]

        self.knightEval = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
            [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
            [-3.0,  0.5,  1.5,  2.0,  2.0,  1.5,  0.5, -3.0],
            [-3.0,  0.0,  1.5,  2.0,  2.0,  1.5,  0.0, -3.0],
            [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
            [-4.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ]

        self.bishopEvalWhite = [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
            [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
            [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
            [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
            [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ]
        self.bishopEvalBlack = self.bishopEvalWhite[::-1]

        self.rookEvalWhite = [
            [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,  0.0],
            [ 0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0,  0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [ 0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0,  0.0]
        ]
        self.rookEvalBlack = self.rookEvalWhite[::-1]

        self.queenEval = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [-1.0,  0.5,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]

        self.kingEvalWhite = [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
            [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
        ]
        self.kingEvalBlack = self.kingEvalWhite[::-1]

    def evaluate_board(self, board):
        total_evaluation = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                x = chess.square_file(square)
                y = chess.square_rank(square)
                total_evaluation += self.get_piece_value(piece, x, y)
        return total_evaluation

    def get_piece_value(self, piece, x, y):
        if piece is None:
            return 0
        is_white = piece.color == chess.WHITE
        if not is_white:
            y = 7 - y  # Flip the rank for black pieces

        if piece.piece_type == chess.PAWN:
            value = 10 + (self.pawnEvalWhite[y][x] if is_white else self.pawnEvalBlack[y][x])
        elif piece.piece_type == chess.ROOK:
            value = 50 + (self.rookEvalWhite[y][x] if is_white else self.rookEvalBlack[y][x])
        elif piece.piece_type == chess.KNIGHT:
            value = 30 + self.knightEval[y][x]
        elif piece.piece_type == chess.BISHOP:
            value = 30 + (self.bishopEvalWhite[y][x] if is_white else self.bishopEvalBlack[y][x])
        elif piece.piece_type == chess.QUEEN:
            value = 90 + self.queenEval[y][x]
        elif piece.piece_type == chess.KING:
            value = 900 + (self.kingEvalWhite[y][x] if is_white else self.kingEvalBlack[y][x])
        else:
            raise Exception(f"Unknown piece type: {piece.piece_type}")
        return value if is_white else -value

    def minimax(self, board, depth, alpha, beta, is_maximizing_player):
        self.position_count += 1
        if depth == 0 or board.is_game_over():
            return self.evaluate_board(board)

        legal_moves = list(board.legal_moves)
        if is_maximizing_player:
            max_eval = -float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, False)
                board.pop()
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, alpha, beta, True)
                board.pop()
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def choose_move(self, board, depth):
        self.position_count = 0
        legal_moves = list(board.legal_moves)
        best_move = None
        if board.turn == chess.WHITE:
            max_eval = -float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, -float('inf'), float('inf'), False)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
        else:
            min_eval = float('inf')
            for move in legal_moves:
                board.push(move)
                eval = self.minimax(board, depth - 1, -float('inf'), float('inf'), True)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
        return best_move
