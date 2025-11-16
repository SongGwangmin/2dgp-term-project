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

DELTA_KNOCKBACK_SPEED = 40

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
    hpbar = None
    def load_images(self):
        if Zombie.images == None:
            Zombie.images = load_image('LARVA.png')
        if Zombie.font == None:
            Zombie.font = load_font('ENCR10B.TTF', 16)
        if Zombie.hpbar == None:
            Zombie.hpbar = load_image('hpbar.png')

    def __init__(self):
        self.x, self.y = random.randint(100, 800), 150
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.count = 1
        self.size = 100
        self.hp = Zombie.maxhp
        self.knockbackspeed = 0
        self.knockbackdir = 0


    def get_bb(self):
        return self.x - self.size, self.y - self.size + 50 * (self.count - 1), self.x + self.size, self.y + self.size + 50 * (self.count - 1)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        self.x += self.knockbackspeed * self.knockbackdir * PIXEL_PER_METER * game_framework.frame_time
        self.knockbackspeed = max(0, self.knockbackspeed - DELTA_KNOCKBACK_SPEED * game_framework.frame_time)

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
        #Zombie.font.draw(self.x-10, self.y + 50, f'{self.hp:02d}', (255, 0, 0))
        Zombie.hpbar.clip_draw(0, 0, 5, 5, self.x, self.y + 50, 50 * (self.hp / Zombie.maxhp), 5)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'ball:zombie':
            self.hp -= other.strength
            if self.hp > 0:
                # 맞은 곳과 반대로 튕겨야함
                dx = self.x - other.x
                if dx == 0:
                    self.knockbackdir = 0.0
                else:
                    # dx / math.fabs(dx)는 dx의 부호(+1 또는 -1)를 반환
                    self.knockbackdir = dx / math.fabs(dx)
                self.knockbackspeed = 5
                pass
            else:
                game_world.remove_object(self)
                other.boy_pointer.hunt_count += 1
        elif group == 'boy:zombie':
            pass