from settings import *
from random import choice
from Timer import Timer


class Game:
    def __init__(self):
        
        # general
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT)) # Game surface
        self.display_surface = pygame.display.get_surface() # Surface from Main
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()

        # Line surface to set alpha value
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # Tetromnio
        self.data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]
        self.create_new_tetromino(False)

        # Timer
        self.Timers = {
            'vertical move' : Timer(UPDATE_START_SPEED, True, self.move_down),
            'horizontal move' : Timer(MOVE_WAIT_TIME),
            'rotate' : Timer(ROTATE_WAIT_TIME)
        }

        self.Timers['vertical move'].activate()
        self.Timers['horizontal move'].activate()

    def create_new_tetromino(self, fix_previous):
        # If not the first fix the previous
        if fix_previous:
            for block in self.tetromino.blocks:
                x,y = block.pos
                x = int(x)
                y = int(y)
                self.data[y][x] = 1
                
        # Create new random shape tetr
        self.tetromino = Tetromino(
            choice(list(TETROMINOES.keys())) , 
            self.sprites, 
            self.create_new_tetromino,
            self.data)
        
    def timer_update(self):
        for timer in self.Timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()
    
    def move_horizontal(self, dx):
        self.tetromino.move_horizontal(dx)

    # Drawing each line, attaching the grid onto the Game
    def draw_grid(self):
        
        for col in range(1,COLUMNS):
            x = col*CELL_SIZE
            pygame.draw.line(self.line_surface, GRID_LINE_COLOR, (x,0), (x, GAME_HEIGHT))

        for row in range(1,ROWS):
            y = row*CELL_SIZE
            pygame.draw.line(self.line_surface, GRID_LINE_COLOR, (0,y), (GAME_WIDTH, y))

        self.surface.blit(self.line_surface, (0,0))

    def input(self):

        # Can not take input at the moment
            
        
        keys = pygame.key.get_pressed()

        if not self.Timers['horizontal move'].active:
            dx = 0
            # Moving left
            if keys[pygame.K_LEFT]:
                dx -= 1
            # Moving right
            if keys[pygame.K_RIGHT]:
                dx += 1

            if dx:
                self.move_horizontal(dx)
                self.Timers['horizontal move'].activate()

        if not self.Timers['rotate'].activate:
            # Rotate ccw    
            if keys[pygame.K_z]:
                pass
            # Rotate cw
            if keys[pygame.K_x]:
                pass
 
    def run(self):
        
        # input
        self.input()

        # update
        self.timer_update()
        self.sprites.update()

        self.surface.fill(GAME_COLOR)
        self.sprites.draw(self.surface) 

        self.draw_grid()
        self.display_surface.blit(self.surface, (PADDING,PADDING))
        
        pygame.draw.rect(self.display_surface, WHEAT, self.rect, 2, 2)


class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, grid):
        
        # Setup
        self.block_positions = TETROMINOES[shape]['shape']
        self.color = TETROMINOES[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.grid = grid

        # Create Blocks
        self.blocks = [Block(group, pos, self.color) for pos in self.block_positions]

    # collisions
    def next_move_horizontal_collide(self, amount):
        collision_list = [block.horizontal_collide(block.pos.x + amount, self.grid) for block in self.blocks]
        
        if any(collision_list):
            return True
        
        return False

    def next_move_vertical_collide(self, amount):
        collision_list = [block.vertical_collide(block.pos.y + amount, self.grid) for block in self.blocks]
        
        if any(collision_list):
            return True
        
        return False

    def move_down(self):

        if self.next_move_vertical_collide(1):
            self.create_new_tetromino(True)
            return

        for block in self.blocks:
            block.pos.y += 1

    def move_horizontal(self, dx):
        
        if self.next_move_horizontal_collide(dx):
            return
            
        for block in self.blocks:
            block.pos.x += dx


class Block(pygame.sprite.Sprite):
    def __init__(self, groups, pos, color):
        
        # general
        super().__init__(groups)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def update(self):
        self.rect.topleft = self.pos * CELL_SIZE

    def horizontal_collide(self, x, grid):
        x = int(x)
        y = int(self.pos.y)

        return (not 0 <= x < COLUMNS) or grid[y][x]
    
    def vertical_collide(self, y, grid):
        
        x = int(self.pos.x)
        y = int(y)

        return (not 0 <= y < ROWS) or grid[y][x]
         