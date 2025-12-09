
from pico2d import load_image, draw_rectangle
import game_world
import game_framework
import math

import common

METER = 1
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

RUN_SPEED_KMPH = 40.0            # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

GRAVITY = 9.8  # 중력 가속도 (m/s^2)

class Rock:
    image = None
    def __init__(self, x = 400, y=400, xv=0, strength=5):
        print('create rock')
        if Rock.image is None:
            Rock.image = load_image('point.png')  # 적절한 이미지로 교체 가능
        self.x = x
        self.y = y
        self.strength = strength
        self.yv = 15
        self.xv = xv



    def draw(self):
        sx = self.x - common.grass.left
        Rock.image.draw(sx, self.y)


    def update(self):
        # 직선으로 이동
        self.x += game_framework.frame_time * self.xv
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        self.yv -= GRAVITY * game_framework.frame_time  # m/s

        # 화면 밖으로 나가면 제거
        if self.x < -50 or self.x > common.grass.w + 50 or self.y < -50:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 30, self.y - 30, self.x + 30, self.y + 30

    def handle_collision(self, group, other):
        if group == 'boy:enemy':
            #game_world.remove_object(self)
            print('rock collide with boy')

