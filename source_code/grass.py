from pico2d import *


class Grass:
    def __init__(self, y=0):
        self.image = load_image('grass.png')
        self.y = y

    def draw(self):
        self.image.draw(400, 30 + self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0, 0, 800, 50

