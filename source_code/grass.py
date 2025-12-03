from pico2d import *


class Grass:
    image = None
    def __init__(self, y=0, x=800):
        #self.image = load_image('forest.png')
        self.y = y
        self.left = 0
        self.right = x
        if Grass.image is None:
            Grass.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 300)
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        return 0, 0, 8000, 50

    def handle_collision(self, group, other):
        pass
