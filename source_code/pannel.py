from pico2d import load_image, draw_rectangle
import boy

class Pannel:
    image = None
    def __init__(self, divider=0):
        if Pannel.image is None:
            Pannel.image = load_image('item_select.png')
        self.Sold_out = load_image('sold_out.png')
        self.divider = divider
        self.slashleft = 270
        self.slashright = 530
        self.slashbottom = 200
        self.slashtop = 260

    def draw(self):
        self.image.draw(400, 300)
        if self.divider == 0:
            if boy.Boy.set_slash == 1:
                self.Sold_out.draw(700, 150)
            else:
                draw_rectangle(self.slashleft, self.slashbottom, self.slashright, self.slashtop)


    def update(self):
        pass

    def click_colision(self, x, y):
        if self.divider == 0:
            if self.slashleft <= x <= self.slashright and self.slashbottom <= y <= self.slashtop:
                return True
        return False

    def mousemove_colision(self, x, y):
        if self.divider == 0:
            if self.slashleft <= x <= self.slashright and self.slashbottom <= y <= self.slashtop:
                return True
        return False