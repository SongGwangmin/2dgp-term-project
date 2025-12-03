import random
import game_framework
import game_world

from pico2d import *
from money import Money
import common

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

METER = 20

animation_names = ['Walk']

IDLE, ATTACK, CRUSH = 200, 100, 0

class Boss:
    images = None
    max_hp = 100
    font = None
    hpbar = None
    hpblank = None
    def load_images(self):
        if Boss.images == None:
            Boss.images = load_image('boss.png')
        if Boss.font == None:
            Boss.font = load_font('ENCR10B.TTF', 16)
        if Boss.hpbar == None:
            Boss.hpbar = load_image('hpbar.png')
        if Boss.hpblank == None:
            Boss.hpblank = load_image('hpblank.png')

    def __init__(self, x = 400, left=1, bottom=1, right=1, top=1, strength=50):
        self.x = x
        self.y =  80
        self.load_images()
        self.frame = random.randint(0, 9)
        self.dir = random.choice([-1,1])
        self.count = 1
        self.left = METER / 3
        self.bottom = METER / 2
        self.right = METER / 3
        self.top = METER / 2
        self.now_hp = Boss.max_hp
        # 공격력: 전달받지 않으면 기본값 5
        self.strength = strength
        self.knockbackspeed = 0
        self.knockbackdir = 0
        # 데미지 디바운스용 대기시간 초기화
        self.wait_time = 0
        self.state = IDLE


    def get_bb(self):
        if self.dir < 0:
            return self.x - self.left * PIXEL_PER_METER, self.y - self.bottom * PIXEL_PER_METER, self.x + self.right * PIXEL_PER_METER, self.y + self.top * PIXEL_PER_METER
        else:
            return self.x - self.right * PIXEL_PER_METER, self.y - self.bottom * PIXEL_PER_METER, self.x + self.left * PIXEL_PER_METER, self.y + self.top * PIXEL_PER_METER

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION




    def draw(self):

        Boss.images.clip_composite_draw(int(self.frame) * 100, self.state, 100, 100, 0, '',
                                               self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)

        draw_rectangle(*self.get_bb())
        Boss.hpblank.clip_draw_to_origin(0, 0, 5, 5, 25, 15, common.grass.w - 25 - 25, 25)
        Boss.hpbar.clip_draw_to_origin(0, 0, 5, 5, 25, 15, (common.grass.w - 25 - 25) * (self.now_hp / Boss.max_hp), 25)
        #(self.now_hp / Boss.max_hp)
    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'attack:zombie':
            # 일정 시간(ATTACK_WAIT_TIME) 동안은 추가 데미지를 받지 않도록 디바운스
            if get_time() - self.wait_time >= ATTACK_WAIT_TIME:
                self.wait_time = get_time()
                self.now_hp -= other.strength
                if self.now_hp > 0:
                    # 보스는 넉백없음
                    pass
                else:
                    # 죽을 때 돈을 드롭
                    money = Money(self.x, self.y, value=500)
                    game_world.add_object(money, 1)
                        # boy:money 충돌 페어에 몬스터 드랍 등록
                    game_world.add_collision_pair('boy:money', None, money)
                    game_world.remove_object(self)
                    other.boy_pointer.hunt_count += 1

        elif group == 'boy:enemy':
            pass
