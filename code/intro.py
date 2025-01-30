import pygame, sys
import pygame_gui
from settings import *
from button import Button

class Intro:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.backgrounds = [pygame.transform.scale(pygame.image.load(f'../graphics/bg_images/intro_bg_{i}.jpeg'),(WINDOW_WIDTH, WINDOW_HEIGHT)) for i in range(1, 4)]
        self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 65)

        self.flower_image = pygame.image.load('../graphics/objects/Yellow_Flower.png')

        self.back_button = Button(150, WINDOW_HEIGHT - 100,'< BACK')
        self.next_button = Button(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100,'NEXT >')
        self.play_button = Button(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 100,'PLAY')

        self.skip_button = Button(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 180,'SKIP >>')

        self.theme = {
            "text_entry_line": {
                "colours": {
                    "dark_bg": '#C4BD80',
                    "normal_text": '#3B352A'
                },
                "font": {
                    "size": 50
                }
            }
        }

        self.manager = pygame_gui.UIManager((WINDOW_WIDTH, WINDOW_HEIGHT), self.theme)
        text_input_rect = pygame.Rect((WINDOW_WIDTH / 2 + 50, WINDOW_HEIGHT / 2), (400, 100))
        text_input_rect.center = (WINDOW_WIDTH / 2 + 250, WINDOW_HEIGHT / 2)
        text_input = pygame_gui.elements.UITextEntryLine(text_input_rect, self.manager, None, None,'#username_entry')

        text_input.set_text_length_limit(15)

    def intro_page_1(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 45)

            message_1 = "THE WORLD IS CHANGED."
            message_2 = "THE FLOWERS ARE GONE, AND LIFE FADES WITH THEM."
            message_3 = "YOU ARE THE LAST OF YOUR KIND, A LONE BEE IN A DYING WORLD."
            message_4 = "YOUR MISSION IS SIMPLE – GATHER WHAT FEW FLOWERS REMAIN"
            message_5 = "AND AWAKE THE EARTH’S LIFEFORCE"

            lineheight = 15

            text_1 = self.font.render(message_1, True, button_border_color)
            title_rect_1 = text_1.get_rect(midtop=(WINDOW_WIDTH / 2, 100))
            text_2 = self.font.render(message_2, True, button_border_color)
            title_rect_2 = text_2.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_1.bottom + lineheight))
            text_3 = self.font.render(message_3, True, button_border_color)
            title_rect_3 = text_3.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_2.bottom + lineheight))
            text_4 = self.font.render(message_4, True, button_border_color)
            title_rect_4 = text_4.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_3.bottom + lineheight))
            text_5 = self.font.render(message_5, True, button_border_color)
            title_rect_5 = text_5.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_4.bottom + lineheight))

            all_title_rects = [title_rect_1,title_rect_2,title_rect_3,title_rect_4,title_rect_5]
            self.display_surface.blit(self.backgrounds[0], (0, 0))
            buttons = [self.next_button,self.skip_button]
            hover = False

            bg_rect = pygame.Rect(WINDOW_WIDTH / 2,WINDOW_HEIGHT / 2,0,0)
            bg_rect = bg_rect.unionall(all_title_rects)

            pygame.draw.rect(self.display_surface, button_border_color, bg_rect.inflate(10, 10))
            pygame.draw.rect(self.display_surface, button_bg_color, bg_rect)

            self.display_surface.blit(text_1,title_rect_1)
            self.display_surface.blit(text_2,title_rect_2)
            self.display_surface.blit(text_3,title_rect_3)
            self.display_surface.blit(text_4,title_rect_4)
            self.display_surface.blit(text_5,title_rect_5)

            for button in buttons:
                button.draw()
                pos = pygame.mouse.get_pos()
                if button.button.collidepoint(pos):
                    hover = True

            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.next_button.action():
                return 'intro_page_2'

            if self.skip_button.action():
                return 'game'

            pygame.display.update()

    def intro_page_2(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 45)

            message_1 = "YOUR MISSION IS TO COLLECT SACRED FLOWERS. THERE ARE 13 ON THE MAP."
            message_2 = "YOU NEED 9 TO RESTORE LIFE ON EARTH. BUT BE CAREFUL! THERE ARE"
            message_3 = "UNKNOWN MUTATED CREATURES AND TOXIC WASTES ALL OVER! BEWARE OF POISON"
            message_4 = "CLOUDS. IF YOU SEE ONE COMING RUN TO YOUR SAFE SPACE! EVERY WAVE DESTORYS "
            message_5 = "ONE UNCOLLECTED FLOWER. EACH COLLECTED FLOWER DECREASES YOUR SPEED BY 5%."
            message_6 = "TO REGAIN FULL SPEED RETURN TO THE SAFE SPACE AND UNLOAD YOUR CARGO."

            lineheight = 15

            text_1 = self.font.render(message_1, True, button_border_color)
            title_rect_1 = text_1.get_rect(midtop=(WINDOW_WIDTH / 2, 100))
            text_2 = self.font.render(message_2, True, button_border_color)
            title_rect_2 = text_2.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_1.bottom + lineheight))
            text_3 = self.font.render(message_3, True, button_border_color)
            title_rect_3 = text_3.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_2.bottom + lineheight))
            text_4 = self.font.render(message_4, True, button_border_color)
            title_rect_4 = text_4.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_3.bottom + lineheight))
            text_5 = self.font.render(message_5, True, button_border_color)
            title_rect_5 = text_5.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_4.bottom + lineheight))
            text_6 = self.font.render(message_6, True, button_border_color)
            title_rect_6 = text_6.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_5.bottom + lineheight))

            all_title_rects = [title_rect_1, title_rect_2, title_rect_3, title_rect_4, title_rect_5, title_rect_6]
            self.display_surface.blit(self.backgrounds[2], (0, 0))

            bg_rect = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 0, 0)
            bg_rect = bg_rect.unionall(all_title_rects)

            pygame.draw.rect(self.display_surface, button_border_color, bg_rect.inflate(10, 10))
            pygame.draw.rect(self.display_surface, button_bg_color, bg_rect)

            self.display_surface.blit(text_1, title_rect_1)
            self.display_surface.blit(text_2, title_rect_2)
            self.display_surface.blit(text_3, title_rect_3)
            self.display_surface.blit(text_4, title_rect_4)
            self.display_surface.blit(text_5, title_rect_5)
            self.display_surface.blit(text_6, title_rect_6)

            buttons = [self.back_button,self.next_button, self.skip_button]
            hover = False

            for button in buttons:
                button.draw()
                pos = pygame.mouse.get_pos()
                if button.button.collidepoint(pos):
                    hover = True

            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.back_button.action():
                return 'intro_page_1'

            if self.next_button.action():
                return 'intro_page_3'

            if self.skip_button.action():
                return 'game'

            pygame.display.update()

    def intro_page_3(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'exit'

            self.font = pygame.font.Font('../graphics/Apocalypse.ttf', 45)

            message_1 = "CONTROLS"
            message_2 = "W/UP ARROW - MOVE UP"
            message_3 = "S/DOWN ARROW - MOVE DOWN"
            message_4 = "A/LEFT ARROW - MOVE LEFT"
            message_5 = "D/RIGHT ARROW - MOVE RIGHT"
            message_6 = "E/P - COLLECT AND EMPTY STORAGE"

            lineheight = 15

            text_1 = self.font.render(message_1, True, button_border_color)
            title_rect_1 = text_1.get_rect(midtop=(WINDOW_WIDTH / 2, 100))
            text_2 = self.font.render(message_2, True, button_border_color)
            title_rect_2 = text_2.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_1.bottom + lineheight))
            text_3 = self.font.render(message_3, True, button_border_color)
            title_rect_3 = text_3.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_2.bottom + lineheight))
            text_4 = self.font.render(message_4, True, button_border_color)
            title_rect_4 = text_4.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_3.bottom + lineheight))
            text_5 = self.font.render(message_5, True, button_border_color)
            title_rect_5 = text_5.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_4.bottom + lineheight))
            text_6 = self.font.render(message_6, True, button_border_color)
            title_rect_6 = text_6.get_rect(midtop=(WINDOW_WIDTH / 2, title_rect_5.bottom + lineheight))

            all_title_rects = [title_rect_1, title_rect_2, title_rect_3, title_rect_4, title_rect_5, title_rect_6]
            self.display_surface.blit(self.backgrounds[0], (0, 0))

            bg_rect = pygame.Rect(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2, 0, 0)
            bg_rect = bg_rect.unionall(all_title_rects)

            pygame.draw.rect(self.display_surface, button_border_color, bg_rect.inflate(10, 10))
            pygame.draw.rect(self.display_surface, button_bg_color, bg_rect)

            self.display_surface.blit(text_1, title_rect_1)
            self.display_surface.blit(text_2, title_rect_2)
            self.display_surface.blit(text_3, title_rect_3)
            self.display_surface.blit(text_4, title_rect_4)
            self.display_surface.blit(text_5, title_rect_5)
            self.display_surface.blit(text_6, title_rect_6)

            buttons = [self.back_button, self.play_button]
            hover = False

            for button in buttons:
                button.draw()
                pos = pygame.mouse.get_pos()
                if button.button.collidepoint(pos):
                    hover = True

            if hover:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if self.back_button.action():
                return 'intro_page_2'

            if self.play_button.action():
                return 'game'

            pygame.display.update()

    def get_username(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_object_id == '#username_entry' and len(event.text)>0:
                    username = event.text
                    return username

                self.manager.process_events(event)

            dt = self.clock.tick() / 1000
            self.manager.update(dt)

            title = self.font.render('USERNAME:', True, button_border_color)
            title_rect = title.get_rect(center=(WINDOW_WIDTH / 2 - 150, WINDOW_HEIGHT / 2))

            next = self.font.render('PRESS ENTER TO CONTINUE:', True, button_border_color)
            next_rect = next.get_rect(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 100))

            self.display_surface.blit(self.backgrounds[0], (0, 0))
            pygame.draw.rect(self.display_surface, button_bg_color, title_rect.inflate(5,5))
            pygame.draw.rect(self.display_surface, button_bg_color, next_rect.inflate(5,5))

            self.display_surface.blit(next,next_rect)
            self.display_surface.blit(title,title_rect)
            self.manager.draw_ui(self.display_surface)

            pygame.display.update()