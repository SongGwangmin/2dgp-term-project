from pico2d import load_image, draw_rectangle
import boy

class Pannel:
    image = None
    def __init__(self, divider=0):
        if Pannel.image is None:
            Pannel.image = load_image('item_select.png')
        self.Sold_out = load_image('sold_out.png')
        self.divider = divider
        # border[0] = (left, bottom, right, top)
        # border[1] = border[0]의 각 요소에 100을 더한 값
        self.border = (
            (270, 200, 530, 260),
            (270, 260, 530, 320)
        )
        self.cursorin = 0

    def draw(self):
        self.image.draw(400, 300)
        if self.divider == 0:
            if self.cursorin == 1:
                draw_rectangle(*self.border[0])
            elif self.cursorin == 2:
                draw_rectangle(*self.border[1])
                
            if boy.Boy.set_slash == 1:
                self.Sold_out.draw(700, 150)




    def update(self):
        pass

    def click_colision(self, x, y):
        if self.border[0][0] <= x <= self.border[0][2] and self.border[0][1] <= y <= [3]:
            return 1
        elif self.border[1][0] <= x <= self.border[1][2] and self.border[1][1] <= y <= self.border[1][3]:
            return 2
        return 0

    def mousemove_colision(self, x, y):
        if self.border[0][0] <= x <= self.border[0][2] and self.border[0][1] <= y <= self.border[0][3]:
            self.cursorin = 1
        elif self.border[1][0] <= x <= self.border[1][2] and self.border[1][1] <= y <= self.border[1][3]:
            self.cursorin = 2
        else:
            self.cursorin = 0