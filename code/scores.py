import pygame, sys
from button import Button
from settings import *

class Scores:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.menu_bg = pygame.image.load('../graphics/bg_images/scores_bg.jpeg')
        self.menu_bg = pygame.transform.scale(self.menu_bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 120)

        self.return_button = Button(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 75,'RETURN TO MENU')

        self.buttons = [self.return_button]

    def get_scores(self):
        scores = []
        with open('best_scores.txt', 'r') as f:
            for line in f:
                user = line.split()[1]
                score = line.split()[2]
                scores.append(tuple([user, int(score)]))  # appends a tuple with username and score(int for sorting)

        return scores

    def sort_scores(self,scores):
        for i in range(len(scores)):
            for j in range(len(scores) - i - 1):
                if scores[j][1] < scores[j + 1][1]:  # compares scores from tuples
                    scores[j], scores[j + 1] = scores[j + 1], scores[j]

        return scores

    def write_scores(self,scores):

        with open('best_scores.txt', 'w') as f:
            i = 1  # indexing scores
            for user, score in scores:
                f.write(f'{i}. {user} {score}\n')
                if i == 5:  # checks if there are already 5 scores
                    break
                else:
                    i += 1

    def display_scores(self,scores):
        y = 200
        font = pygame.font.Font('../graphics/Apocalypse.ttf', 75)
        for index, data in enumerate(scores):
            user, score = data

            text = font.render(f"{index+1}. {user} {score}", True, button_border_color)
            text_rect = text.get_rect(center = (WINDOW_WIDTH / 2,y))
            y+=85
            pygame.draw.rect(self.display_surface, button_border_color, text_rect.inflate(15,15))
            pygame.draw.rect(self.display_surface, button_bg_color, text_rect.inflate(10,10))

            self.display_surface.blit(text, text_rect)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            title = self.font.render('BEST SCORES',True, button_border_color)
            title_rect = title.get_rect(center = (WINDOW_WIDTH / 2, 85))

            self.display_surface.blit(self.menu_bg, (0, 0))
            self.display_surface.blit(title, title_rect)

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

            if self.return_button.action():
                return 'menu'

            initial_scores = self.get_scores()

            self.display_scores(initial_scores)

            self.clock.tick(60)
            pygame.display.update()