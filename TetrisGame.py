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

        # Components
        self.game = Game()
        self.score = Score()
        self.preview = Preview()

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
            self.preview.run()

            # Update game
            pygame.display.update()
            self.clock.tick()
        


if __name__ == '__main__':
    main = Main()
    main.run()