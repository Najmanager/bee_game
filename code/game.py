import pygame, sys, random
from settings import *
from pygame.math import Vector2 as vector
from pytmx.util_pygame import load_pygame
from sprite import *
from player import Player
from text import *
from enemy import Enemy
from button import Button
from end_screen import GameEndScreen
from random import randint

class AllSprites(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.offset = vector()
        self.display_surface = pygame.display.get_surface()
        self.bg = pygame.image.load('../graphics/bg_images/game_bg.png').convert()

    def draw(self, player):
        max_offset_x = self.bg.get_width() - WINDOW_WIDTH
        max_offset_y = self.bg.get_height() - WINDOW_HEIGHT

        self.offset.x = player.rect.centerx - WINDOW_WIDTH / 2
        self.offset.y = player.rect.centery - WINDOW_HEIGHT / 2

        self.offset.x = max(0, min(self.offset.x, max_offset_x))
        self.offset.y = max(0, min(self.offset.y, max_offset_y))

        self.display_surface.blit(self.bg, -self.offset)

        self.sorted_sprites = sorted(self.sprites(), key=lambda sprite: sprite.rect.centery)

        for sprite in self.sorted_sprites:
            offset_rect = sprite.image.get_rect(center=sprite.rect.center)
            offset_rect.center -= self.offset
            self.display_surface.blit(sprite.image, offset_rect)

class Game:
    def __init__(self,username):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('The last bee')
        self.clock = pygame.time.Clock()
        self.smoke_image = pygame.image.load('../graphics/smoke.jpg').convert()
        self.smoke_image = pygame.transform.scale(self.smoke_image,(WINDOW_WIDTH,WINDOW_HEIGHT))

        self.username = username
        self.max_score = 1000

        self.all_sprites = AllSprites()

        self.collision_sprites = pygame.sprite.Group()
        self.asylum_sprites = pygame.sprite.Group()
        self.flower_sprites = pygame.sprite.Group()
        self.enemies_sprites = pygame.sprite.Group()
        self.hurtful_sprites = pygame.sprite.Group()

        self.smoke_active = False  # State to track if smoke is active
        self.do_damage = False

        self.setup()

        self.smoke_time = SmokeText()
        self.flowers_text = FlowersText(self.player)
        self.speed_text = SpeedText(self.player)
        self.amount_to_win = int(len(self.flower_sprites.sprites())*0.7)

        self.pause_button = Button(WINDOW_WIDTH-150, 50, 'PAUSE')

        self.buttons = [self.pause_button]

        self.game_paused = False
        self.hurt = False

    def setup(self):
        tmx_map = load_pygame('../data/map-1.tmx')
        for x, y, surf in tmx_map.get_layer_by_name('Safe').tiles():
            Sprite((x * 32, y * 32), surf, [self.all_sprites,self.asylum_sprites])
        for obj in tmx_map.get_layer_by_name('Objects'):
            Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])
        for obj in tmx_map.get_layer_by_name('Hurtful objects'):
            hurtful_object = Sprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites, self.hurtful_sprites])
            hurtful_object.hitbox.y = -hurtful_object.rect.height
        for obj in tmx_map.get_layer_by_name('Entities'):
            if obj.name == 'Player':
                self.player = Player((obj.x, obj.y), self.all_sprites, self.collision_sprites,'../graphics/player')
            if obj.name == 'Enemy':
                self.enemy = Enemy((obj.x, obj.y), [self.all_sprites,self.enemies_sprites], [self.collision_sprites,self.asylum_sprites, self.enemies_sprites], '../graphics/monster', self.player)
        for obj in tmx_map.get_layer_by_name('Flowers'):
            self.flower = Flower((obj.x,obj.y), obj.image, [self.all_sprites,self.flower_sprites], self.player)
        for obj in tmx_map.get_layer_by_name('Home base'):
            self.base = Base((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites],self.player)

    def pause(self):
        self.smoke_time.pause()  # Pause the smoke timer

        resume_button = Button(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 'RESUME')
        menu_button = Button(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 100, 'MAIN MENU')
        font = pygame.font.Font('../graphics/Apocalypse.ttf', 100)
        pause_text = font.render("PAUSE MENU", True, text_color)
        pause_text_rect = pause_text.get_rect(center=(WINDOW_WIDTH / 2, 200))

        while self.game_paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            self.enemy_attack()
            self.can_move()
            self.display_surface.blit(pause_text, pause_text_rect)
            resume_button.draw()
            menu_button.draw()

            if resume_button.action():
                self.game_paused = False
                self.smoke_time.unpause()  # Unpause the smoke timer
            if menu_button.action():
                return 'menu'

            pygame.display.update()

    def check_smoke_damage(self):
        max_top = MAP_HEIGHT
        max_left = MAP_WIDTH
        max_right = 0
        max_bottom = 0
        for sprite in self.asylum_sprites.sprites():
            if sprite.rect.top < max_top:
                max_top = sprite.rect.top
            if sprite.rect.bottom > max_bottom:
                max_bottom = sprite.rect.bottom
            if sprite.rect.left < max_left:
                max_left = sprite.rect.left
            if sprite.rect.right > max_right:
                max_right = sprite.rect.right
        if self.player.hitbox.bottom > max_bottom or self.player.hitbox.top < max_top or self.player.hitbox.left < max_left or self.player.hitbox.right > max_right:
            self.hurt = True

    def count_score(self):
        self.score = self.max_score
        self.score -= int(pygame.time.get_ticks() / 120)

    def enemy_attack(self):
        for enemy in self.enemies_sprites.sprites():
            enemy.walk_to_player(self.game_paused)

    def can_move(self):
        self.player.input(self.game_paused)

    def update(self,dt):
        self.all_sprites.update(dt)
        self.enemy_attack()
        self.can_move()
        self.all_sprites.draw(self.player)
        self.smoke_time.display(self.game_paused)
        self.flowers_left = len(self.flower_sprites.sprites())
        self.flowers_text.display_count(self.flowers_left,self.amount_to_win)
        self.speed_text.display_speed()
        self.player.health_bar()
        self.base.empty_equipment()
        self.count_score()


        for flower in self.flower_sprites.sprites():
            flower.collect(self.all_sprites.offset)

        if pygame.sprite.spritecollide(self.player, self.enemies_sprites, False, pygame.sprite.collide_mask):
            self.player.damage(10)

        if pygame.sprite.spritecollide(self.player, self.hurtful_sprites, False, pygame.sprite.collide_mask):
            self.player.damage(10)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            # Game logic
            dt = self.clock.tick() / 1000

            if self.smoke_time.display(self.game_paused):
                self.display_surface.blit(self.smoke_image, (0, 0))
                self.smoke_active = True
                self.do_damage = True
            else:
                self.smoke_active = False

            if not self.smoke_active and not self.game_paused:
                if self.do_damage:
                    self.check_smoke_damage()
                    random_sprite = random.choice(self.flower_sprites.sprites())
                    random_sprite.kill()
                    self.do_damage = False

                if self.hurt:
                    self.player.damage(20)
                    self.hurt = False

                self.update(dt)
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

                if self.pause_button.action():
                    self.game_paused = True
                    if self.pause() == 'exit':
                        return 'exit'
                    elif self.pause() == 'menu':
                        return 'menu'

                if self.player.collected == self.amount_to_win:
                    score = int(abs(self.score)*self.player.collected*1.5)
                    screen = GameEndScreen(score,self.username, 'win')
                    status = screen.run()
                    screen.pass_score()
                    return status

                if self.amount_to_win > self.player.collected + self.flowers_left or self.player.current_health <= 0:
                    score = int(abs(self.score/2)*self.player.collected)
                    screen = GameEndScreen(score,self.username, 'lost')
                    status = screen.run()
                    screen.pass_score()
                    return status

            pygame.display.update()

if __name__ == '__main__':
    game = Game('ss')
    game.run()