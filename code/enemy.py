import pygame
from entity import Entity
from settings import *
from pygame.math import Vector2 as vector

class Enemy(Entity):
    def __init__(self,pos,groups,collision_sprites,path,player):
        super().__init__(pos,groups,collision_sprites,path)

        self.player = player

        self.speed = 140
        self.notice_radius = 700
        self.walk_radius = 400
        self.attack_radius = 20
        self.hitbox = self.rect.inflate(-self.rect.width / 1.2, -self.rect.height / 1.2)

    def get_player_distance_direction(self):
        enemy_pos = vector(self.rect.center)
        player_pos = vector(self.player.rect.center)
        distance = (player_pos - enemy_pos).magnitude()

        if distance != 0:
            direction = (player_pos - enemy_pos).normalize()
        else:
            direction = vector()

        return (distance, direction)

    def face_player(self):
        distance, direction = self.get_player_distance_direction()
        if distance < self.notice_radius:
            if -0.5 < direction.y < 0.5:
                if direction.x < 0:
                    self.status = 'left_idle'
                elif direction.x > 0:
                    self.status = 'right_idle'
            else:
                if direction.y < 0:
                    self.status = 'up_idle'
                else:
                    self.status = 'down_idle'

    def attack(self):
        distance = self.get_player_distance_direction()[0]
        if distance < self.attack_radius and not self.attacking:
            self.attacking = True
            self.frame_index = 0

        if self.attacking:
            self.status = self.status.split('_')[0] + '_attack'

    def walk_to_player(self,game_paused):
        distance, direction = self.get_player_distance_direction()
        if self.attack_radius < distance < self.walk_radius and not game_paused:
            self.direction = direction
            self.status = self.status.split('_')[0]
        else:
            self.direction = vector()

    def animate(self, dt):
        current_animation = self.animations[self.status]

        self.frame_index += 7 * dt

        if self.frame_index >= len(current_animation):
            self.frame_index = 0
            if self.attacking:
                self.attacking = False

        self.image = current_animation[int(self.frame_index)]
        self.mask = pygame.mask.from_surface(self.image)

    def collision(self,direction):
        if self.pos.x < 0:
            self.pos.x = 0
        if self.pos.x > MAP_WIDTH:
            self.pos.x = MAP_WIDTH

        if self.pos.y < 10:
            self.pos.y = 10
        if self.pos.y > MAP_HEIGHT:
            self.pos.y = MAP_HEIGHT

        for sprites in self.collision_sprites:
            for sprite in sprites.sprites():
                if sprite == self:  # Skip self-collision
                    continue

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

    def update(self,dt):
        self.face_player()
        self.attack()

        self.move(dt)
        self.animate(dt)
