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
        
        # state
        self.state = 0 # 0 = Main Menu, 1 = Playing, 2 = Game over

        # shapes
        self.next_shapes = [random_shape() for shape in range(3)]
        # print(self.next_shapes)

        # Main game menu
        self.main_menu = pygame.Rect(MAIN_GAME_MENU_X, MAIN_GAME_MENU_Y, MAIN_GAME_MENU_WIDTH, MAIN_GAME_MENU_HEIGHT)
        (centerx, centery) = (self.main_menu.centerx, self.main_menu.centery)
        
        btn_x = centerx - (MAIN_GAME_BUTTON_WIDTH) / 2

        self.start_btn = pygame.Rect(
                btn_x, 
                centery + MAIN_GAME_BUTTON_MARGIN*2,
                MAIN_GAME_BUTTON_WIDTH, 
                MAIN_GAME_BUTTON_HEIGHT)

        self.quit_btn1 = pygame.Rect(
                btn_x, 
                centery + MAIN_GAME_BUTTON_MARGIN*3 + MAIN_GAME_BUTTON_HEIGHT,
                MAIN_GAME_BUTTON_WIDTH, 
                MAIN_GAME_BUTTON_HEIGHT)
        


        # Game Over
        self.game_over_menu = pygame.Rect(GAME_OVER_MENU_X, GAME_OVER_MENU_Y, GAME_OVER_MENU_WIDTH, GAME_OVER_MENU_HEIGHT)
        (centerx, centery) = (self.game_over_menu.centerx, self.game_over_menu.centery)
        
        self.main_menu_btn = pygame.Rect(
                centerx - GAME_OVER_BUTTON_MARGIN - GAME_OVER_BUTTON_WIDTH, 
                centery + GAME_OVER_BUTTON_MARGIN * 2,
                GAME_OVER_BUTTON_WIDTH, 
                GAME_OVER_BUTTON_HEIGHT)

        self.restart_btn = pygame.Rect(
                centerx + GAME_OVER_BUTTON_MARGIN, 
                centery + GAME_OVER_BUTTON_MARGIN * 2,
                GAME_OVER_BUTTON_WIDTH, 
                GAME_OVER_BUTTON_HEIGHT)

        self.quit_btn2 = pygame.Rect(
                centerx - (GAME_OVER_BUTTON_WIDTH // 2), 
                centery + GAME_OVER_BUTTON_MARGIN * 3 + GAME_OVER_BUTTON_HEIGHT,
                GAME_OVER_BUTTON_WIDTH, 
                GAME_OVER_BUTTON_HEIGHT)


        
        self.dark_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.dark_overlay.set_alpha(100)
        self.dark_overlay.fill((0,0,0))
        self.font = pygame.font.Font(join('..','graphics',FONT), FONT_SIZE)
    

        # New Game
        self.new_game()

    def new_game(self):
        # Components    
        self.score = Score()
        self.game = Game(self.get_next_shape, self.update_score)
        self.preview = Preview()
 
    def main_menu_screen(self):
        # Darken background with overlay
        self.display_surface.blit(self.dark_overlay, (0,0))

        # Show menu
        pygame.draw.rect(self.display_surface, NIGHT_RIDER ,self.main_menu)
        
         # 'HOLD MY LINE PIECE' text
        title_surf = self.font.render('HOLD MY LINE PIECE', True, WHITE)
        title_rect = title_surf.get_rect(midtop = (self.main_menu.centerx, self.main_menu.top + 20))
        self.display_surface.blit(title_surf, title_rect)
       
        # Show buttons
        for rect, text in [ (self.start_btn, 'START'), (self.quit_btn1, 'QUIT')]:
            # Change color on hover
            color = GOLD if rect.collidepoint(pygame.mouse.get_pos()) else WHITE
            pygame.draw.rect(self.display_surface, color, rect, 2)
           
            font = pygame.font.Font(join('..','graphics',FONT), BUTTON_FONT_SIZE)
            
            btn_surf = font.render(text, True, color)
            btn_rect = btn_surf.get_rect(center = rect.center)
            self.display_surface.blit(btn_surf, btn_rect)


        

    def game_over_screen(self):
        # Darken background with overlay
        self.display_surface.blit(self.dark_overlay, (0,0))

        # Show menu
        pygame.draw.rect(self.display_surface, NIGHT_RIDER ,self.game_over_menu)
        
        # 'GAME OVER' text
        title_surf = self.font.render('GAME OVER', True, WHITE)
        title_rect = title_surf.get_rect(midtop = (self.game_over_menu.centerx, self.game_over_menu.top + 20))
        self.display_surface.blit(title_surf, title_rect)
       
        # Display final state
        stats_text = f"Score: {self.score.score} | Level: {self.score.level}"
        stats_surf = self.font.render(stats_text, True, GRAY)
        stats_rect = stats_surf.get_rect(center = (self.game_over_menu.centerx, self.game_over_menu.centery - 20))
        self.display_surface.blit(stats_surf, stats_rect)

        # Show buttons
        for rect, text in [(self.main_menu_btn, 'MAIN MENU'),(self.restart_btn, 'RESTART'), (self.quit_btn2, 'QUIT')]:
            # Change color on hover
            color = GOLD if rect.collidepoint(pygame.mouse.get_pos()) else WHITE
            pygame.draw.rect(self.display_surface, color, rect, 2)
           
            font = pygame.font.Font(join('..','graphics',FONT), BUTTON_FONT_SIZE)
            
            btn_surf = font.render(text, True, color)
            btn_rect = btn_surf.get_rect(center = rect.center)
            self.display_surface.blit(btn_surf, btn_rect)

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
                # Handle closing the game
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if self.state == 0 and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_btn.collidepoint(event.pos):
                        self.new_game()
                        self.state = 1
                    
                    if self.quit_btn1.collidepoint(event.pos):
                        pygame.quit()
                        exit()


                if self.state == 2 and event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_btn.collidepoint(event.pos):
                        self.state = 1
                    
                    if self.main_menu_btn.collidepoint(event.pos):
                        self.state = 0

                    if self.quit_btn2.collidepoint(event.pos):
                        pygame.quit()
                        exit()
           
                    self.new_game()
            
            # display
            self.display_surface.fill(NIGHT_RIDER)
            

            if self.game.is_game_over:
                self.state = 2

            if self.state == 0:
                self.main_menu_screen()
            elif self.state == 1:
                self.score.run()
                self.preview.run(self.next_shapes)
                self.game.run()
            elif self.state == 2:
                self.score.run()
                self.preview.run(self.next_shapes)
                
                self.game.draw()
                self.game_over_screen()
            
            # Update game
            pygame.display.update()
            self.clock.tick()

def random_shape():
    return choice(list(TETROMINOES.keys()))

if __name__ == '__main__':
    main = Main()
    main.run()
