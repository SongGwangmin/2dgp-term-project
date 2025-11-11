from pico2d import load_image
import game_world
import game_framework

METER = 3
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

RUN_SPEED_KMPH = 100.0            # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Ball:
    image = None
    def __init__(self, x = 400, y=400, velocity=1):
        print('create ball')
        if Ball.image is None:
            Ball.image = load_image('ball21x21.png')
        self.x = x
        self.y = y
        self.velocity = velocity
        # self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 2 * 128, 128, 128, 0, 'h',
        #                                           self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
    def draw(self):
        self.image.clip_composite_draw(0, 0, 21, 21, 0, '', self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        print('draw ball')

    def update(self):
        self.x += self.velocity * RUN_SPEED_PPS * game_framework.frame_time
        print('update ball')

        if self.x < 0 or self.x > 800:
            game_world.remove_object(self)
