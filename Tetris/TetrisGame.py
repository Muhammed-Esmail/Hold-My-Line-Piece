from settings import *
from sys import exit

from logic import Game
from score import Score
from preview import Preview
from State import MainMenu

class Main:
    def __init__(self):
        
        # general
        pygame.init() # create a window
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT)) # set window dimensions
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("HOLD MY LINE PIECE") # set window name
        
        # Main game menu
        self.state = MainMenu()

        # shapes
        self.next_shapes = [random_shape() for shape in range(3)]


    def new_game(self):
        # Components    
        self.score = Score()
        self.game = Game(self.get_next_shape, self.update_score)
        self.preview = Preview()
 

    def update_score(self, score, level, lines):
        self.score.score = score
        self.score.level = level
        self.score.lines = lines


    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(random_shape())
        return next_shape


    def run(self):

        while True:
            
            for event in pygame.event.get():

                newState = self.state.handleEvents(event, self)
                if newState is not None:
                    self.state = newState
                    break
            
            self.display_surface.fill(NIGHT_RIDER)
            

            self.state.run(self)

            self.state.draw(self)

            updatedState = self.state.update(self)
            if updatedState is not None:
                self.state = updatedState

            # Update game
            pygame.display.update()
            self.clock.tick()

def random_shape():
    return choice(list(TETROMINOES.keys()))

if __name__ == '__main__':
    main = Main()
    main.run()
