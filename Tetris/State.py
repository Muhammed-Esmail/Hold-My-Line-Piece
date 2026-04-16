from settings import *

class State:
    def __init__(self):
        self.dark_overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.dark_overlay.set_alpha(100)
        self.dark_overlay.fill((0,0,0))
        self.font = pygame.font.Font(FONT_PATH, FONT_SIZE)

    def draw(self, window):
        pass 
    
    def run(self, window):
        pass

    def update(self, window):
        return None

    def handleEvents(self, event, window):
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()


class MainMenu(State):
    
    main_menu: pygame.Rect
    start_btn: pygame.Rect
    quit_btn: pygame.Rect

    def __init__(self) -> None:
        super().__init__()


        self.main_menu : pygame.Rect = pygame.Rect(MAIN_GAME_MENU_X, MAIN_GAME_MENU_Y, MAIN_GAME_MENU_WIDTH, MAIN_GAME_MENU_HEIGHT)
        
        (centerx, centery) = (self.main_menu.centerx, self.main_menu.centery)
        
        btn_x = centerx - (MAIN_GAME_BUTTON_WIDTH) / 2

        self.start_btn : pygame.Rect = pygame.Rect(
                btn_x, 
                centery + MAIN_GAME_BUTTON_MARGIN*2,
                MAIN_GAME_BUTTON_WIDTH, 
                MAIN_GAME_BUTTON_HEIGHT)

        self.quit_btn : pygame.Rect = pygame.Rect(
                btn_x, 
                centery + MAIN_GAME_BUTTON_MARGIN*3 + MAIN_GAME_BUTTON_HEIGHT,
                MAIN_GAME_BUTTON_WIDTH, 
                MAIN_GAME_BUTTON_HEIGHT)
        

    def draw(self, window) -> None:
        super().draw(window)
        
        # Darken background with overlay
        window.display_surface.blit(self.dark_overlay, (0,0))

        # Show menu
        pygame.draw.rect(window.display_surface, NIGHT_RIDER ,self.main_menu)
        
        # 'HOLD MY LINE PIECE' text
        title_surf = self.font.render('HOLD MY LINE PIECE', True, WHITE)
        title_rect = title_surf.get_rect(midtop = (self.main_menu.centerx, self.main_menu.top + 20))
        window.display_surface.blit(title_surf, title_rect)
       
        # Show buttons
        for rect, text in [ (self.start_btn, 'START'), (self.quit_btn, 'QUIT')]:
            # Change color on hover
            color = GOLD if rect.collidepoint(pygame.mouse.get_pos()) else WHITE
            pygame.draw.rect(window.display_surface, color, rect, 2)
           
            font = pygame.font.Font(FONT_PATH, BUTTON_FONT_SIZE)
            
            btn_surf = font.render(text, True, color)
            btn_rect = btn_surf.get_rect(center = rect.center)
            window.display_surface.blit(btn_surf, btn_rect)


    def handleEvents(self, event, window) -> State | None:
        super().handleEvents(event, window)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Clicking on "START"
            if self.start_btn.collidepoint(event.pos):
                window.new_game()
                return Playing()
            # Clicking on "QUIT"
            if self.quit_btn.collidepoint(event.pos):
                pygame.quit()
                exit()

        return None


class Playing(State):
    def __init__(self):
        super().__init__()


    def run(self, window) -> None:
        window.score.run()
        window.preview.run(window.next_shapes)
        window.game.run()

        
    def update(self, window):
        if window.game.is_game_over:
            return GameOver()
        return None


    def handleEvents(self, event, window) -> State | None:
        super().handleEvents(event, window)

        return None


class GameOver(State):

    game_over_menu: pygame.Rect
    main_menu_btn: pygame.Rect
    restart_btn: pygame.Rect
    quit_btn: pygame.Rect

    def __init__(self):
        super().__init__()

        self.game_over_menu: pygame.Rect = pygame.Rect(GAME_OVER_MENU_X, GAME_OVER_MENU_Y, GAME_OVER_MENU_WIDTH, GAME_OVER_MENU_HEIGHT)

        (centerx, centery) = (self.game_over_menu.centerx, self.game_over_menu.centery)
        
        self.main_menu_btn: pygame.Rect = pygame.Rect(
                centerx - GAME_OVER_BUTTON_MARGIN - GAME_OVER_BUTTON_WIDTH, 
                centery + GAME_OVER_BUTTON_MARGIN * 2,
                GAME_OVER_BUTTON_WIDTH, 
                GAME_OVER_BUTTON_HEIGHT)

        self.restart_btn: pygame.Rect = pygame.Rect(
                centerx + GAME_OVER_BUTTON_MARGIN, 
                centery + GAME_OVER_BUTTON_MARGIN * 2,
                GAME_OVER_BUTTON_WIDTH, 
                GAME_OVER_BUTTON_HEIGHT)

        self.quit_btn: pygame.Rect = pygame.Rect(
                centerx - (GAME_OVER_BUTTON_WIDTH // 2), 
                centery + GAME_OVER_BUTTON_MARGIN * 3 + GAME_OVER_BUTTON_HEIGHT,
                GAME_OVER_BUTTON_WIDTH, 
                GAME_OVER_BUTTON_HEIGHT)


    def draw(self, window):
        # Darken background with overlay
        window.display_surface.blit(self.dark_overlay, (0,0))

        # Show menu
        pygame.draw.rect(window.display_surface, NIGHT_RIDER ,self.game_over_menu)
        
        # 'GAME OVER' text
        title_surf = self.font.render('GAME OVER', True, WHITE)
        title_rect = title_surf.get_rect(midtop = (self.game_over_menu.centerx, self.game_over_menu.top + 20))
        window.display_surface.blit(title_surf, title_rect)
       
        # Display final state
        stats_text = f"Score: {window.score.score} | Level: {window.score.level}"
        stats_surf = self.font.render(stats_text, True, GRAY)
        stats_rect = stats_surf.get_rect(center = (self.game_over_menu.centerx, self.game_over_menu.centery - 20))
        window.display_surface.blit(stats_surf, stats_rect)

        # Show buttons
        for rect, text in [(self.main_menu_btn, 'MAIN MENU'),(self.restart_btn, 'RESTART'), (self.quit_btn, 'QUIT')]:
            # Change color on hover
            color = GOLD if rect.collidepoint(pygame.mouse.get_pos()) else WHITE
            pygame.draw.rect(window.display_surface, color, rect, 2)
           
            font = pygame.font.Font(FONT_PATH, BUTTON_FONT_SIZE)
            
            btn_surf = font.render(text, True, color)
            btn_rect = btn_surf.get_rect(center = rect.center)
            window.display_surface.blit(btn_surf, btn_rect)


    def run(self, window) -> None:
        window.score.run()
        window.preview.run(window.next_shapes)
        
        window.game.draw()


    def handleEvents(self, event, window) -> State | None:
        super().handleEvents(event, window)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_btn.collidepoint(event.pos):
                window.new_game()
                return Playing()
            
            if self.main_menu_btn.collidepoint(event.pos):
                return MainMenu()

            if self.quit_btn.collidepoint(event.pos):
                pygame.quit()
                exit()

        return None