import numpy as np
import pygame
import sys

# Dimensions du plateau de jeu
ROWS = 6
COLS = 7
CELL_SIZE = 100  # Taille d'une cellule en pixels
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = (ROWS + 1) * CELL_SIZE  # Une rangée supplémentaire pour la zone de sélection

# Couleurs
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)

# Fonction pour créer un plateau de jeu vide
def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

# Fonction pour vérifier si une colonne est valide pour placer un jeton
def is_valid_move(board, col):
    # Vérifie si la colonne est valide (dans les limites du plateau)
    if col < 0 or col >= len(board[0]):
        return False

# Fonction pour placer un jeton dans une colonne
def make_move(board, col, player):
    # Parcours les lignes du bas vers le haut pour trouver la première case vide dans la colonne
    for row in range(len(board) - 1, -1, -1):
        if board[row][col] == 0:
            board[row][col] = player
            return True  # Le coup a été effectué avec succès

    # Si la colonne est pleine, le coup est invalide
    return False

# Fonction pour vérifier si un joueur a gagné
def is_winner(board, player):
    pass


def evaluate(board):
    if is_winner(board, 1):
        return 1000
    elif is_winner(board, -1):
        return -1000
    else:
        return 0

# Fonction pour minimax avec élagage alpha-beta
def minimax(board, depth, alpha, beta, maximizing, player):
    if depth == 0 or is_winner(board, 1) or is_winner(board, -1):
        return evaluate(board), None

    if maximizing:
        max_eval = -np.inf
        best_move = None
        for col in range(COLS):
            if is_valid_move(board, col):
                temp_board = board.copy()
                make_move(temp_board, col, player)
                eval, _ = minimax(temp_board, depth - 1, alpha, beta, False, -player)
                if eval > max_eval:
                    max_eval = eval
                    best_move = col
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval, best_move
    else:
        min_eval = np.inf
        best_move = None
        for col in range(COLS):
            if is_valid_move(board, col):
                temp_board = board.copy()
                make_move(temp_board, col, -player)
                eval, _ = minimax(temp_board, depth - 1, alpha, beta, True, -player)
                if eval < min_eval:
                    min_eval = eval
                    best_move = col
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval, best_move

# Fonction pour initialiser la fenêtre Pygame
def init_pygame():
    pygame.init()
    return pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# Fonction pour dessiner le plateau de jeu
def draw_board(board, screen):
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, WHITE, (col * CELL_SIZE, (row + 1) * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            if board[row][col] == 1:
                pygame.draw.circle(screen, RED, (col * CELL_SIZE + CELL_SIZE // 2, (row + 1) * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif board[row][col] == -1:
                pygame.draw.circle(screen, YELLOW, (col * CELL_SIZE + CELL_SIZE // 2, (row + 1) * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

# Fonction principale du jeu
def main():
    board = create_board()
    pygame_screen = init_pygame()

    player_turn = 1
    AI_PLAYER = -1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(pygame_screen, BLACK, (0, 0, WINDOW_WIDTH, CELL_SIZE))
                posx = event.pos[0]
                pygame.draw.circle(pygame_screen, RED if player_turn == 1 else YELLOW, (posx, CELL_SIZE // 2), CELL_SIZE // 2 - 5)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(pygame_screen, BLACK, (0, 0, WINDOW_WIDTH, CELL_SIZE))
                col = event.pos[0] // CELL_SIZE

                if is_valid_move(board, col):
                    make_move(board, col, player_turn)

                    if is_winner(board, player_turn):
                        print("Le joueur", player_turn, "a gagné !")
                        pygame.quit()
                        sys.exit()

                    player_turn = -player_turn

                    if not any(0 in row for row in board):
                        print("La partie est terminée. C'est un match nul !")
                        pygame.quit()
                        sys.exit()

                    # Tour de l'IA
                    _, ai_move = minimax(board, 4, -np.inf, np.inf, True, AI_PLAYER)
                    make_move(board, ai_move, AI_PLAYER)

                    if is_winner(board, AI_PLAYER):
                        print("L'IA a gagné. Vous avez perdu.")
                        pygame.quit()
                        sys.exit()

            draw_board(board, pygame_screen)
            pygame.display.update()

if __name__ == "__main__":
    main()

