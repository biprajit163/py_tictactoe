import sys
import time
import os
import pygame as pg
from pygame.locals import *


#Initialize global variables
X_O = "x"
x_wins, o_wins = 0, 0
check_winner, check_draw = None, None  
width, height = 600, 400
white = (255, 255, 255)
black = (0, 0, 0)
red = (250, 0, 0)
board = [[None]*3,[None]*3,[None]*3]

# get current working directory
curr_dir = os.getcwd()

# initialize pygame window
pg.init()

# set fps
fps = 30

# track time
CLOCK = pg.time.Clock()

# build game window for display
window = pg.display.set_mode((width, height + 100), 0, 32)

# set color of window
window.fill(white)

# set gametag for game window
pg.display.set_caption("Tic Tac Toe")

# construct file path for images
x_icon_path = os.path.join(curr_dir, "images", "x_icon.png")
o_icon_path = os.path.join(curr_dir, "images", "o_icon.png")

# set images as python objects
x_icon = pg.image.load(x_icon_path)
o_icon = pg.image.load(o_icon_path)

# Set the game initial window
def game_initiating_window():
    global board
    
    # color window white to clear the board
    window.fill(white)
    
    # draw verticle line
    pg.draw.line(window, black, (width/3, 0), (width/3, height), 7)
    pg.draw.line(window, black, (width/3 * 2, 0), (width/3 * 2, height), 7)

    # drawing horizontal lines
    pg.draw.line(window, black, (0, height/3), (width, height/3), 7)
    pg.draw.line(window, black, (0, height/3 * 2), (width, height / 3 * 2), 7)

    # reset board to None values
    board = [[None] * 3 for _ in range(3)]

    update_status()


# provide real-time update on game status and display on window
def update_status():
 
    # getting the global variables
    global check_draw, check_winner, x_wins, o_wins
 
    if check_winner is None:
        message = X_O.upper() + "'s Turn"
    else:
        message = check_winner.upper() + " won !"
        if check_winner == 'x':
            x_wins += 1
        if check_winner == 'o':
            o_wins += 1
    if check_draw:
        message = "Game Draw !"

    font = pg.font.Font(None, 30)

    x_wins_text = font.render(f"X Wins: {x_wins}", 1, red)
    o_wins_text = font.render(f"O Wins: {o_wins}", 1, red)
    text = font.render(message, 1, red)
    
    x_wins_width, _ = x_wins_text.get_size()
    o_wins_width, _ = o_wins_text.get_size()

    text_rect = text.get_rect(center=(width / 2, 500 - 50))
    x_wins_position = (text_rect.centerx - text_rect.width - x_wins_width - 50, 500 - 50)
    o_wins_position = (text_rect.centerx + text_rect.width // 4 + o_wins_width, 500 - 50)

    window.fill(black, (0, 400, width, 100))
    window.blit(text, text_rect)
    window.blit(x_wins_text, x_wins_position)
    window.blit(o_wins_text, o_wins_position)
    pg.display.update()


# check win or draw status and return board coordinates
def check_win():
    global board, check_winner, check_draw, x_wins, o_wins

    # check for draw
    if all(cell is not None for row in board for cell in row):
        check_draw = True
    else:
        check_draw = False

    # draw horrizontal line
    for row in range(3):
        if(all([cell == board[row][0] for cell in board[row]]) 
        and board[row][0] is not None):
            check_winner = board[row][0]
            return (0, row * height // 3 + height // 6, width, row * height // 3 + height // 6)
    
    # Draw vertical line
    for col in range(3):
        if(all([cell == board[0][col] for cell in [board[row][col] for row in range(3)]]) 
        and board[0][col] is not None):
            check_winner = board[0][col]
            return (col * width // 3 + width // 6, 0, col * width // 3 + width // 6, height)
    
    # Draw diagonal line
    if(all([board[i][i] == board[0][0] for i in range(3)]) 
    and board[0][0] is not None):
        check_winner = board[0][0]
        return (0, 0, width, height)
    if (all([board[i][2 - i] == board[0][2] for i in range(3)]) 
        and board[0][2] is not None):
        check_winner = board[0][2]
        return (0, height, width, 0)
    
    return None

# draw X or O on board
def draw_XO(row, col):
    global board, X_O, x_icon, o_icon
    
    if board[row][col] is None:
        # width and height of each cell
        cell_width = width // 3
        cell_height = height // 3

        # resize X and O icon images
        resized_x_icon = pg.transform.scale(x_icon, (cell_width, cell_height))
        resized_o_icon = pg.transform.scale(o_icon, (cell_width, cell_height))

        # calculate x and y position to draw img
        x_pos = (col * cell_width) + ((cell_width - resized_x_icon.get_width()) // 2)
        y_pos = (row * cell_height) + ((cell_height - resized_x_icon.get_height()) // 2)

        # update the board to be x or o
        board[row][col] = X_O

        # post the X_O image
        if X_O == 'x':
            window.blit(resized_x_icon, (x_pos, y_pos))
            X_O = 'o'
        else:
            window.blit(resized_o_icon, (x_pos, y_pos))
            X_O = 'x'

    update_status()
    

# get user input from mouse click
def user_click():
    # get (x, y) coordinate with mouse click
    x, y = pg.mouse.get_pos()
    # print(f"X coordinate {x} && Y coordinate {y}")

    # initialize row and col variables
    row, col = None, None

    # get col with x-coordinate
    if x < width / 3:
        col = 0
    elif x < width / 3 * 2:
        col = 1
    elif x < width:
        col = 2
    else:
        col = None
    
    # get row with y-coordinate
    if y < height / 3:
        row = 0
    elif y < height / 3 * 2:
        row = 1
    elif y < height:
        row = 2
    else:
        row = None
    
    # using row and col draw img at desired location, and check if conditions are met for a winner
    if (row is not None and col is not None and board[row][col] is None):
        draw_XO(row, col)
        check_win()

# function to reset game
def reset_game():
    global board, check_winner, X_O, check_draw
    time.sleep(1)
    X_O = 'x'
    check_draw = False
    game_initiating_window()
    check_winner = None
    board = [[None] * 3 for _ in range(3)]

game_initiating_window()

# Create a running loop to display the window
while True:
    for event in pg.event.get():
        
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            # check if mouse button has been pressed
            if event.button == 1:
                user_click()
                
                win_coords = check_win()
                if check_winner is not None or win_coords is not None:
                    pg.draw.line(window, red, win_coords[0:2], win_coords[2:4], 4)
                    pg.display.update()
                    reset_game()
                elif check_draw: 
                    reset_game() 

    pg.display.update()
    CLOCK.tick(fps)
    

