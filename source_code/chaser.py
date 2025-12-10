import random
import math
import game_framework
import game_world

from pico2d import *
from money import Money

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

# 공격 데미지 디바운스 시간 (boy의 attacktime_per_action(0.3) * 1.5과 동일)
ATTACK_WAIT_TIME = 0.3 * 0.8

METER = 2

animation_names = ['Walk']

class Chaser:
    images = None
    max_hp = 10
    font = None
    hpbar = None
    hpblank = None
    hit_sound = None
    death_sound = None
    def load_images(self):
        if Chaser.images == None:
            Chaser.images = load_image('16336.png')
        if Chaser.font == None:
            Chaser.font = load_font('ENCR10B.TTF', 16)
        if Chaser.hpbar == None:
            Chaser.hpbar = load_image('hpbar.png')
        if Chaser.hpblank == None:
            Chaser.hpblank = load_image('hpblank.png')
        if Chaser.hit_sound == None:
            Chaser.hit_sound = load_wav('se/hit.mp3')
        if Chaser.death_sound == None:
            Chaser.death_sound = load_wav('se/hit-flesh.mp3')

    def __init__(self, x = 400, left=100, bottom=100, right=100, top=100, strength=50, boy=None):
        self.x = x
        self.y =  80
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.count = 1
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top
        self.now_hp = Chaser.max_hp
        # 공격력: 전달받지 않으면 기본값 5
        self.strength = strength
        self.knockbackspeed = 0
        self.knockbackdir = 0
        # 데미지 디바운스용 대기시간 초기화
        self.wait_time = 0
        self.target = boy


    def get_bb(self):
        if self.dir < 0:
            return self.x - self.left * PIXEL_PER_METER, self.y - self.bottom * PIXEL_PER_METER, self.x + self.right * PIXEL_PER_METER, self.y + self.top * PIXEL_PER_METER
        else:
            return self.x - self.right * PIXEL_PER_METER, self.y - self.bottom * PIXEL_PER_METER, self.x + self.left * PIXEL_PER_METER, self.y + self.top * PIXEL_PER_METER

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if self.dir == 1 and self.x >= self.target.x + 15:
            self.dir = -1

        elif self.dir == -1 and self.x <= self.target.x - 15:
            self.dir = 1
        self.x += RUN_SPEED_PPS * self.dir * game_framework.frame_time
        self.x += self.knockbackspeed * self.knockbackdir * PIXEL_PER_METER * game_framework.frame_time
        self.knockbackspeed = max(0, self.knockbackspeed - DELTA_KNOCKBACK_SPEED * game_framework.frame_time)

        # 프레임 마다 바운더리 다르게 - 만약에 몬스터 종류마다 클래스로 하면 다시 주석 해제할것
        #if int(self.frame) == 2 or int(self.frame) == 3:
        #    self.left = 30
        #else:
        #    self.left = 10

        if self.x > 800:
            self.dir = -1
        elif self.x < 100:
            self.dir = 1
        self.x = clamp(100, self.x, 800)
        pass


    def draw(self):
        if self.dir < 0:
            Chaser.images.clip_composite_draw(int(self.frame) * 25, 0, 25, 27, 0, '',
                                               self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            Chaser.images.clip_composite_draw(int(self.frame) * 25, 0, 25, 27, 0, 'h',
                                              self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        #draw_rectangle(*self.get_bb())
        Chaser.hpblank.clip_draw(0, 0, 5, 5, self.x, self.y + 50, 50, 5)
        Chaser.hpbar.clip_draw_to_origin(0, 0, 5, 5, self.x - 25, self.y + 50, 50 * (self.now_hp / Chaser.max_hp), 5)

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'attack:zombie':
            # 일정 시간(ATTACK_WAIT_TIME) 동안은 추가 데미지를 받지 않도록 디바운스
            if get_time() - self.wait_time >= ATTACK_WAIT_TIME:
                self.wait_time = get_time()
                self.now_hp -= other.strength
                if self.now_hp > 0:
                    # 맞은 곳과 반대로 튕겨야함
                    Chaser.hit_sound.play()
                    dx = self.x - other.x
                    if dx == 0:
                        self.knockbackdir = 0.0
                    else:
                        # dx / math.fabs(dx)는 dx의 부호(+1 또는 -1)를 반환
                        self.knockbackdir = dx / math.fabs(dx)
                    self.knockbackspeed = 10
                    pass
                else:
                    Chaser.death_sound.play()
                    # 죽을 때 돈을 드롭
                    money = Money(self.x, self.y, value=5)
                    game_world.add_object(money, 1)
                        # boy:money 충돌 페어에 몬스터 드랍 등록
                    game_world.add_collision_pair('boy:money', None, money)
                    game_world.remove_object(self)
                    other.boy_pointer.hunt_count += 1

        elif group == 'boy:enemy':
            pass
