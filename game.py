import pygame
import chess
from WhyUseStockfish import ChessAI

class ChessGame:
    def __init__(self):
        pygame.init()
        self.WIDTH, self.HEIGHT = 640, 640
        self.SQUARE_SIZE = self.WIDTH // 8
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.HIGHLIGHT_COLOR = (88, 88, 88, 128)

        self.board_image = pygame.image.load('./res/board.png')
        self.board_image = pygame.transform.scale(self.board_image, (self.WIDTH, self.HEIGHT))
        self.pieces_images = {f"{color}{piece}": pygame.image.load(f"./res/{color}_{piece}.png")
                              for color in ['w', 'b'] for piece in ['p', 'r', 'n', 'b', 'q', 'k']}
        
        self.board = chess.Board()
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('ChessAI')

        self.ai = ChessAI()
        self.player_color = chess.WHITE

        global depth, flag
        depth = {
            "easy": 2, 
            "medium": 3, 
            "hard": 4,
        }


    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                img = self.pieces_images[f"{piece.color and 'w' or 'b'}{piece.symbol().lower()}"]
                rank, file = divmod(square, 8)
                rect = img.get_rect(center=(file * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                                            (7 - rank) * self.SQUARE_SIZE + self.SQUARE_SIZE // 2))
                self.screen.blit(img, rect)

    def highlight_moves(self, square):
        for move in self.board.legal_moves:
            if move.from_square == square:
                row = 7 - chess.square_rank(move.to_square)
                col = chess.square_file(move.to_square)
                self.highlight_circle(col, row)

    def highlight_circle(self, col, row):
        center = (col * self.SQUARE_SIZE + self.SQUARE_SIZE // 2,
                  row * self.SQUARE_SIZE + self.SQUARE_SIZE // 2)
        pygame.draw.circle(self.screen, self.HIGHLIGHT_COLOR, center, self.SQUARE_SIZE // 6)

    def check_game_over(self):
        if self.board.is_checkmate():
            print("Black wins!" if self.board.turn == chess.WHITE else "White wins!")
            pygame.quit()
            exit()
        elif self.board.is_stalemate() or self.board.is_insufficient_material():
            print("Draw!")
            pygame.quit()
            exit()

    def handle_promotion(self, move):
        waiting_for_promotion = True
        promotion_piece = None

        print("Press Q for Queen, R for Rook, B for Bishop, N for Knight for promotion.")

        while waiting_for_promotion:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        promotion_piece = chess.QUEEN
                    elif event.key == pygame.K_r:
                        promotion_piece = chess.ROOK
                    elif event.key == pygame.K_b:
                        promotion_piece = chess.BISHOP
                    elif event.key == pygame.K_n:
                        promotion_piece = chess.KNIGHT

                    if promotion_piece:
                        move.promotion = promotion_piece
                        waiting_for_promotion = False

            self.screen.blit(self.board_image, (0, 0))
            self.draw_pieces()
            pygame.display.flip()

        self.board.push(move)
        self.check_game_over()

    def run(self, mode):
        selected = None
        running = True

        while running:
            if self.board.turn == self.player_color:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        x, y = pygame.mouse.get_pos()
                        col, row = x // self.SQUARE_SIZE, 7 - (y // self.SQUARE_SIZE)
                        square = chess.square(col, row)

                        if selected is None:
                            if self.board.piece_at(square) and self.board.piece_at(square).color == self.board.turn:
                                selected = square
                        else:
                            promotion_moves = [m for m in self.board.legal_moves if m.from_square == selected and m.to_square == square]
                            if promotion_moves:
                                if any(m.promotion for m in promotion_moves):
                                    move = chess.Move(selected, square)
                                    self.handle_promotion(move)
                                    print(move)
                                else:
                                    move = promotion_moves[0]
                                    self.board.push(move)
                                    print(move)
                                    self.check_game_over()
                                selected = None
                            else:
                                selected = None
            else:
                pygame.event.pump()
                ai_move = self.ai.choose_move(self.board, depth[mode])
                if ai_move is not None:
                    self.board.push(ai_move)
                    print(ai_move)
                    self.check_game_over()

            self.screen.blit(self.board_image, (0, 0))
            self.draw_pieces()
            if selected is not None:
                self.highlight_moves(selected)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    mode = "medium"  # Select Mode. # easy or medium or hard
    ChessGame().run(mode)
