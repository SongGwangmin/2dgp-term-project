from pico2d import load_image


class Grass:
    def __init__(self, y=0):
        self.image = load_image('grass.png')
        self.y = y

    def draw(self):
        self.image.draw(400, 30 + self.y)

    def update(self):
        pass
