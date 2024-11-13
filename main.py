"""
Karan Patel Chess Bot Project

Current Progress:
- Board Created
- Pieces loaded in
- Ability to move pieces on the board based on turn

To Do:
- Program all legal moves
- Program winning/losing
- Research and implement basic reinforcement learning model

Please check https://github.com/k22patel/Chess_bot for updates.

"""

import pygame

# initialize pygame and display settings

pygame.init()
WIDTH = 800
HEIGHT = 800
surface = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Chess')
font = pygame.font.Font('freesansbold.ttf', 20)
big_font = pygame.font.Font('freesansbold.ttf', 30)

# Timer settings for future use
timer = pygame.time.Clock()
fps = 60
color = 'gray'
surface.fill(color)
pygame.display.flip()

# Variable to store if game is at play
play = True

# Black piece order and locations
black_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_loc = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7),
             (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7)]

# White piece order and location
white_pieces = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']

white_loc = [(7, 0), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (7, 7),
             (6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7)]

# Sprite dimensions
image_width = 70
image_height = 70

# Load in white and black piece sprites
white_queen = pygame.image.load('1x/w_queen_1x_ns.png')
white_queen = pygame.transform.scale(white_queen, (image_width, image_width))
white_rook = pygame.image.load('1x/w_rook_1x_ns.png')
white_rook = pygame.transform.scale(white_rook, (image_width, image_width))
white_knight = pygame.image.load('1x/w_knight_1x_ns.png')
white_knight = pygame.transform.scale(white_knight, (image_width, image_width))
white_bishop = pygame.image.load('1x/w_bishop_1x_ns.png')
white_bishop = pygame.transform.scale(white_bishop, (image_width, image_width))
white_king = pygame.image.load('1x/w_king_1x_ns.png')
white_king = pygame.transform.scale(white_king, (image_width, image_width))
white_pawn = pygame.image.load('1x/w_pawn_1x_ns.png')
white_pawn = pygame.transform.scale(white_pawn, (image_width, image_width))

white_sprites = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop, white_knight,
                 white_rook, white_pawn, white_pawn, white_pawn, white_pawn, white_pawn, white_pawn,
                 white_pawn, white_pawn]

black_queen = pygame.image.load('1x/b_queen_1x_ns.png')
black_queen = pygame.transform.scale(black_queen, (image_width, image_width))
black_rook = pygame.image.load('1x/b_rook_1x_ns.png')
black_rook = pygame.transform.scale(black_rook, (image_width, image_width))
black_knight = pygame.image.load('1x/b_knight_1x_ns.png')
black_knight = pygame.transform.scale(black_knight, (image_width, image_width))
black_bishop = pygame.image.load('1x/b_bishop_1x_ns.png')
black_bishop = pygame.transform.scale(black_bishop, (image_width, image_width))
black_king = pygame.image.load('1x/b_king_1x_ns.png')
black_king = pygame.transform.scale(black_king, (image_width, image_width))
black_pawn = pygame.image.load('1x/b_pawn_1x_ns.png')
black_pawn = pygame.transform.scale(black_pawn, (image_width, image_width))

black_sprites = [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop, black_knight,
                 black_rook, black_pawn, black_pawn, black_pawn, black_pawn, black_pawn, black_pawn, black_pawn,
                 black_pawn]


# Function to draw the board after each move
def draw():
    # Loop through each of the 64 tiles and color them accordingly
    for i in range(64):
        col = i % 8
        row = i // 8
        if row % 2 == 0 and col % 2 == 0 or row % 2 == 1 and col % 2 == 1:
            pygame.draw.rect(surface, (209, 175, 132),
                             [col * 80 + (WIDTH - 640) / 2, row * 80 + (HEIGHT - 640) / 2, 80, 80])
        else:
            pygame.draw.rect(surface, (160, 82, 45),
                             [col * 80 + (WIDTH - 640) / 2, row * 80 + (HEIGHT - 640) / 2, 80, 80])
    # Loop through the black pieces and place them at the right loc
    for i in range(len(black_sprites)):
        surface.blit(black_sprites[i], (
            (black_loc[i][1] * 80 + (WIDTH - 640) / 2) + 5, ((black_loc[i][0] * 80 + (HEIGHT - 640) / 2) + 5)))
    # Loop through the white pieces and place them at the right loc
    for i in range(len(white_sprites)):
        surface.blit(white_sprites[i], ((white_loc[i][1] * 80 + (WIDTH - 640) / 2) + 5, ((white_loc[i][0] * 80 +
                                                                                          (HEIGHT - 640) / 2) + 5)))


# Call the draw function initially
draw()

# Step variable to determine whose step it is
step = 0
# variable to determine which piece is selected
cur_piece = [-1, -1]

# update the display after draw
pygame.display.flip()

valid_moves = []


def get_valid_white():
    out = []

    for ind, piece in enumerate(white_pieces):
        if piece == 'pawn':
            if white_loc[ind][0] == 6:
                if (5, white_loc[ind][1]) not in white_loc and (5, white_loc[ind][1]) not in black_loc:
                    out.append((white_loc[ind], (5, white_loc[ind][1])))
                    if (4, white_loc[ind][1]) not in white_loc and (4, white_loc[ind][1]) not in black_loc:
                        out.append((white_loc[ind], (4, white_loc[ind][1])))

            elif (white_loc[ind][0] - 1, white_loc[ind][1]) not in white_loc and \
                    (white_loc[ind][0] - 1, white_loc[ind][1]) not in black_loc:
                out.append((white_loc[ind], (white_loc[ind][0] - 1, white_loc[ind][1])))

            if (white_loc[ind][0] - 1, white_loc[ind][1] + 1) in black_loc:
                out.append((white_loc[ind], (white_loc[ind][0] - 1, white_loc[ind][1] + 1)))

            if (white_loc[ind][0] - 1, white_loc[ind][1] - 1) in black_loc:
                out.append((white_loc[ind], (white_loc[ind][0] - 1, white_loc[ind][1] - 1)))

        elif piece == 'rook':
            r_row = white_loc[ind][0]
            r_col = white_loc[ind][1]

            for i in range(r_row + 1, 8):
                if (i, r_col) not in white_loc and (i, r_col) not in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                elif (i, r_col) in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                    break
                elif (i, r_col) in white_loc:
                    break

            for i in range(r_row - 1, -1, -1):
                if (i, r_col) not in white_loc and (i, r_col) not in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                elif (i, r_col) in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                    break
                elif (i, r_col) in white_loc:
                    break

            for i in range(r_col + 1, 8):
                if (r_row, i) not in white_loc and (r_row, i) not in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                elif (r_row, i) in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                    break
                elif (r_row, i) in white_loc:
                    break

            for i in range(r_col - 1, -1, -1):
                if (r_row, i) not in white_loc and (r_row, i) not in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                elif (r_row, i) in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                    break
                elif (r_row, i) in white_loc:
                    break

        elif piece == 'bishop':
            r_row = white_loc[ind][0]
            r_col = white_loc[ind][1]

            tr = min(r_row, 7-r_col)
            tl = min(r_row, r_col)
            bl = min(7-r_row, r_col)
            br = min(7-r_row, 7-r_col)

            for i in range(1, tr+1):
                if (r_row - i, r_col + i) not in white_loc and (r_row - i, r_col + i) not in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col + i)))
                elif (r_row - i, r_col + i) in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col + i)))
                    break
                elif (r_row - i, r_col + i) in white_loc:
                    break

            for i in range(1, tl+1):
                if (r_row - i, r_col - i) not in white_loc and (r_row - i, r_col - i) not in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col - i)))
                elif (r_row - i, r_col - i) in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col - i)))
                    break
                elif (r_row - i, r_col - i) in white_loc:
                    break

            for i in range(1, bl+1):
                if (r_row + i, r_col - i) not in white_loc and (r_row + i, r_col - i) not in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col - i)))
                elif (r_row + i, r_col - i) in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col - i)))
                    break
                elif (r_row + i, r_col - i) in white_loc:
                    break

            for i in range(1, br+1):
                if (r_row + i, r_col + i) not in white_loc and (r_row + i, r_col + i) not in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col + i)))
                elif (r_row + i, r_col + i) in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col + i)))
                    break
                elif (r_row + i, r_col + i) in white_loc:
                    break

        elif piece == 'knight':
            r_row = white_loc[ind][0]
            r_col = white_loc[ind][1]

            tl = min(r_row, r_col)
            bl = min(7-r_row, r_col)
            br = min(7-r_row, 7-r_col)

            if r_row > 1 and 7-r_col > 0:
                if (r_row - 2, r_col + 1) not in white_loc:
                    out.append((white_loc[ind], (r_row - 2, r_col + 1)))

            if r_row > 0 and 7-r_col > 1:
                if (r_row - 1, r_col + 2) not in white_loc:
                    out.append((white_loc[ind], (r_row - 1, r_col + 2)))

            if r_row > 0 and r_col > 1:
                if (r_row - 1, r_col - 2) not in white_loc:
                    out.append((white_loc[ind], (r_row - 1, r_col - 2)))

            if r_row > 1 and r_col > 0:
                if (r_row - 2, r_col - 1) not in white_loc:
                    out.append((white_loc[ind], (r_row - 2, r_col - 1)))

            if 7 - r_row > 1 and 7-r_col > 0:
                if (r_row + 2, r_col + 1) not in white_loc:
                    out.append((white_loc[ind], (r_row + 2, r_col + 1)))

            if 7 - r_row > 0 and 7-r_col > 1:
                if (r_row + 1, r_col + 2) not in white_loc:
                    out.append((white_loc[ind], (r_row + 1, r_col + 2)))

            if 7 - r_row > 0 and r_col > 1:
                if (r_row + 1, r_col - 2) not in white_loc:
                    out.append((white_loc[ind], (r_row + 1, r_col - 2)))

            if 7 - r_row > 1 and r_col > 0:
                if (r_row + 2, r_col - 1) not in white_loc:
                    out.append((white_loc[ind], (r_row + 2, r_col - 1)))

        elif piece == 'queen':
            r_row = white_loc[ind][0]
            r_col = white_loc[ind][1]

            tr = min(r_row, 7-r_col)
            tl = min(r_row, r_col)
            bl = min(7-r_row, r_col)
            br = min(7-r_row, 7-r_col)

            for i in range(1, tr+1):
                if (r_row - i, r_col + i) not in white_loc and (r_row - i, r_col + i) not in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col + i)))
                elif (r_row - i, r_col + i) in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col + i)))
                    break
                elif (r_row - i, r_col + i) in white_loc:
                    break

            for i in range(1, tl+1):
                if (r_row - i, r_col - i) not in white_loc and (r_row - i, r_col - i) not in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col - i)))
                elif (r_row - i, r_col - i) in black_loc:
                    out.append(((r_row, r_col), (r_row - i, r_col - i)))
                    break
                elif (r_row - i, r_col - i) in white_loc:
                    break

            for i in range(1, bl+1):
                if (r_row + i, r_col - i) not in white_loc and (r_row + i, r_col - i) not in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col - i)))
                elif (r_row + i, r_col - i) in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col - i)))
                    break
                elif (r_row + i, r_col - i) in white_loc:
                    break

            for i in range(1, br+1):
                if (r_row + i, r_col + i) not in white_loc and (r_row + i, r_col + i) not in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col + i)))
                elif (r_row + i, r_col + i) in black_loc:
                    out.append(((r_row, r_col), (r_row + i, r_col + i)))
                    break
                elif (r_row + i, r_col + i) in white_loc:
                    break

            for i in range(r_row + 1, 8):
                if (i, r_col) not in white_loc and (i, r_col) not in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                elif (i, r_col) in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                    break
                elif (i, r_col) in white_loc:
                    break

            for i in range(r_row - 1, -1, -1):
                if (i, r_col) not in white_loc and (i, r_col) not in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                elif (i, r_col) in black_loc:
                    out.append(((r_row, r_col), (i, r_col)))
                    break
                elif (i, r_col) in white_loc:
                    break

            for i in range(r_col + 1, 8):
                if (r_row, i) not in white_loc and (r_row, i) not in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                elif (r_row, i) in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                    break
                elif (r_row, i) in white_loc:
                    break

            for i in range(r_col - 1, -1, -1):
                if (r_row, i) not in white_loc and (r_row, i) not in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                elif (r_row, i) in black_loc:
                    out.append(((r_row, r_col), (r_row, i)))
                    break
                elif (r_row, i) in white_loc:
                    break

        elif piece == 'king':
            r_row = white_loc[ind][0]
            r_col = white_loc[ind][1]

            if 7 - r_row > 0 and 7 - r_col > 0 and (r_row + 1, r_col + 1) not in white_loc:
                out.append((white_loc[ind], (r_row + 1, r_col + 1)))

            if r_row > 0 and 7 - r_col > 0 and (r_row - 1, r_col + 1) not in white_loc:
                out.append((white_loc[ind], (r_row - 1, r_col + 1)))

            if r_row > 0 and r_col > 0 and (r_row - 1, r_col - 1) not in white_loc:
                out.append((white_loc[ind], (r_row - 1, r_col - 1)))

            if 7 - r_row > 0 and r_col > 0 and (r_row + 1, r_col - 1) not in white_loc:
                out.append((white_loc[ind], (r_row + 1, r_col - 1)))

            if 7 - r_row > 0 and (r_row + 1, r_col) not in white_loc:
                out.append((white_loc[ind], (r_row + 1, r_col)))

            if r_row > 0 and (r_row - 1, r_col) not in white_loc:
                out.append((white_loc[ind], (r_row - 1, r_col)))

            if r_col > 0 and (r_row, r_col - 1) not in white_loc:
                out.append((white_loc[ind], (r_row, r_col - 1)))

            if 7 - r_col > 0 and (r_row, r_col + 1) not in white_loc:
                out.append((white_loc[ind], (r_row, r_col + 1)))

    return out


def is_check(white_temp):

    return True


# Loop while playing
while play:
    timer.tick(fps)
    # for each event i.e quit or mouse button click
    for event in pygame.event.get():
        # quit then exit while loop
        if event.type == pygame.QUIT:
            play = False
        # if button is clicked via left click then proceed
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # determine the location of the click
            col = event.pos[0] // 80
            row = event.pos[1] // 80
            loc = (row - 1, col - 1)
            # if it's white turn and the click was on a white piece then select it
            if (step == 0 and loc in white_loc) or (step == 1 and loc in white_loc):
                draw()
                pygame.draw.rect(surface, (0, 0, 0),
                                 [col * 80, row * 80, 80, 80], 3)
                if step == 0:
                    step += 1

                cur_piece = loc
                valid_moves = get_valid_white()
            # if the next click is not a white piece then move the prev white piece there
            elif step == 1 and loc not in white_loc and 0 <= loc[0] < 8 and 0 <= loc[1] < 8:

                move = (cur_piece, loc)
                if move in valid_moves:

                    step += 1
                    index = white_loc.index(cur_piece)
                    white_loc[index] = loc
                    if loc in black_loc:
                        index = black_loc.index(loc)
                        del black_sprites[index]
                        del black_pieces[index]
                        black_loc.remove(loc)

                    draw()
                    pygame.draw.rect(surface, (0, 0, 0),
                                     [col * 80, row * 80, 80, 80], 3)

            # if black's turn and black piece is clicked on then select it
            elif (step == 2 and loc in black_loc) or (step == 3 and loc in black_loc):
                draw()
                pygame.draw.rect(surface, (0, 0, 0),
                                 [col * 80, row * 80, 80, 80], 3)
                if step == 2:
                    step += 1

                cur_piece = loc
            # if the next click is not a black piece then move the prev black piece there
            elif step == 3 and loc not in black_loc and 0 <= loc[0] < 8 and 0 <= loc[1] < 8:
                step = 0
                index = black_loc.index(cur_piece)
                black_loc[index] = loc
                if loc in white_loc:
                    index = white_loc.index(loc)
                    del white_sprites[index]
                    del white_pieces[index]
                    white_loc.remove(loc)
                draw()
                pygame.draw.rect(surface, (0, 0, 0),
                                 [col * 80, row * 80, 80, 80], 3)
    # Update display after event
    pygame.display.flip()
# quit game once exited out of while loop
pygame.quit()
