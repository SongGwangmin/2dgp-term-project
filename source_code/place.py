from pico2d import *
import common

class Place:
    image = None
    def __init__(self, y=0, x=800):
        #self.image = load_image('forest.png')
        self.y = y
        if Place.image is None:
            Place.image = load_image('bossplace.png')
        self.cw = get_canvas_width()

        self.w = self.image.w
        self.left = 0



    def draw(self):
        self.image.clip_draw_to_origin( self.left, 0, self.cw, 600, 0, 0 )
        #draw_rectangle(*self.get_bb())

    def update(self):
        self.left = clamp(0, int(common.boy.x) - self.cw // 2, self.w - self.cw - 1)

    def get_bb(self):
        return 0, 0, 8000, 50

    def handle_collision(self, group, other):
        pass