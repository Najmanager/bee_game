import pygame, sys
from pygame.math import Vector2 as vector
from settings import *
from entity import Entity
from math import sin

class Player(Entity):
    def __init__(self,pos,groups,collision_sprites,path):
        super().__init__(pos,groups,collision_sprites,path)

        self.collected = 0
        self.storage = 0

        self.max_health = 100
        self.current_health = self.max_health
        self.health_bar_length = 200
        self.max_speed = 200

        self.health_ratio = self.max_health / self.health_bar_length
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 40)

        self.is_vulnerable = True

    def wave_walue(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else:
            return 0

    def blink(self):
        if not self.is_vulnerable:
            alpha = self.wave_walue()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def damage(self,amount):
        if self.is_vulnerable:
            self.current_health -= amount
            self.is_vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def vulnerability_timer(self):
        if not self.is_vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time > 500:
                self.is_vulnerable = True

    def input(self,game_paued):
        keys = pygame.key.get_pressed()

        if not game_paued:
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0
        else:
            self.direction = vector()

    def animate(self,dt):
        if self.direction == vector(0,0):
            self.status = self.status.split('_')[0] + '_idle'

        current_animation = self.animations[self.status]

        if '_idle' in self.status:
            self.frame_index += 7 * dt
        else:
            self.frame_index += 10 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0

        self.image = current_animation[int(self.frame_index)]

    def health_bar(self):
        x = 10
        y = 10
        text = self.font.render('HEALTH:', True, button_bg_color)
        text_rect = text.get_rect(topleft=(x, y))

        self.display_surface.blit(text,text_rect)
        pygame.draw.rect(self.display_surface, (255,0,0), (text_rect.right+10,text_rect.height/2-y,self.current_health/self.health_ratio,25))
        pygame.draw.rect(self.display_surface, (255,255,255), (text_rect.right+10,text_rect.height/2-y,self.health_bar_length,25),4)

    def update(self,dt):
        self.speed = self.max_speed - 10 * self.storage
        self.blink()
        self.animate(dt)
        self.move(dt)

        self.vulnerability_timer()
