from settings import *
from Timer import Timer


class Game:
    def __init__(self, get_next_shape):
        
        # general
        self.surface = pygame.Surface((GAME_WIDTH,GAME_HEIGHT)) # Game surface
        self.display_surface = pygame.display.get_surface() # Surface from Main
        self.rect = self.surface.get_rect(topleft = (PADDING,PADDING))
        self.sprites = pygame.sprite.Group()
        self.get_next_shape = get_next_shape

        # Line surface to set alpha value
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        # Tetromnio
        self.clear_data()
        self.create_new_tetromino(False)

        # Timer
        self.down_speed = UPDATE_START_SPEED
        self.down_speed_faster = self.down_speed * 0.3
        self.down_pressed = False

        self.Timers = {
            'vertical move' : Timer(self.down_speed, True, self.move_down),
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
                self.data[y][x] = block
       
        self.check_finished_rows()
        
        # Create new random shape tetr
        self.tetromino = Tetromino(
            self.get_next_shape() , 
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
 
        keys = pygame.key.get_pressed()
        
        # horizontal input
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
            
        
        # rotation
        if not self.Timers['rotate'].active:
            # Rotate ccw    
            if keys[pygame.K_z]: 
                pass        

            # Rotate cw
            if keys[pygame.K_x] or keys[pygame.K_UP]: 
                self.tetromino.rotate()
                self.Timers['rotate'].activate()
        
        # down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.Timers['vertical move'].duration = self.down_speed_faster
            print('Pressing Down')

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.Timers['vertical move'].duration = self.down_speed
            print('Down released')

            
            

    def clear_data(self):
        
        self.data = [[0 for x in range(COLUMNS)] for y in range(ROWS)]

    def check_finished_rows(self):
        # get full row indexes
        # inside data
        delete_rows = []
        for i, row in enumerate(self.data):
            if all(row):
                delete_rows.append(i)
        
        if delete_rows:
            for full_row in delete_rows:
                # delete full rows
                for block in self.data[full_row]:
                    block.kill()

                # move above rows down
                for falling_row in range(0, full_row):
                    for block in self.data[falling_row]:
                        if block:
                            block.pos.y += 1

            self.clear_data()

            # rebuild data table
            for block in self.sprites:
                x,y = block.pos
                x = int(x)
                y = int(y)
                self.data[y][x] = block


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
        self.shape = shape
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

    # rotate method
    def rotate(self):
        if self.shape != 'O':
            # 1. pivot point
            pivot_pos = self.blocks[0].pos

            # 2. new block position
            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
        
            # 3. collision check
            for pos in new_block_positions:
                x = int(pos.x)
                y = int(pos.y)
                # horizontal check
                if x < 0 or x >= COLUMNS:
                    return

                # vertical check
                if y >= ROWS:
                    return

                # field check
                if self.grid[y][x]:
                    return
                
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
            


class Block(pygame.sprite.Sprite):
    def __init__(self, groups, pos, color):
        
        # general
        super().__init__(groups)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        # position
        self.pos = pygame.Vector2(pos) + BLOCK_OFFSET
        self.rect = self.image.get_rect(topleft = self.pos * CELL_SIZE)

    def rotate(self, pivot_pos):
        distance = self.pos - pivot_pos
        rotated = distance.rotate(90)
        new_pos = pivot_pos + rotated
        return new_pos

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
