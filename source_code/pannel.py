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
            (270, 260, 530, 320),
            (270, 330, 530, 390)
        )
        self.cursorin = 0

    def draw(self):
        self.image.draw(400, 300)
        for i in range(len(self.border)):
            if self.cursorin == i + 1:
                draw_rectangle(*self.border[i])
        if self.divider == 0:
            if boy.Boy.set_slash == 1:
                self.Sold_out.draw(700, 150)




    def update(self):
        pass

    def click_colision(self, x, y):
        for i in range(len(self.border)):
            if self.border[i][0] <= x <= self.border[i][2] and self.border[i][1] <= y <= self.border[i][3]:
                return i + 1
        return 0

    def mousemove_colision(self, x, y):
        for i in range(len(self.border)):
            if self.border[i][0] <= x <= self.border[i][2] and self.border[i][1] <= y <= self.border[i][3]:
                self.cursorin = i + 1
                return
        self.cursorin = 0
