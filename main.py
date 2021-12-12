import pygame
from rocket import Rocket
from moon import Platform, Moon
from random import *
import numpy as np
from time import *
import tkinter
from PIL import ImageTk, Image


pygame.init()
p = 1280
i = 720
run = True
game_over = pygame.transform.scale(
    pygame.image.load(r"assets\game-over-screen.png"), (p, i))
BOOM = [
    r"assets\1.png",
    r"assets\2.png",
    r"assets\3.png",
    r"assets\4.png",
    r"assets\5.png",
    r"assets\6.png",
    r"assets\7.png",
    r"assets\8.png"]
FUEL = [r"assets\1_fuel.jpg", r"assets\2_fuel.jpg"]
bg = pygame.transform.scale(pygame.image.load(
    r'assets\earth-4566050__340.png'), (p, i))
bg_pause = pygame.transform.scale(
    pygame.image.load(r'assets\earth-pause.png'), (p, i))
PLATFORM_WIDTH = p // 50
PLATFORM_HEIGHT = i // 40
PLATFORM_COLOR = "#000000"
PLANET_COLOR = "#888888"
root = None
pause = False
temp_fuel = 400


def draw_shield_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 400
    BAR_HEIGHT = 10
    fill = (pct / 400) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    if fill >= 120:
        pygame.draw.rect(surf, "GREEN", fill_rect)
    else:
        pygame.draw.rect(surf, "RED", fill_rect)
    pygame.draw.rect(surf, "WHITE", outline_rect, 2)


def level_gener():
    global level, rocket, temp_fuel, peak
    rocket = Rocket(
        p //
        2,
        i //
        6,
        PLATFORM_WIDTH,
        PLATFORM_WIDTH *
        2)  # создаем героя по (x,y) координатам
    try:
        if temp_fuel + 200 < 400:
            rocket.fuel = temp_fuel + 200
            rocket.consumption = score // 2 + 1
    except BaseException:
        pass
    left = right = False    # по умолчанию — стоим

    # создание поверхности луны 40*50
    step_counter = randint(2, 18)

    step_counter_2 = step_counter + randint(10, 30)

    level = np.zeros((51, 40))
    for row in range(len(level)):
        if step_counter == 0 or step_counter == -1 or step_counter == - \
                2 or step_counter_2 == 0 or step_counter_2 == -1 or step_counter_2 == -2:
            level[row][peak] = 2
            level[row][peak + 1] = 2
            for j in range(peak + 2, len(level[row])):
                level[row][j] = 1
        else:
            peak = randint((len(level[row]) // 2),
                           len(level[row]) - len(level[row]) // 4)
            level[row][peak] = 3
            for j in range(peak + 1, len(level[row])):
                level[row][j] = 1
        step_counter -= 1
        step_counter_2 -= 1
    level = level.transpose()
    rocket.level = level


def score_writer(score):
    f = open('record.txt', 'r+')
    text = [i.split() for i in f]
    if text[0][-1] == "None" or int(text[0][-1]) < score:
        text[0][-1] = str(score)
    for i in range(3, 1, -1):
        text[i][-1] = text[i - 1][-1]
    text[1][-1] = str(score)
    text = [' '.join(i) for i in text]
    f.truncate(0)
    f.seek(0)
    for i in text:
        f.write(i + '\n')
    f.close()


def main():
    global p, i, run, level, entities, rocket, platforms, moon, moon_surface, x, pause, temp_fuel
    score = 0
    root.destroy()
    pygame.init()
    pygame.display.set_caption("MoonLand by Alex_Manich")
    window = pygame.display.set_mode((p, i))
    level_gener()
    rocket.consumption = score // 2 + 1
    while run:
        clock = pygame.time.Clock()
        clock.tick(60)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        window.blit(bg, (0, 0))
        entities = pygame.sprite.Group()
        platforms = []
        entities.add(rocket)
        moon_surface = pygame.sprite.Group()
        moon = []
        moon_surface.add(rocket)
        x = y = 0  # координаты
        for row in rocket.level:  # вся строка
            for col in row:  # каждый символ
                if col == 2:
                    pf = Platform(
                        x,
                        y,
                        PLATFORM_COLOR,
                        PLATFORM_WIDTH,
                        PLATFORM_HEIGHT)
                    entities.add(pf)
                    platforms.append(pf)
                elif col == 1:
                    pf = pygame.Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
                    pf.fill(pygame.Color(PLANET_COLOR))
                    window.blit(pf, (x, y))
                elif col == 3:
                    pf = Moon(x, y, "#FFCC33", PLATFORM_WIDTH, PLATFORM_HEIGHT)
                    moon_surface.add(pf)
                    moon.append(pf)
                x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

        # Работа клавиш
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            left = True
            right = False
        elif keys[pygame.K_RIGHT]:
            left = False
            right = True
        else:
            left = False
            right = False

        if keys[pygame.K_UP] and y > 0:
            up = True
        elif keys[pygame.K_DOWN] and y > 0:
            down = True
        else:
            up = False
            down = False

        if keys[pygame.K_ESCAPE]:
            if pause:
                sleep(0.1)
                pause = False
            else:
                sleep(0.1)
                pause = True

        if rocket.win == True:
            rocket.win = None
            level, moon, platforms = [], [], []
            level_gener()
            temp_fuel = rocket.fuel
            score += 1
            rocket.consumption = score // 2 + 1

        if rocket.win == False:
            if rocket.boom:
                for j in BOOM:
                    frame = pygame.transform.scale(
                        pygame.image.load(j), (p, i))
                    window.blit(frame, (0, 0))
                    pygame.display.update()
                    sleep(0.3)
            elif rocket.nullfuel:
                for k in range(3):
                    for j in FUEL:
                        frame = pygame.transform.scale(
                            pygame.image.load(j), (p, i))
                        window.blit(frame, (0, 0))
                        pygame.display.update()
                        sleep(0.8)
            window.blit(game_over, (0, 0))
            font = pygame.font.Font(None, 74)
            text = font.render("YOUR SCORE " + str(score), 1, "white")
            score_writer(score)
            window.blit(text, (700, 600))
            pygame.display.update()
            sleep(2)
            pygame.display.quit()
            pygame.quit()
            main_menu()

        if pause:
            window.blit(bg_pause, (0, 0))
            pygame.display.update()
        else:
            font = pygame.font.Font(None, 74)
            text = font.render("SCORE " + str(score), 1, "white")
            window.blit(text, (1000, 10))
            if left or right or up or down:
                rocket.fuel -= rocket.consumption
            rocket.update(
                left,
                right,
                up,
                down,
                p,
                platforms,
                moon)  # передвижение
            entities.draw(window)
            moon_surface.draw(window)
            draw_shield_bar(window, p / 5, 10, rocket.fuel)
            pygame.display.update()


def main_menu():
    def ShowRecords():
        record_win = tkinter.Tk()
        f = open('record.txt')
        for line in f:
            tkinter.Label(
                record_win, text=line, font=(
                    "Comic Sans MS", 12, "bold")).pack()
        record_win.mainloop()
        f.close()
    global root
    root = tkinter.Tk()
    root.title("MoonLand by Alex_Manich")
    root.geometry(f"{p}x{i}")
    img = Image.open(r"assets\earth.jpg")
    imag = img.resize((p, i), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(imag)
    panel = tkinter.Label(root, image=image)
    panel.pack(side="top", fill="both", expand="no")
    tkinter.Label(
        root,
        text="Moon Landing",
        font="Arial 40").place(
        relx=0.45,
        rely=0.1)
    tkinter.Button(
        root,
        height=5,
        width=20,
        text="Play",
        command=main).place(
        relx=0.5,
        rely=0.3)
    tkinter.Button(
        root,
        height=5,
        width=20,
        text="Records",
        command=ShowRecords).place(
        relx=0.5,
        rely=0.5)
    tkinter.Button(
        root,
        height=5,
        width=20,
        text="Quit",
        command=root.destroy).place(
        relx=0.5,
        rely=0.7)
    root.mainloop()


if __name__ == "__main__":
    main_menu()
