from pico2d import load_image

class Keycap:
    image = None

    def __init__(self, x=400, y=300):
        if Keycap.image is None:
            Keycap.image = load_image('space.png')
        self.x = x
        self.y = y

    def draw(self):
        if Keycap.image:
            Keycap.image.draw(self.x, self.y)

    def update(self):
        pass

    def get_bb(self):
        # 중심을 (self.x, self.y - 100)으로 하고, 너비 50, 높이 40으로 바운딩 박스 반환
        cx = self.x
        cy = self.y - 100
        half_w = 50 / 2
        half_h = 40 / 2
        left = cx - half_w
        bottom = cy - half_h
        right = cx + half_w
        top = cy + half_h
        return left, bottom, right, top
