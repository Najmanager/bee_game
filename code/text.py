import pygame
from settings import *

class SmokeText:
    def __init__(self):
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 60)
        self.display_surface = pygame.display.get_surface()
        self.start_time = pygame.time.get_ticks()
        self.paused_time = 0  # Track total pause duration
        self.last_pause_start = None  # When the game was last paused

    def pause(self):
        self.last_pause_start = pygame.time.get_ticks()

    def unpause(self):
        if self.last_pause_start is not None:
            self.paused_time += pygame.time.get_ticks() - self.last_pause_start
            self.last_pause_start = None

    def display(self, game_paused):
        current_time = pygame.time.get_ticks()

        if game_paused and self.last_pause_start is None:
            self.pause()  # Ensure the pause time is recorded

        # Adjust the timer for paused time
        adjusted_start_time = self.start_time + self.paused_time
        time_left = smoke_timer - (current_time - adjusted_start_time)

        if time_left > 0 and not game_paused:
            # Convert remaining time to seconds
            seconds_left = time_left // 1000 + 1
            countdown_text = f"NEXT POISON CLOUD IN: {seconds_left}"

            if time_left < 750:
                return True

            # Render the countdown text
            text = self.font.render(countdown_text, True, text_color)
            text_rect = text.get_rect(center=(WINDOW_WIDTH / 2, 50))
            self.display_surface.blit(text, text_rect)
        else:
            self.start_time = pygame.time.get_ticks()  # Reset timer
            self.paused_time = 0  # Reset paused duration

class FlowersText:
    def __init__(self,player):
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 40)
        self.display_surface = pygame.display.get_surface()

        self.player = player

    def display_count(self,flowers_amount,amount_to_win):
        left_flowers_count = f"THERE ARE {flowers_amount} LEFT"
        text = self.font.render(left_flowers_count,True,button_bg_color)
        text_rect_1 = text.get_rect(topleft = (10,100))
        self.display_surface.blit(text,text_rect_1)

        flowers_to_win = f"YOU NEED {amount_to_win-self.player.collected} TO WIN"
        text = self.font.render(flowers_to_win, True, button_bg_color)
        text_rect_2 = text.get_rect(topleft=(10, text_rect_1.bottom+15))
        self.display_surface.blit(text, text_rect_2)

        collected_flowers = f"STORAGE: {self.player.storage}"
        text = self.font.render(collected_flowers, True, button_bg_color)
        text_rect_3 = text.get_rect(topleft=(10, text_rect_2.bottom+15))
        self.display_surface.blit(text, text_rect_3)

class SpeedText:
    def __init__(self,player):
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 40)
        self.display_surface = pygame.display.get_surface()

        self.player = player

    def display_speed(self):
        speed = f"SPEED: {int(self.player.speed*0.5)}%"
        text = self.font.render(speed,True,button_bg_color)
        text_rect = text.get_rect(topleft = (10,50))
        self.display_surface.blit(text,text_rect)

