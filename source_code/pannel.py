from pico2d import load_image

class Pannel:
    image = None
    def __init__(self):
        if Pannel.image is None:
            Pannel.image = load_image('item_select.png')


    def draw(self):
        self.image.draw(400, 300)

    def update(self):
        pass