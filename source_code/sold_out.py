from pico2d import load_image

class Sold_out:
    image = None
    def __init__(self, x=400, y=300):
        if Sold_out.image is None:
            Sold_out.image = load_image('sold_out.png')
        self.x = x
        self.y = y


    def draw(self):
        self.image.draw(self.x, self.y)

    def update(self):
        pass