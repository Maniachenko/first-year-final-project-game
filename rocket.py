from pygame import *
import time
import numpy as np


MOVE_SPEED = 10
COLOR = "#888888"
ANIMATION_DELAY = 0.1
ANIMATION_URL = [r'assets\first.png', r'assets\second.png']
ANIMATION_STAY = r'assets\basic.png'
ANIMATION_LAND = [r"assets\land_1.jpg", r"assets\land_2.jpg"]
animCount = 0


class Rocket(sprite.Sprite):

    def __init__(self, x, y, WIDTH, HEIGHT):
        sprite.Sprite.__init__(self)
        self.onGround = False
        self.xvel = 0  # скорость перемещения. 0 - стоять на месте
        self.yvel = 0
        self.xvel_temp = 0
        self.yvel_temp = 0
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.startX = x  # Начальная позиция Х, пригодится когда будем переигрывать уровень
        self.startY = y
        self.image = Surface((WIDTH, HEIGHT))
        self.image = transform.scale(
            image.load(ANIMATION_STAY), (WIDTH * 2, HEIGHT * 2))
        self.rect = Rect(x, y, WIDTH, HEIGHT)  # прямоугольный объект
        self.win = None
        self.l_counter = 0
        self.r_counter = 0
        self.level = None
        self.fuel = 400
        self.consumption = None
        self.boom = False
        self.nullfuel = False

    def update(self, left, right, up, down, p, platforms, moon):
        global FALL_SPEED, animCount
        self.xvel, self.yvel = 0, 0
        if left and self.rect.x >= 10:
            self.xvel = -MOVE_SPEED
            self.image = transform.scale(image.load(
                ANIMATION_URL[animCount % 2]), (self.WIDTH * 2, self.HEIGHT * 2))
            animCount += 1
            self.xvel_temp = - 1

        if right and self.rect.x <= p - self.WIDTH - 35:
            self.xvel = MOVE_SPEED
            self.image = transform.scale(image.load(
                ANIMATION_URL[animCount % 2]), (self.WIDTH * 2, self.HEIGHT * 2))
            animCount += 1
            self.xvel_temp = 1

        if up:
            self.yvel = -MOVE_SPEED
            self.onGround = False
            self.image = transform.scale(image.load(
                ANIMATION_URL[animCount % 2]), (self.WIDTH * 2, self.HEIGHT * 2))
            animCount += 1
            self.yvel_temp -= 1

        if down:
            self.yvel = MOVE_SPEED
            self.onGround = False
            self.image = transform.scale(image.load(
                ANIMATION_URL[animCount % 2]), (self.WIDTH * 2, self.HEIGHT * 2))
            animCount += 1
            self.yvel_temp = 1

        if self.rect.x <= 10:
            if left:
                self.r_counter = 0
                self.l_counter += MOVE_SPEED
                self.image = transform.scale(image.load(
                    ANIMATION_URL[animCount % 2]), (self.WIDTH * 2, self.HEIGHT * 2))
            if self.l_counter >= 25:
                self.l_counter = 0
                self.level = np.c_[self.level[:, -1], self.level[:, :-1]]

        elif self.rect.x >= p - self.WIDTH - 35:
            if right:
                self.l_counter = 0
                self.r_counter += MOVE_SPEED
                self.image = transform.scale(image.load(
                    ANIMATION_URL[animCount % 2]), (self.WIDTH * 2, self.HEIGHT * 2))
            if self.r_counter >= 25:
                self.r_counter = 0
                self.level = np.c_[self.level[:, 1:], self.level[:, 0]]

        if not (down or up or right or left):
            self.image = transform.scale(
                image.load(ANIMATION_STAY), (self.WIDTH * 2, self.HEIGHT * 2))

        if self.fuel <= 0:
            self.win = False
            self.nullfuel = True

        if self.onGround:
            self.yvel = 0
        else:
            if not(down or up):
                self.yvel = self.yvel_temp
            if not(right or left):
                self.xvel = self.xvel_temp
        self.onGround = False

        if animCount > 30:
            animCount = 0

        if self.rect.y + self.yvel >= 0:
            self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms, moon, down)

        if self.rect.x + self.xvel >= 10 and self.rect.x + \
                self.xvel <= p - self.WIDTH - 35:
            self.rect.x += self.xvel  # переносим свои положение на xvel

    def collide(self, xvel, yvel, platforms, moon, down):
        for p in platforms:
            if sprite.collide_rect(
                    self, p):  # если есть пересечение платформы с игроком
                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0           # и энергия падения пропадает
                    time.sleep(1)
                    if down:
                        self.win = False
                        self.boom = True
                    else:
                        self.win = True

        for p in moon:
            if sprite.collide_rect(
                    self, p):  # если есть пересечение платформы с игроком
                if yvel > 0:                      # если падает вниз
                    self.rect.bottom = p.rect.top  # то не падает вниз
                    self.onGround = True          # и становится на что-то твердое
                    self.yvel = 0           # и энергия падения пропадает
                    self.win = False
                    self.boom = True
