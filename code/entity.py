import pygame, sys
from pygame.math import Vector2 as vector
from settings import *
from os import walk

class Entity(pygame.sprite.Sprite):
    def __init__(self,pos,groups,collision_sprites,path):
        super().__init__(groups)
        self.import_assets(path)

        self.frame_index = 0
        self.status = 'right_idle'

        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-self.rect.width / 1.5 ,-self.rect.height / 1.5)
        self.collision_sprites = collision_sprites

        self.mask = pygame.mask.from_surface(self.image)

        self.pos = vector(self.rect.center)
        self.direction = vector()
        self.health = 10
        self.hit_time = None

        self.attacking = False

        self.is_vulnerable = True

        self.display_surface = pygame.display.get_surface()

    def import_assets(self,path):
        self.animations = {}

        for index, tuple in enumerate(walk(path)):
            if index == 0:
                for folder in tuple[1]:
                    self.animations[folder] = []
            else:
                for file_name in sorted(tuple[2], key = lambda file_name: file_name.split('.')[0]):
                    xyz = tuple[0].split('/')[-1]
                    file_path = path +'/' + xyz + '/' + file_name
                    image = pygame.image.load(file_path).convert_alpha()
                    image = pygame.transform.scale_by(image,3)

                    self.animations[xyz].append(image)

    def move(self,dt):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self,direction):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > MAP_WIDTH:
            self.pos.x = MAP_WIDTH

        if self.pos.y < 10:
            self.pos.y = 10
        if self.pos.y > MAP_HEIGHT:
            self.pos.y = MAP_HEIGHT

        for sprite in self.collision_sprites.sprites():
            if sprite.hitbox.colliderect(self.hitbox):
                if direction == 'horizontal':
                    if self.direction.x > 0:  # moving right
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:  # moving left
                        self.hitbox.left = sprite.hitbox.right
                    self.rect.centerx = self.hitbox.centerx
                    self.pos.x = self.hitbox.centerx
                else:
                    if self.direction.y > 0:  # moving down
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0:  # moving up
                        self.hitbox.top = sprite.hitbox.bottom
                    self.rect.centery = self.hitbox.centery
                    self.pos.y = self.hitbox.centery
