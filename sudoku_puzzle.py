import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 450, 450
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
CONFETTI_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]


# Function to draw the Sudoku grid
def draw_grid(board, screen):
    for i in range(GRID_SIZE + 1):
        line_thickness = 2 if i % 3 == 0 else 1
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), line_thickness)
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), line_thickness)

    font = pygame.font.Font(None, 36)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            if value != 0:
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=((j * CELL_SIZE) + CELL_SIZE // 2, (i * CELL_SIZE) + CELL_SIZE // 2))
                screen.blit(text, text_rect)


# Function to highlight the selected cell
def draw_selection(screen, row, col):
    pygame.draw.rect(screen, BLUE, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 3)


# Function to check if the board is solved
def is_board_solved(board):
    for row in board:
        if 0 in row:
            return False
    return True


def draw_confetti(screen, confetti_particles):
    for particle in confetti_particles:
        pygame.draw.circle(screen, particle[2], (particle[0], particle[1]), 3)


# Function to generate a new puzzle
def generate_puzzle():
    board = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    solve_sudoku(board)

    # Remove some numbers to create the puzzle
    for _ in range(random.randint(12, 30)):
        row, col = random.randint(0, 8), random.randint(0, 8)
        board[row][col] = 0

    return board


# Function to solve Sudoku
def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  # Puzzle solved

    row, col = empty_cell
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve_sudoku(board):
                return True  # Continue solving

            board[row][col] = 0  # Backtrack if the solution is not valid

    return False  # No solution found


# Function to find an empty cell
def find_empty_cell(board):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if board[i][j] == 0:
                return i, j
    return None  # No empty cell found


# Function to check if a number is valid in a cell
def is_valid(board, row, col, num):
    # Check if the number is not in the same row or column
    for i in range(GRID_SIZE):
        if board[row][i] == num or board[i][col] == num:
            return False

    # Check if the number is not in the same 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True


# Main function
def main():
    # Initialize the screen
    selected_cell = None  # declaring selected_cell as global variable
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku Puzzle")

    # Generate a new Sudoku puzzle
    sudoku_board = generate_puzzle()
    confetti_particles = []

    # Game loop
    running = True
    solved = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                selected_cell = (mouse_pos[1] // CELL_SIZE, mouse_pos[0] // CELL_SIZE)
            elif event.type == pygame.KEYDOWN:
                if selected_cell and sudoku_board[selected_cell[0]][selected_cell[1]] == 0:
                    if event.unicode.isdigit() and 1 <= int(event.unicode) <= 9:
                        sudoku_board[selected_cell[0]][selected_cell[1]] = int(event.unicode)

        # Draw the Sudoku grid
        screen.fill(WHITE)

        if not solved:
            draw_grid(sudoku_board, screen)
            if selected_cell:
                draw_selection(screen, selected_cell[0], selected_cell[1])
        else:
            draw_confetti(screen, confetti_particles)

        if is_board_solved(sudoku_board) and not solved:
            # Generate confetti particles
            for _ in range(100):
                x = random.randint(0, WIDTH)
                y = random.randint(0, HEIGHT)
                color = random.choice(CONFETTI_COLORS)
                confetti_particles.append((x, y, color))
            solved = True

        # Update the display
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
