
from pico2d import load_image, draw_rectangle
import game_world
import game_framework
import math


METER = 1
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm

RUN_SPEED_KMPH = 40.0            # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


class Fether:
    image = None
    def __init__(self, x = 400, y=400, boy = None):
        print('create fether')
        if Fether.image is None:
            Fether.image = load_image('fether.png')  # 적절한 이미지로 교체 가능
        self.x = x
        self.y = y

        # boy의 현재 좌표를 목표로 설정
        if boy:
            self.target_x = boy.x
            self.target_y = boy.y

            # boy를 향한 방향 계산 (각도)
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            self.angle = math.atan2(dy, dx)  # 반대 방향으로 날아가도록 각도 조정
            distance = math.sqrt(dx**2 + dy**2)

        else:
            self.dir_x = 1
            self.dir_y = 0

    def draw(self):
        self.image.clip_composite_draw(0, 0, 64, 64, self.angle + math.pi / 2, 'h', self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        draw_rectangle(*self.get_bb())

    def update(self):
        # 직선으로 이동
        self.x += math.cos(self.angle) * RUN_SPEED_PPS * game_framework.frame_time
        self.y += math.sin(self.angle) * RUN_SPEED_PPS * game_framework.frame_time

        # 화면 밖으로 나가면 제거
        if self.x < -50 or self.x > 850 or self.y < -50 or self.y > 650:
            game_world.remove_object(self)

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def handle_collision(self, group, other):
        if group == 'fether:boy':
            game_world.remove_object(self)
            print('fether collide with boy')

