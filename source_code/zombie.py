import random
import math
import game_framework
import game_world

from pico2d import *

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4.0

METER = 5

animation_names = ['Walk']

class Zombie:
    images = None
    maxhp = 10
    font = None
    def load_images(self):
        if Zombie.images == None:
            Zombie.images = load_image('LARVA.png')
        if Zombie.font == None:
            Zombie.font = load_font('ENCR10B.TTF', 16)

    def __init__(self):
        self.x, self.y = random.randint(100, 800), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.count = 1
        self.size = 100
        self.hp = Zombie.maxhp


    def get_bb(self):
        return self.x - self.size, self.y - self.size + 50 * (self.count - 1), self.x + self.size, self.y + self.size + 50 * (self.count - 1)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        if self.x > 800:
            self.dir = -1
        elif self.x < 100:
            self.dir = 1
        self.x = clamp(100, self.x, 800)
        pass


    def draw(self):
        if self.dir < 0:
            Zombie.images.clip_composite_draw(int(self.frame) * 144 + 2, 0, 144, 114, 0, '',
                                               self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            Zombie.images.clip_composite_draw(int(self.frame) * 144 + 2, 0, 144, 114, 0, 'h',
                                              self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        draw_rectangle(*self.get_bb())
        Zombie.font.draw(self.x-10, self.y + 50, f'{self.hp:02d}', (255, 0, 0))

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'ball:zombie':
            self.hp -= other.strength
            if self.hp > 0:
                pass
            else:
                game_world.remove_object(self)
        elif group == 'boy:zombie':
            pass