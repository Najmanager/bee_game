import pygame
from settings import *
from pygame.math import Vector2 as vector

class Sprite(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 1.5)

        self.mask = pygame.mask.from_surface(self.image)

class Base(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,player):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 2, -self.rect.height / 1.25)

        self.font = pygame.font.Font(None, 25)
        self.display_surface = pygame.display.get_surface()

        self.empty_radius = 150
        self.player = player

        self.mask = pygame.mask.from_surface(self.image)

    def display_message(self):
        text = self.font.render("PRESS E/P TO EMPTY STORAGE", True, text_color)
        text_rect = text.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 10))
        self.display_surface.blit(text,text_rect)

    def empty_equipment(self):
        base_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - base_pos).magnitude()

        if distance < self.empty_radius and self.player.storage > 0:
            self.display_message()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] or keys[pygame.K_p]:
                self.player.storage = 0

class Flower(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups,player):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.player = player

        self.collect_radius = 60

        self.font = pygame.font.Font(None, 25)

        self.display_surface = pygame.display.get_surface()

    def display_message(self,offset):
        text = self.font.render("PRESS E/P TO COLLECT", True, text_color)
        text_rect = text.get_rect(center = (self.rect.centerx, self.rect.centery - 50))

        text_rect.center -= offset

        self.display_surface.blit(text, text_rect)

    def collect(self,offset):
        flower_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - flower_pos).magnitude()

        if distance < self.collect_radius:
            self.display_message(offset)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_e] or keys[pygame.K_p]:
                self.kill()
                self.player.collected += 1
                self.player.storage += 1

