from pico2d import load_image

class Plate:
    image = None
    def __init__(self, divider=0):
        if Plate.image is None:
            Plate.image = load_image('gameover.png')

    def draw(self):
        self.image.draw(400, 300)




    def update(self):
        pass


