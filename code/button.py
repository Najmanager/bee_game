import pygame
from settings import *

class Button:
    def __init__(self, x, y,text):
        self.button = pygame.Rect(x,y,200,50)

        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 50)
        self.text = text
        self.adjust_x = x
        self.adjust_y = y

        self.mouse_held = False

        self.button.center = (self.adjust_x, self.adjust_y)

        self.display_surface = pygame.display.get_surface()

    def draw(self):
        border_width = 5

        text = self.font.render(self.text, True, title_color)
        text_rect = text.get_rect(center=(self.button.center))

        if text_rect.width > self.button.width:
            self.button.width = text_rect.width + 20
            self.button.center = (self.adjust_x, self.adjust_y)

        pygame.draw.rect(self.display_surface, button_border_color, self.button.inflate(border_width * 2, border_width * 2))
        pygame.draw.rect(self.display_surface, button_bg_color, self.button)
        self.display_surface.blit(text, text_rect)

    def action(self):
        mouse_pressed = pygame.mouse.get_pressed()[0]
        mouse_pos = pygame.mouse.get_pos()
        action = False

        # Detect mouse release
        if self.mouse_held and not mouse_pressed:
            if self.button.collidepoint(mouse_pos):
                action = True
            self.mouse_held = False

        if mouse_pressed:
            self.mouse_held = True

        return action