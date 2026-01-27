from settings import *

class Score:
    def __init__(self):
        self.surface = pygame.Surface((SIDEBAR_WIDTH, GAME_HEIGHT * SCORE_HEIGHT_FRACTION - PADDING))
        self.rect = self.surface.get_rect(bottomright = (WINDOW_WIDTH - PADDING, WINDOW_HEIGHT - PADDING))
        self.display_surface = pygame.display.get_surface()
       
        # font
        self.font = pygame.font.Font(join('..','graphics',FONT), FONT_SIZE)
    
        # increment (dividing into 3 pieces : Score, Level, Cleared Lines)
        self.increment_height = self.surface.get_height() / 3
        
        # data
        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, pos, text):
        text_surface = self.font.render(f"{text[0]} : {text[1]}", True, FONT_COLOR)
        text_rect = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):
        
        self.surface.fill(SCORE_COLOR)
        
        for i, text in enumerate([('Score', self.score), ('Level', self.level), ('Lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height * (i + 0.5)
            
            self.display_text((x,y), text)
            
                        

        self.display_surface.blit(self.surface, self.rect)

        pygame.draw.rect(
            self.display_surface, 
            WINDOW_BORDER_COLOR,
            self.rect,
            2, 2
        )

