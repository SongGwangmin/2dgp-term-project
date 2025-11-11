from pico2d import *


class Grass:
    def __init__(self, y=0):
        self.image = load_image('forest.png')
        self.y = y

    def draw(self):
        self.image.draw(400, 300)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0, 0, 800, 50

    def handle_collision(self, group, other):
        pass
