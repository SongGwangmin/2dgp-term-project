from pico2d import load_image, draw_rectangle
import boy

class Pannel:
    image = None
    def __init__(self, divider=0):
        if Pannel.image is None:
            Pannel.image = load_image('item_select.png')
        self.Sold_out = load_image('sold_out.png')
        self.divider = divider

    def draw(self):
        self.image.draw(400, 300)
        if self.divider == 0:
            if boy.Boy.set_slash == 1:
                self.Sold_out.draw(700, 150)


    def update(self):
        pass