from pico2d import *
import common

class Grass:
    image = None
    def __init__(self, y=0, x=800):
        #self.image = load_image('forest.png')
        self.y = y

        self.cw = get_canvas_width()


        self.w = self.image.w
        self.left = 0

        if Grass.image is None:
            Grass.image = load_image('grass.png')

    def draw(self):
        self.image.draw(400, 300)
        draw_rectangle(*self.get_bb())

    def update(self):
        self.left = clamp(0, int(common.boy.x) - self.cw // 2, self.w - self.cw - 1)

    def get_bb(self):
        return 0, 0, 8000, 50

    def handle_collision(self, group, other):
        pass
