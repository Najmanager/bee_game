import pygame, sys
from button import Button
from settings import *
from scores import Scores
from tests import *

class GameEndScreen:
    def __init__(self,score,username,result):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_image = pygame.image.load('../graphics/bg_images/intro_bg_2.jpeg').convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.bg_rect = pygame.Rect(0, 0, WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.5)
        self.bg_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 85)

        self.menu_button = Button(self.bg_rect.left + 150, self.bg_rect.bottom - 70,'MAIN MENU')
        self.scores_button = Button(self.bg_rect.right - 150, self.bg_rect.bottom - 70,'SCORES')

        self.score = score
        self.username = username
        self.result = result
        self.scores = Scores()

        self.buttons = [self.menu_button,self.scores_button]

    def draw_background(self):
        if self.result == 'win':
            message = 'YOU WON!'
        else:
            message = 'YOU LOST :('

        title = self.font.render(message, True, button_border_color)
        title_rect = title.get_rect(midtop=(WINDOW_WIDTH / 2, self.bg_rect.top + 50))

        score = self.font.render(f'SCORE: {self.score}', True, button_border_color)
        score_rect = score.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect.bottom + 50))

        if score_rect.width > self.bg_rect.width:
            self.bg_rect.width = score_rect.width + 20
            self.bg_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

        self.display_surface.blit(self.bg_image,(0,0))

        pygame.draw.rect(self.display_surface, button_bg_color, self.bg_rect)
        self.display_surface.blit(title, title_rect)
        self.display_surface.blit(score, score_rect)

    def pass_score(self):
        current_scores = self.scores.get_scores()
        current_scores.append((self.username,self.score))
        sorted_scores = self.scores.sort_scores(current_scores)
        try:
            sort_scores_test(sorted_scores)
            self.scores.write_scores(sorted_scores)
        except AssertionError:
            self.scores.write_scores(sorted(current_scores, key=lambda x: x[1], reverse=True))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            self.draw_background()

            hover = False

            for button in self.buttons:
                button.draw()
                pos = pygame.mouse.get_pos()
                if button.button.collidepoint(pos):
                    hover = True

            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.menu_button.action():
                return 'menu'
            if self.scores_button.action():
                return 'scores'

            pygame.display.update()