from settings import *
from sys import exit

from logic import Game
from score import Score
from preview import Preview


class Main:
    def __init__(self):
        
        # general
        pygame.init() # create a window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) # set window dimensions
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("HOLD MY LINE PIECE") # set window name
        
        # shapes
        self.next_shapes = [random_shape() for shape in range(3)]
        # print(self.next_shapes)
        

        # Components    
        self.game = Game(self.get_next_shape)
        self.score = Score()
        self.preview = Preview()
    


    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(random_shape())
        return next_shape

    def run(self):
        while True:
            
            for event in pygame.event.get():
                # Handle closing the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            # display
            self.display_surface.fill(NIGHT_RIDER)

            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            # Update game
            pygame.display.update()
            self.clock.tick()
        

def random_shape():
    return choice(list(TETROMINOES.keys()))

if __name__ == '__main__':
    main = Main()
    main.run()
