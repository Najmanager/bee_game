import pygame,sys
from menu import Menu
from game import Game
from intro import Intro
from scores import Scores

def app():
    menu = Menu()
    status = 'menu'

    while status != 'exit':  # assuming 'exit' is the way to stop the loop
        if status == 'menu':
            status = menu.run()
        elif status == 'scores':
            scores = Scores()
            status = scores.run()
        elif status == 'intro':
            intro = Intro()
            username = intro.get_username()
            status = intro.intro_page_1()
        elif status == 'intro_page_1':
            intro = Intro()
            status = intro.intro_page_1()
        elif status == 'intro_page_2':
            intro = Intro()
            status = intro.intro_page_2()
        elif status == 'intro_page_3':
            intro = Intro()
            status = intro.intro_page_3()
        elif status == 'game':
            game = Game(username)
            status = game.run()

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    app()
