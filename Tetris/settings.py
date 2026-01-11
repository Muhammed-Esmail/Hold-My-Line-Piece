import pygame
from random import choice

# Game size
COLUMNS = 10
ROWS = 20
CELL_SIZE = 40
GAME_WIDTH, GAME_HEIGHT = COLUMNS * CELL_SIZE, ROWS * CELL_SIZE

# Side bar [score and preview]
SIDEBAR_WIDTH = 200
PREVIEW_HEIGHT_FRACTION = 0.7 # 70%
SCORE_HEIGHT_FRACTION = 1 - PREVIEW_HEIGHT_FRACTION

# Window
PADDING = 20
WINDOW_WIDTH = GAME_WIDTH + SIDEBAR_WIDTH + PADDING * 3
WINDOW_HEIGHT = GAME_HEIGHT + PADDING * 2

BLOCK_OFFSET = pygame.Vector2(COLUMNS//2, 2)

# Game behaviour 
UPDATE_START_SPEED = 300
MOVE_WAIT_TIME = 150
ROTATE_WAIT_TIME = 200

# Colors
SKY_BLUE     = "#87CEEB"
ROYAL_BLUE   = "#4169E1"
NAVY_BLUE    = "#000080"
EMERALD      = "#50C878"
OLIVE        = "#808000"
GOLD         = "#FFD700"
ORANGE       = "#FFA500"
CORAL        = "#FF7F50"
HOT_PINK     = "#FF69B4"
PURPLE       = "#800080"
INDIGO       = "#4B0082"
CRIMSON      = "#DC143C"
SILVER       = "#C0C0C0"
GRAY         = "#808080"
DARK_GRAY    = "#A9A9A9"
SLATE_GRAY   = "#708090"
NIGHT_RIDER  = "#333333"
CHOCOLATE    = "#D2691E"
SADDLE_BROWN = "#8B4513"
SANDY_BROWN  = "#F4A460"
WHEAT        = "#F5DEB3"
BEIGE        = "#F5F5DC"

GAME_COLOR = NIGHT_RIDER
PREVIEW_COLOR = SLATE_GRAY
WINDOW_BORDER_COLOR = SKY_BLUE
SCORE_COLOR = SLATE_GRAY
GRID_LINE_COLOR = SLATE_GRAY

T_SHAPE_COLOR = PURPLE       # Standard purple
O_SHAPE_COLOR = GOLD         # Bright yellow
J_SHAPE_COLOR = ROYAL_BLUE   # Deep blue
L_SHAPE_COLOR = ORANGE       # Standard orange
I_SHAPE_COLOR = SKY_BLUE     # Cyan/Light blue
S_SHAPE_COLOR = EMERALD      # Vibrant green
Z_SHAPE_COLOR = CRIMSON      # Sharp red


# Shapes

TETROMINOES = {
    'T': {'shape': [(0,0), (-1,0), (1 , 0), (0,-1)], 'color' : T_SHAPE_COLOR},
    'O': {'shape': [(0,0), (-1,0), (-1,-1), (0,-1)], 'color' : O_SHAPE_COLOR},
    'J': {'shape': [(0,0), (0,-1), (0 , 1), (-1,1)], 'color' : J_SHAPE_COLOR},
    'L': {'shape': [(0,0), (0,-1), (0 , 1), (1,1)], 'color' : L_SHAPE_COLOR},
    'I': {'shape': [(0,0), (-1,0), (-2,0), (1,0)], 'color' : I_SHAPE_COLOR},
    'S': {'shape': [(0,0), (-1,0), (0,-1), (1,-1)], 'color' : S_SHAPE_COLOR},
    'Z': {'shape': [(0,0), (1,0), (0,-1), (-1,-1)],'color' : Z_SHAPE_COLOR}
}
