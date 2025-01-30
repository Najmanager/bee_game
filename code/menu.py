import pygame
from button import Button
from settings import *

class Menu:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('The last bee')
        self.clock = pygame.time.Clock()
        self.menu_bg = pygame.image.load('../graphics/bg_images/menu_bg.jpeg')
        self.menu_bg = pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 120)

        x = 175
        self.play_button = Button(x,175,'PLAY')
        self.scores_button = Button(x,self.play_button.button.y+125,'SCORES')
        self.quit_button = Button(x,self.scores_button.button.y+125,'QUIT')

        self.buttons = [self.play_button,self.scores_button,self.quit_button]

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            title = self.font.render('THE LAST BEE',True,title_color)
            title_rect = title.get_rect(center = (WINDOW_WIDTH / 2, 85))

            self.display_surface.blit(self.menu_bg, (0, 0))
            self.display_surface.blit(title, title_rect)

            hover = False

            for button in self.buttons:
                pos = pygame.mouse.get_pos()
                button.draw()
                if button.button.collidepoint(pos):
                    hover = True

            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.play_button.action():
                return 'intro'

            if self.scores_button.action():
               return 'scores'

            if self.quit_button.action():
                return 'exit'

            pygame.display.update()
