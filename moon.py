from pygame import *


class Platform(sprite.Sprite):
    def __init__(self, x, y, PLATFORM_COLOR, PLATFORM_WIDTH, PLATFORM_HEIGHT):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class Moon(sprite.Sprite):
    def __init__(self, x, y, PLATFORM_COLOR, PLATFORM_WIDTH, PLATFORM_HEIGHT):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
