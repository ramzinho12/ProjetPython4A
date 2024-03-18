import pygame  # Import the pygame library for creating video games
import sys  # Import the sys module for using system-specific functions and variables
import random  # Import the random module to generate random numbers
import math  # Import the math module for mathematical functions

# SQL BLOCK START

import sqlite3  # Import the sqlite3 module to work with SQLite database

# Connect to the database (it will be created if it doesn't exist)
conn = sqlite3.connect('puissance4.db')

# Create a cursor object to interact with the database
cur = conn.cursor()

# Create a table to save the results of the games
cur.execute('''
CREATE TABLE IF NOT EXISTS game_results (
    id INTEGER PRIMARY KEY,
    game_mode TEXT,
    winner TEXT,
    move_count INTEGER,
    loser TEXT
)
''')  # Adding columns game_mode and loser for more detailed tracking of results

# Make sure changes are committed to the database
conn.commit()

# SQL BLOCK END

# Define colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
GRAY = (150, 150, 150)
BUTTON_COLOR = (255, 87, 34)
BUTTON_HOVER_COLOR = (211, 47, 47)
BUTTON_BORDER_COLOR = (33, 150, 243)

# Define constants
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARE_SIZE = 100
RADIUS = int(SQUARE_SIZE / 2 - 5)  # Calculate the radius for the pieces
WIDTH = COLUMN_COUNT * SQUARE_SIZE  # Calculate the width of the game board
HEIGHT = (ROW_COUNT + 1) * SQUARE_SIZE  # Calculate the height of the game board
move_count = 0  # Initialize the move counter

# Function to create the game board
def create_board():
    return [[0] * COLUMN_COUNT for _ in range(ROW_COUNT)]  # Return a 2D list filled with 0s representing an empty board

# Function to check if a move is valid (i.e., the top row of the column is empty)
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Function to find the first empty row in a column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

# Function to drop a piece into the board
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Function to check for a winning move (four in a row horizontally, vertically, or diagonally)
def winning_move(board, piece):
    # Check horizontal locations
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negatively sloped diagonals
    for r in range(ROW_COUNT - 3):
        for c in range(3, COLUMN_COUNT):
            if (
                board[r][c] == piece
                and board[r + 1][c - 1] == piece
                and board[r + 2][c - 2] == piece
                and board[r + 3][c - 3] == piece
            ):
                return True

    return False  # If no winning move found, return False

# Function to draw the game board
def draw_board(screen, board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(
                screen,
                BLUE,
                (c * SQUARE_SIZE, r * SQUARE_SIZE + SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )
            pygame.draw.circle(
                screen,
                BLACK,
                (
                    int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                    int(r * SQUARE_SIZE + SQUARE_SIZE + SQUARE_SIZE / 2),
                ),
                RADIUS,
            )

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(
                    screen,
                    RED,
                    (
                        int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                        HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2),
                    ),
                    RADIUS,
                )
            elif board[r][c] == 2:
                pygame.draw.circle(
                    screen,
                    YELLOW,
                    (
                        int(c * SQUARE_SIZE + SQUARE_SIZE / 2),
                        HEIGHT - int(r * SQUARE_SIZE + SQUARE_SIZE / 2),
                    ),
                    RADIUS,
                )

    pygame.display.update()  # Update the display after drawing

# AI move function
def ai_move(board):
    # Check if AI can win in the next move
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            temp_board = [row[:] for row in board]
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, 2)
            if winning_move(temp_board, 2):
                return col

    # Check if player can win in the next move and block them
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            temp_board = [row[:] for row in board]
            row = get_next_open_row(temp_board, col)
            drop_piece(temp_board, row, col, 1)
            if winning_move(temp_board, 1):
                return col

    # If no immediate win or block, make a random move
    return random.randint(0, COLUMN_COUNT - 1)

# Function for the home screen with a background image
def draw_home_screen(screen):
    background_image = pygame.image.load("C:/Users/ramzi/Downloads/image3.jpeg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)
    start_text = font.render("START GAME", True, RED)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - HEIGHT // 8 - start_text.get_height()))
    pygame.display.update()

# Function for playing against AI
def play_vs_ai():
    global move_count
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puissance 4 - Joueur vs IA")

    board = create_board()
    game_over = False
    turn = 0  # 0 for Red player, 1 for Yellow AI
    move_count = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                draw_board(screen, board)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN and turn == 0:  # Ensure it's the player's turn
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE_SIZE))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, turn + 1)
                    move_count += 1  # Increment the move counter each turn

                    if winning_move(board, turn + 1):
                        winner_name = "Joueur Rouge"
                        loser_name = "IA Jaune"
                        print(f"Félicitations ! {winner_name} a gagné en {move_count} coups.")
                        cur.execute('INSERT INTO game_results (game_mode, winner, move_count, loser) VALUES (?, ?, ?, ?)', 
                                    ("Joueur vs IA", winner_name, move_count, loser_name))
                        conn.commit()
                        draw_winner_screen(screen, turn + 1)
                        game_over = True

                    draw_board(screen, board)
                    if not game_over:
                        turn = 1  # Switch turn to AI

        # AI's turn
        if turn == 1 and not game_over:
            # Add your logic here to determine AI's move, e.g.:
            col = ai_move(board)

            if is_valid_location(board, col):
                pygame.time.wait(100)  # Delay to simulate AI thinking
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)  # AI always plays with piece 2
                move_count += 1

                if winning_move(board, 2):
                    winner_name = "IA Jaune"
                    loser_name = "Joueur Rouge"
                    print(f"Dommage ! {winner_name} a gagné en {move_count} coups.")
                    cur.execute('INSERT INTO game_results (game_mode, winner, move_count, loser) VALUES (?, ?, ?, ?)', 
                                ("Joueur vs IA", winner_name, move_count, loser_name))
                    conn.commit()
                    draw_winner_screen(screen, 2)
                    game_over = True

                draw_board(screen, board)
                turn = 0  # Switch back to player

    pygame.quit()


# Function for player vs player mode
def play_vs_player():
    global move_count
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puissance 4 - Joueur vs Joueur")

    board = create_board()
    game_over = False
    turn = 0  # 0 for Red player, 1 for Yellow player

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, SQUARE_SIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARE_SIZE / 2)), RADIUS)
                else:
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE_SIZE / 2)), RADIUS)

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(posx // SQUARE_SIZE)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, turn + 1)
                    move_count += 1  # Increment the move counter each turn
                    if winning_move(board, turn + 1):
                        winner = f"Joueur {turn + 1}"
                        loser = "Joueur 1" if turn == 1 else "Joueur 2"  # The loser is the other player
                        print(f"Félicitations ! {winner} a gagné en {move_count} coups.")  # Display the move count
                        cur.execute('INSERT INTO game_results (game_mode, winner, move_count, loser) VALUES (?, ?, ?, ?)', 
                                    ("Joueur vs Joueur", winner, move_count, loser))
                        conn.commit()
                        draw_winner_screen(screen, turn + 1)
                        game_over = True

                    turn += 1
                    turn %= 2  # Switch turns between players

        draw_board(screen, board)
        pygame.display.update()


# Function for the end screen
def draw_winner_screen(screen, winner):
    background_image = pygame.image.load("C:/Users/ramzi/Downloads/image5.jpeg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    screen.blit(background_image, (0, 0))
    font = pygame.font.Font(None, 36)

    if winner == 0:
        winner_text = font.render("THE BATTLE WAS LEGENDARY!", True, BLACK)
    elif winner == 1:
        winner_text = font.render(" RED WARRIOR EMERGES VICTORIOUS!", True, RED)
    else:
        winner_text = font.render(" YELLOW WARRIOR EMERGES VICTORIOUS!", True, YELLOW)

    screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 4))
    pygame.display.update()
    pygame.time.wait(2000)
    main()

# Function for the button
def draw_button(screen, rect, color, hover_color, text, text_color, font):
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BUTTON_BORDER_COLOR, rect, 2)

    if rect.collidepoint(pygame.mouse.get_pos()):
        pygame.draw.rect(screen, hover_color, rect)

    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)

# Function for player choice
def get_player_choice():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CHOOSE THE GAME MODE")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)
    small_font = pygame.font.Font(None, 24)

    background_image = pygame.image.load("C:/Users/ramzi/Downloads/image4.jpeg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    button_width = WIDTH // 2 + 100
    button1_rect = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2, button_width, 50)
    button2_rect = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 + 70, button_width, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button1_rect.collidepoint(event.pos):
                    pygame.quit()
                    return "AI"

                elif button2_rect.collidepoint(event.pos):
                    pygame.quit()
                    return "Player"

        screen.blit(background_image, (0, 0))

        draw_button(screen, button1_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, " RED WARRIOR vs Golden AI Synth", BLACK, font)
        draw_button(screen, button2_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, "RED WARRIOR vs YELLOW WARRIOR", BLACK, font)
        title_text = font.render("CHOOSE GAME MODE", True, RED)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)

        info_text = small_font.render("(Click on a mode to start)", True, GRAY)
        info_rect = info_text.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(info_text, info_rect)

        pygame.display.flip()
        clock.tick(60)
        
# Choose AI difficulty      
def get_ai_difficulty():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("CHOOSE AI DIFFICULTY")

    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 36)

    background_image = pygame.image.load("C:/Users/ramzi/Downloads/image4.jpeg")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    button_easy_rect = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 - 30, WIDTH // 2, 50)
    button_medium_rect = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 + 40, WIDTH // 2, 50)
    button_hard_rect = pygame.Rect(WIDTH // 4 - 50, HEIGHT // 2 + 110, WIDTH // 2, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_easy_rect.collidepoint(event.pos):
                    pygame.quit()
                    return "Easy"
                elif button_medium_rect.collidepoint(event.pos):
                    pygame.quit()
                    return "Medium"
                elif button_hard_rect.collidepoint(event.pos):
                    pygame.quit()
                    return "Hard"

        screen.blit(background_image, (0, 0))
        draw_button(screen, button_easy_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, "Easy", BLACK, font)
        draw_button(screen, button_medium_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, "Medium", BLACK, font)
        draw_button(screen, button_hard_rect, BUTTON_COLOR, BUTTON_HOVER_COLOR, "Hard", BLACK, font)

        pygame.display.flip()
        clock.tick(60)

# Main function
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Puissance 4")

    draw_home_screen(screen)
    waiting_for_start = True

    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting_for_start = False

    game_mode = get_player_choice()
    ai_difficulty = None
    if game_mode == "AI":
        ai_difficulty = get_ai_difficulty()
    print("Game mode chosen:", game_mode, ">>  " "AI Difficulty:", ai_difficulty)

    for _ in range(3):  # Play three rounds
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Puissance 4")

        if game_mode == "AI":
            play_vs_ai()
        else:
            play_vs_player()
    # Close the database connection
    cur.close()
    conn.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()  # Execute the main function if this file is run directly
