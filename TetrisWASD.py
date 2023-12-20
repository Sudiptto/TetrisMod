import random, pygame
from pygame.locals import *

#CANT FIGURE OUT TEAM MODE
"""
10 x 20 grid
play_height = 2 * play_width

tetriminos:
    0 - S - green
    1 - Z - red
    2 - I - cyan
    3 - O - yellow
    4 - J - blue
    5 - L - orange
    6 - T - purple
"""

pygame.font.init()
#Line 615, 203 - 209, 265
# MUSIC FROM: https://pixabay.com/music/search/brazil/
# NOTE FOR TEAM ADDING MUSIC! (BATTLE THEME ) REFER TO GITHUB COMMIT FOR MORE INFORMATION
# Starting the mixer 
pygame.mixer.init()
  
# Loading the song 
pygame.mixer.music.load("brazilmusic.mp3") 
pygame.mixer.music.play(loops=-1) # keep the loop going 
# Setting the volume  
pygame.mixer.music.set_volume(0.7) 

# Start playing the song 
#mixer.music.play() 

# SOUND FROM HERE: https://pixabay.com/sound-effects/search/cheers/ (yay by Pixabay)
yay_sound = pygame.mixer.Sound("yay.mp3")
yay_sound.set_volume(0.5)

# global variables
col = 10  # 10 columns
row = 20  # 20 rows
col_2 = 10
row_2 = 20
s_width = 1500  # window width                                           < NOTE to Group: Create variable that changes depending on gamemode(Teammode, difficulty ect)
s_height = 850  # window height                                         <
play_width = 300  # play window width; 300/10 = 30 width per block      <
play_height = 600  # play window height; 600/20 = 20 height per block   <
block_size = 30  # size of block

top_left_x = (s_width - play_width) // 4 #Splits main screen to create tetris display - Normally its devided by 2
top_left_y = s_height - play_height - 50 # ^^^

top_left_x_2 = (s_width - play_width) - 300 #Splits main screen to create tetris display - Normally its devided by 2
top_left_y_2 = s_height - play_height - 50

filepath = './highscore.txt'
fontpath = './arcade.ttf'
fontpath_mario = './mario.ttf'

# shapes formats
# NOTE to Group we can add different shapes but ensure to add them to shapes and shape_color
S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['.....',
      '..0..',
      '..0..',
      '..0..',
      '..0..'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

# index represents the shape
shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)] #We can add a function that changes these colors to fit a certain theme depending on the level


# class to represent each of the pieces


class Piece(object):
    def __init__(self, x, y, shape):
        if piece_num == 1:
            self.x = x
            self.y = y
            self.shape = shape
            self.color = shape_colors[shapes.index(shape)]  # choose color from the shape_color list
            self.rotation = 0  # chooses the rotation according to index
        elif piece_num == 2:
            self.x_2 = x
            self.y_2 = y
            self.shape = shape
            self.color = shape_colors[shapes.index(shape)]  # choose color from the shape_color list
            self.rotation = 0  # chooses the rotation according to index


# initialise the grid
def create_grid(locked_pos={},locked_pos_2={}):
    grid = {}
    grid_2 = {}
    if locked_pos_2 == 0:
        grid = [[(0, 0, 0) for x in range(col)] for y in range(row)]  # grid represented rgb tuples
        #       ^^NOTE FOR GROUP TO CHANGE COLOR Have same value as on line 259, still not sure what else to change
        # locked_positions dictionary
        # (x,y):(r,g,b)
        for y in range(row):
            for x in range(col):
                if (x, y) in locked_pos:
                    color = locked_pos[
                        (x, y)]  # get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                    grid[y][x] = color  # set grid position to color
    elif locked_pos == 0:
        grid_2 = [[(0, 0, 0) for x_2 in range(col_2+10,40)] for y_2 in range(row_2)]  # grid represented rgb tuples
        for y_2 in range(row_2):
            for x_2 in range(col_2+10,40):
                if (x_2, y_2) in locked_pos_2:
                    color = locked_pos_2[
                        (x_2, y_2)]  # get the value color (r,g,b) from the locked_positions dictionary using key (x,y)
                    grid_2[y_2][x_2-20] = color  # set grid position to color
        print(grid_2)
    return (grid, grid_2)

def convert_shape_format(piece, place):
    positions = []
    positions_2 = []

    '''
    e.g.
       ['.....',
        '.....',
        '..00.',
        '.00..',
        '.....']
    '''
    if place == 1:
        shape_format = piece.shape[piece.rotation % len(piece.shape)] 
        for i, line in enumerate(shape_format):  # i gives index; line gives string
            row = list(line)  # makes a list of char from string
            for j, column in enumerate(row):  # j gives index of char; column gives char
                if column == '0':
                    positions.append((piece.x + j, piece.y + i))
        for i, pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)  # offset according to the input given with dot and zero
        return positions
    
    elif place == 2:
        shape_format_2 = piece.shape[piece.rotation % len(piece.shape)]
        for i, line in enumerate(shape_format_2):  # i gives index; line gives string
            row_2 = list(line)  # makes a list of chart from string
            for j, column in enumerate(row_2):  # j gives index of chart; column gives chart
                if column == '0':
                    positions_2.append((piece.x_2 + j, piece.y_2 + i))

        for i, pos2 in enumerate(positions_2):
            positions_2[i] = (pos2[0] - 4, pos2[1] - 4)  # offset according to the input given with dot and zero, CHANGE pos[0] FOR X AXIS PIECE
            
        return positions_2

# checks if current position of piece in grid is valid
def valid_space(piece, grid, player):
    if player == 1:
        # makes a 2D list of all the possible (x,y)
        accepted_pos = [[(x, y) for x in range(col) if grid[y][x] == (0, 0, 0)] for y in range(row)]
        # removes sub lists and puts (x,y) in one list; easier to search
        accepted_pos = [x for item in accepted_pos for x in item]
        formatted_shape = convert_shape_format(piece, 1)
        for pos in formatted_shape:
            if pos not in accepted_pos:
                if pos[1] >= 0:
                    return False
        return True
    elif player == 2:
        accepted_pos_2 = [[(x_2 + 20, y_2) for x_2 in range(20) if grid[y_2][x_2] == (0, 0, 0)] for y_2 in range(row_2)]
        accepted_pos_2 = [x_2 for item_2 in accepted_pos_2 for x_2 in item_2]
        formatted_shape_2 = convert_shape_format(piece, 2)
        for pos_2 in formatted_shape_2:
            if pos_2 not in accepted_pos_2:
                if pos_2[1] >= 0:
                     return False
        return True

# check if piece is out of board
def check_lost(positions, num1):
    if num1 == 1:
        for pos in positions:
            x, y = pos
            if y < 1:
                return True
        return False
    if num1 == 2:
        for pos_2 in positions:
            x_2, y_2 = pos_2
            if y_2 < 1:
                return True
        return False

# chooses a shape randomly from shapes list, changes the x and y of where the shape appears
def get_shape(grid):
    global piece_num
    piece_num = grid
    if piece_num == 1:
        return Piece(4, 0, random.choice(shapes))
    elif piece_num == 2:
        return Piece(30, 0, random.choice(shapes))

# draws text in the middle
def draw_text_middle(text, size, color, surface):
    font = pygame.font.Font(fontpath, size)
    font.set_bold(False)
    font.set_italic(True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


# draws the lines of the grid for the game
def draw_grid(surface):
    r = g = b = 0
    grid_color = (r, g, b)

    for i in range(row):
        # draw grey horizontal lines
        pygame.draw.line(surface, grid_color, (top_left_x, top_left_y + i * block_size),
                         (top_left_x + play_width, top_left_y + i * block_size))
        pygame.draw.line(surface, grid_color, (top_left_x_2, top_left_y_2 + i * block_size),
                         (top_left_x_2 + play_width, top_left_y_2 + i * block_size))
        for j in range(col):
            # draw grey vertical lines
            pygame.draw.line(surface, grid_color, (top_left_x + j * block_size, top_left_y),
                             (top_left_x + j * block_size, top_left_y + play_height))
            pygame.draw.line(surface, grid_color, (top_left_x_2 + j * block_size, top_left_y_2),
                (top_left_x_2 + j * block_size, top_left_y_2 + play_height))


# clear a row when it is filled
def clear_rows(grid, locked, num):
    # need to check if row is clear then shift every other row above down one
    increment = 0
    if num == 1:
        for i in range(len(grid) - 1, -1, -1):      # start checking the grid backwards
            grid_row = grid[i]                      # get the last row
            if (0, 0, 0) not in grid_row:           # if there are no empty spaces (i.e. black blocks)
                increment += 1
                # add positions to remove from locked
                index = i                           # row index will be constant
                for j in range(len(grid_row)):
                    try:
                        del locked[(j, i)]          # delete every locked element in the bottom row
                    except ValueError:
                        continue
    # shift every row one step down, delete filled bottom row, add another empty row on the top, move down one step
        if increment > 0:
            pygame.mixer.Channel(1).play(yay_sound) # NOTE PLAY THE SOUND HERE
            # sort the locked list according to y value in (x,y) and then reverse
            # reversed because otherwise the ones on the top will overwrite the lower ones
            for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
                x, y = key
                if y < index:                       # if the y value is above the removed index
                    new_key = (x, y + increment)    # shift position to down
                    locked[new_key] = locked.pop(key)
        return increment
    elif num == 2:
        for i in range(len(grid) - 1, -1, -1):      # start checking the grid backwards
            grid_row = grid[i]                      # get the last row
            if (0, 0, 0) not in grid_row:           # if there are no empty spaces (i.e. black blocks)
                increment += 1
                # add positions to remove from locked
                index = i                           # row index will be constant
                for j in range(len(grid_row)):
                    try:
                        del locked[(j, i)]          # delete every locked element in the bottom row
                    except ValueError:
                        continue
        if increment > 0:
            pygame.mixer.Channel(1).play(yay_sound) # NOTE PLAY THE SOUND HERE
            # sort the locked list according to y value in (x,y) and then reverse
            # reversed because otherwise the ones on the top will overwrite the lower ones
            for key in sorted(list(locked), key=lambda a: a[1])[::-1]:
                x_2, y_2 = key
                if y_2 < index:                       # if the y value is above the removed index
                    new_key_2 = (x_2, y_2 + increment)    # shift position to down
                    locked[new_key_2] = locked.pop(key)
        return increment

# draws the upcoming piece to the left of the screen 

# NOTE FOR ANDY AND SAMANTHA - can delete the draw_next_shape and it will remove the 'next shape' feauture that is shown on the right of the screen, could be used to make more space for the split screen feature 
def draw_next_shape(piece, surface, pos):
    if pos == 0:
        font = pygame.font.Font(fontpath, 30) # set font 
        label = font.render('Next shape', 1, (255, 255, 255))
        start_x = top_left_x + play_width + 50
        start_y = top_left_y + (play_height / 2 - 100)
        shape_format = piece.shape[piece.rotation % len(piece.shape)] # note the piece.rotation uses the built in library function of pygame
        # Loop through the rows and columns of the shape format
        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    # the draw rect is used to draw rectangles
                    pygame.draw.rect(surface, piece.color, ((start_x) + j*block_size, start_y + i*block_size, block_size, block_size), 0)
                    # piece.color - random
        surface.blit(label, (start_x, start_y - 50))
    elif pos == 1:
        font_2 = pygame.font.Font(fontpath, 30) # set font 
        label_2 = font_2.render('Next shape', 1, (255, 255, 255))
        start_x_2 = (top_left_x+600) + play_width + 50
        start_y = top_left_y + (play_height / 2 - 100)
        shape_format_2 = piece.shape[piece.rotation % len(piece.shape)] # note the piece.rotation uses the built in library function of pygame
        # Loop through the rows and columns of the shape format
        for i, line in enumerate(shape_format_2):
            row_2 = list(line)
            for j, column in enumerate(row_2):
                if column == '0':
                    # the draw rect is used to draw rectangles
                    pygame.draw.rect(surface, piece.color, ((start_x_2) + j*block_size, start_y + i*block_size, block_size, block_size), 0)
                    # piece.color - random 
        surface.blit(label_2, (start_x_2, start_y - 50))

    # pygame.display.update()


# draws the content of the window
# Renders everything on-to the window 
def draw_window(surface, grid, score=0, last_score=0):
    surface.fill((0, 0, 0))  # fill the surface with black
    pygame.font.init()  # initialise font
    font = pygame.font.Font(fontpath_mario, 65)
    font.set_bold(True)
    # NOTE: For group we can change the title with this 
    label = font.render('TETRIS', 1, (255, 255, 255))  # initialise 'Tetris' text with white

    surface.blit(label, ((top_left_x + play_width / 2) - (label.get_width() / 2), 30))  # put surface on the center of the window

    # current score
    font = pygame.font.Font(fontpath, 30)
    label = font.render('SCORE   ' + str(score) , 1, (255, 255, 255))

    start_x = top_left_x + play_width + 50
    start_y = top_left_y + (play_height / 2 - 100)
    surface.blit(label, (start_x, start_y + 200)) #Score text
    surface.blit(label, (start_x+600, start_y + 200)) #Score text for Player 2

    # last score
    label_hi = font.render('HIGHSCORE   ' + str(last_score), 1, (255, 255, 255))

    start_x_hi = top_left_x - 240
    start_y_hi = top_left_y + 200

    surface.blit(label_hi, (start_x_hi + 20, start_y_hi + 200)) # NOTE: put the HIGHSCORE POSITION in the bottom place

    # draw content of the grid
    for i in range(row):
        for j in range(col):
            # pygame.draw.rect()
            # draw a rectangle shape
            # rect(Surface, color, Rect, width=0) -> Rect

            # Use pygame.draw.rect to draw each block on the grid.
            pygame.draw.rect(surface, grid[i][j],
                             (top_left_x + j * block_size, top_left_y + i * block_size, block_size, block_size), 0)
    for i_2 in range(row_2):
        for j_2 in range(col_2):
            # pygame.draw.rect()
            # draw a rectangle shape
            # rect(Surface, color, Rect, width=0) -> Rect

            # Use pygame.draw.rect to draw each block on the grid.
            pygame.draw.rect(surface, grid[i_2][j_2],
                             (top_left_x_2 + j * block_size, top_left_y_2 + i * block_size, block_size, block_size), 0)
            # NOTE: To clarify for the code above, this only draws the GRID, but not the actual shapes

    # draw vertical and horizontal grid lines
    draw_grid(surface)

    # draw rectangular border around play area
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (top_left_x, top_left_y, play_width, play_height), 4)
    pygame.draw.rect(surface, border_color, ((top_left_x*3), top_left_y, play_width, play_height), 4)

# update the score txt file with high score
def update_score(new_score):
    score = get_max_score()

    with open(filepath, 'w') as file:
        if new_score > score:
            file.write(str(new_score))
        else:
            file.write(str(score))


# get the high score from the file
def get_max_score():
    with open(filepath, 'r') as file:
        lines = file.readlines()        # reads all the lines and puts in a list
        score = int(lines[0].strip())   # remove \n

    return score


def main(window):
    locked_positions = {}
    create_grid(locked_positions , 0)
    change_piece = False
    run = True
    current_piece = get_shape(1)
    next_piece = get_shape(1)
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0
    last_score = get_max_score() 
    
    #Player 2 Variables in the following
    locked_positions_2 = {}
    create_grid(0 , locked_positions_2)
    change_piece_2 = False
    run_2 = True
    current_piece_2 = get_shape(2)
    next_piece_2 = get_shape(2)
    clock_2 = pygame.time.Clock()
    fall_time_2 = 0
    fall_speed_2 = 0.35
    level_time_2 = 0
    score_2 = 0
    last_score_2 = get_max_score() 

    while run or run_2:
        # need to constantly make new grid as locked positions always change
        grid , rand = create_grid(locked_positions, 0)
        rand, grid_2 = create_grid(0 , locked_positions_2)
        # helps run the same on every computer
        # add time since last tick() to fall_time
        fall_time += clock.get_rawtime()  # returns in milliseconds
        level_time += clock.get_rawtime()
        
        fall_time_2 += clock.get_rawtime()  # returns in milliseconds of player 2
        level_time_2 += clock.get_rawtime()

        clock.tick()  # updates clock

        if level_time/1000 > 5:    # make the difficulty harder every 10 seconds
            level_time = 0
            if fall_speed > 0.15:   # until fall speed is 0.15
                fall_speed -= 0.005
                
        if level_time_2/1000 > 5:    # make the difficulty harder every 10 seconds for player 2
            level_time_2 = 0
            if fall_speed_2 > 0.15:   # until fall speed is 0.15 for player 2
                fall_speed_2 -= 0.005

        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid, 1) and current_piece.y > 0:
                current_piece.y -= 1
                # since only checking for down - either reached bottom or hit another piece
                # need to lock the piece position
                # need to generate new piece
                change_piece = True
                
        if fall_time_2 / 1000 > fall_speed_2: #For player 2
            fall_time_2 = 0
            current_piece_2.y_2 += 1
            if not valid_space(current_piece_2, grid_2, 2) and current_piece_2.y_2 > 0:
                current_piece_2.y_2 -= 1
                # since only checking for down - either reached bottom or hit another piece
                # need to lock the piece position
                # need to generate new piece
                change_piece_2 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                run_2 = False
                pygame.display.quit()
                quit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    current_piece_2.x_2 -= 1  # move x position left
                    if not valid_space(current_piece_2, grid_2, 2):
                        current_piece_2.x_2 += 1

                elif event.key == pygame.K_d:
                    current_piece_2.x_2 += 1  # move x position right
                    if not valid_space(current_piece_2, grid_2, 2):
                        current_piece_2.x_2 -= 1

                elif event.key == pygame.K_s:
                    # move shape down
                    current_piece_2.y_2 += 1
                    if not valid_space(current_piece_2, grid_2, 2):
                        current_piece_2.y_2 -= 1

                elif event.key == pygame.K_w:
                    # rotate shape
                    current_piece_2.rotation = current_piece_2.rotation + 1 % len(current_piece_2.shape)
                    if not valid_space(current_piece_2, grid_2, 2):
                        current_piece_2.rotation = current_piece_2.rotation - 1 % len(current_piece_2.shape)
                
                #FOLLOWING INPUTS FOR PLAYER 1 from line 508
                        
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1  # move x position left
                    if not valid_space(current_piece, grid, 1):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1  # move x position right
                    if not valid_space(current_piece, grid, 1):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid, 1):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid, 1):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                        
                elif event.key == K_ESCAPE:
                    pygame.display.quit()
                    quit()

        piece_pos = convert_shape_format(current_piece, 1)
        piece_pos_2 = convert_shape_format(current_piece_2, 2)

        # draw the piece on the grid by giving color in the piece locations
        for i in range(len(piece_pos)):
            x, y = piece_pos[i]
            if y >= 0:
                grid[y][x] = current_piece.color
                
        for i_2 in range(len(piece_pos_2)):
            x_2, y_2 = piece_pos_2[i_2]
            if y_2 >= 0:
                grid_2[y_2][x_2-20] = current_piece_2.color
                
        if change_piece:  # if the piece is locked
            for pos in piece_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color       # add the key and value in the dictionary
            current_piece = next_piece
            next_piece = get_shape(1)
            change_piece = False
            # CODE NEEDED TO ADD POINTS (WHEN USER CLEARS ROW)
            score += clear_rows(grid, locked_positions, 1) * 10    # increment score by 10 for every row cleared
            update_score(score)
            
        if change_piece_2:  # if the piece is locked
            for pos_2 in piece_pos_2:
                p = (pos_2[0], pos_2[1])
                locked_positions_2[p] = current_piece_2.color       # add the key and value in the dictionary
            current_piece_2 = next_piece_2
            next_piece_2 = get_shape(2)
            change_piece_2 = False
            # CODE NEEDED TO ADD POINTS (WHEN USER CLEARS ROW)
            score += clear_rows(grid_2, locked_positions_2, 2) * 10    # increment score by 10 for every row cleared
            update_score(score_2)

            # NOTE FOR GROUP: THIS IS WHEN THE CURRENT SCORE THE USER GETS BEATS THE HISTORIC SCORE OF ALL TIME (WE CAN PERHAPS DO SOMETHING SPECIAL FOR THIS )
            if last_score < score:
                pass
            if last_score_2 < score_2:
                pass
                    # Loading the song 
                #mixer.music.load("yay.mp3") 
                #yay_sound.play()
                #pygame.mixer.Channel(1).play(yay_sound)  
   
                #last_score = score
                # Setting the volume 
                #mixer.music.set_volume(0.5)

                #mixer.music.play(-1)
                #last_score = score
        draw_window(window, grid_2, score, last_score)
        draw_next_shape(next_piece_2, window, 1)
        
        pygame.display.update()
        if check_lost(locked_positions, 1):
            run = False
        if check_lost(locked_positions_2, 2):
            run_2 = False

    draw_text_middle('You Lost', 40, (255, 255, 255), window)
    pygame.display.update()
    pygame.time.delay(2000)  # wait for 2 seconds
    pygame.quit()


def main_menu(window):
    run = True
    run_2 = True
    while run or run_2:
        draw_text_middle('Press any key to begin', 50, (255, 255, 255), window)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.display.quit() 
                    quit()
                else:
                    main(window)
                
    pygame.quit()


if __name__ == '__main__':
    win = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption('Tetris')

    main_menu(win)  # start game

