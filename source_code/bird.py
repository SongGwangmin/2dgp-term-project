from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
from money import Money
from fether import Fether

import common

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

animation_names = ['eagle_1_0']

ATTACK_WAIT_TIME = 0.3 * 0.8

class Bird:
    images = None
    hpbar = None
    hpblank = None
    max_hp = 10

    def load_images(self):
        if Bird.images == None:
            Bird.images = {}
            for name in animation_names:
                Bird.images[name] = [load_image("./bird/" + name + "%d" % i + ".png") for i in range(1, 6+1)]
            # eagle_1_0 프레임 뒤에 5,4,3,2 순서의 프레임을 추가
            if 'eagle_1_0' in Bird.images:
                for idx in [4, 3, 2, 1]:
                    Bird.images['eagle_1_0'].append(Bird.images['eagle_1_0'][idx])
            Bird.font = load_font('ENCR10B.TTF', 40)


    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.load_images()
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'eagle_1_0'
        self.ball_count = 0
        self.strength = 5
        self.now_hp = Bird.max_hp
        if Bird.hpbar == None:
            Bird.hpbar = load_image('hpbar.png')
        if Bird.hpblank == None:
            Bird.hpblank = load_image('hpblank.png')

        self.tx, self.ty = 1000, 1000
        # 여기를 채우시오.
        self.patrol_locations = [(43, 274), (708, 274)]
        self.loc_no = 0
        self.wait_time = 0
        self.shoottimer = get_time()
        self.build_behavior_tree()


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # fill here
        self.behavior_tree.run() # 매 프레임마다 행동 트리 실행


    def draw(self):
        if math.cos(self.dir) > 0:
            Bird.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Bird.images[self.state][int(self.frame)].draw(self.x, self.y, 100, 100)

        Bird.hpblank.clip_draw(0, 0, 5, 5, self.x, self.y + 50, 50, 5)
        Bird.hpbar.clip_draw_to_origin(0, 0, 5, 5, self.x - 25, self.y + 50, 50 * (self.now_hp / Bird.max_hp), 5)

        draw_rectangle(*self.get_bb())

        #draw_circle(self.x, self.y, int(7 * PIXEL_PER_METER), 255,255,0)  # 추적 범위 표시

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
                    dx = self.x - other.x
                    if dx == 0:
                        self.knockbackdir = 0.0
                    else:
                        # dx / math.fabs(dx)는 dx의 부호(+1 또는 -1)를 반환
                        self.knockbackdir = dx / math.fabs(dx)
                    self.knockbackspeed = 2
                    pass
                else:
                    # 죽을 때 돈을 드롭
                    money = Money(self.x, self.y, value=5)
                    game_world.add_object(money, 1)
                    # boy:money 충돌 페어에 몬스터 드랍 등록
                    game_world.add_collision_pair('boy:money', None, money)
                    game_world.remove_object(self)
                    other.boy_pointer.hunt_count += 1


    def set_target_location(self, x=None, y=None):
        # 여기를 채우시오.
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS




    def distance_less_than(self, x1, y1, x2, y2, r): # 두 점 사이의 거리가 r보다 작은가?
        # 여기를 채우시오.
        # 제곱근은 연산을 느리게 하므로 제곱근을 구하지 않고 대소 비교
        distance_sq = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distance_sq < (r * PIXEL_PER_METER) ** 2 # R은 거리단위라서 픽셀단위로 변경해줘야함
        pass



    def move_little_to(self, tx, ty):
        # 여기를 채우시오.
        # get angle
        self.dir = math.atan2(ty - self.y, tx - self.x)
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        pass

    def run_little_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
          # 반대 방향으로 도망가기
        self.dir += math.pi
        distance = RUN_SPEED_PPS * game_framework.frame_time
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)
        pass


    def move_to(self, r=0.5):
        # 여기를 채우시오.
        self.state = 'eagle_1_0'
        self.move_little_to(self.tx, self.ty)

        # 목표 지점에 거의 도착했으면 성공 리턴
        if self.distance_less_than(self.x, self.y, self.tx, self.ty, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def shoot_fether(self):
        self.shoottimer = get_time()
        fether = Fether(self.x, self.y, common.boy)
        game_world.add_object(fether, 1)

        return BehaviorTree.FAIL

        pass



    def canshoottime(self):
        # 마지막 발사 시각과 현재 시간 차가 3초 이상이면 발사 가능
        if get_time() - self.shoottimer >= 3.0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def canshootframe(self):
        # 현재 프레임이 4 또는 5일 때만 발사 가능
        if int(self.frame) in (4, 5):
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL


    def canshootdir(self):
        # 자기 방향(self.dir)의 코사인과 (self.x - boy.x)의 곱이 양수이면 바라보는 방향이 소년 쪽
        if math.cos(self.dir) * (self.x - common.boy.x) < 0:
            return BehaviorTree.SUCCESS
        return BehaviorTree.FAIL

    def set_random_location(self):
        # 여기를 채우시오.
        self.tx = random.randint(100, 1180)
        self.ty = random.randint(100, 924)
        return BehaviorTree.SUCCESS
        pass


    def if_boy_nearby(self, distance):
        # 여기를 채우시오.
        return BehaviorTree.FAIL
        if self.distance_less_than(common.boy.x, common.boy.y, self.x, self.y, distance):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL
        pass


    def move_to_boy(self, r=0.5):
        # 여기를 채우시오.
        self.state = 'eagle_1_0'
        self.move_little_to(common.boy.x, common.boy.y)
        # 소년에 근접했으면 성공 리턴
        if self.distance_less_than(common.boy.x, common.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def run_to_boy(self, r=0.5):
            # 여기를 채우시오.
        self.state = 'eagle_1_0'
        self.run_little_to(common.boy.x, common.boy.y)
            # 소년에 근접했으면 성공 리턴
        if self.distance_less_than(common.boy.x, common.boy.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass


    def get_patrol_location(self):
        # 여기를 채우시오.
        self.tx, self.ty = self.patrol_locations[self.loc_no]
        if self.distance_less_than(self.x, self.y, self.tx, self.ty, 0.5):
            self.loc_no = (self.loc_no + 1) % len(self.patrol_locations)
        return BehaviorTree.SUCCESS
        pass

    def ball_count_check(self):
        return BehaviorTree.SUCCESS
        if common.boy.hp > self.ball_count:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def build_behavior_tree(self): # sequence
        # 여기를 채우시오.
        a1 = Action('목표 지점 설정', self.set_target_location, 1000, 200)
        a2 = Action('목표 지점으로 이동', self.move_to)
        move_to_target_location = Sequence('지정된 목표 지점으로 이동', a1, a2)
        a3 = Action('랜덤 위치 설정', self.set_random_location)
        wander = Sequence('배회', a3, a2)
        c1 = Condition('소년이 근처에 있는가?', self.if_boy_nearby, 7)
        a4 = Action('소년 추적', self.move_to_boy)

        # 발사 관련 Condition 및 Action 추가
        c_shoottime = Condition('발사 시간 조건', self.canshoottime)
        c_shootframe = Condition('발사 프레임 조건', self.canshootframe)
        c_shootdir = Condition('발사 방향 조건', self.canshootdir)
        a_shoot = Action('깃털 발사', self.shoot_fether)
        shoot_seq = Sequence('발사 시퀀스(시간->방향->프레임->발사)', c_shoottime, c_shootdir, c_shootframe, a_shoot)

        c_ball_count = Condition('좀비의 공이 소년보다 많거나 같은가?', self.ball_count_check)
        a_run = Action('소년에게서 도망가기', self.run_to_boy)

        check_and_run = Sequence('공이 많으면 도망가기', c_ball_count, a_run)
        chase_or_run = Selector('추적 또는 도망가기', check_and_run, a4)

        chase_if_boy_nearby = Sequence('소년이 근처에 있으면 추적', c1, chase_or_run)

        chase_or_wander = Selector('소년이 가까이 있으면 추적하고, 아니면 배회', chase_if_boy_nearby, wander)

        a5 = Action('다음 순찰 위치를 가져오기', self.get_patrol_location)
        patrol = Sequence('순찰', a5, a2)

        root = chase_or_patrol = Selector('추적 또는 순찰', chase_if_boy_nearby, patrol)

        root = shoot_or_patrol = Selector('발사 또는 순찰', shoot_seq, chase_if_boy_nearby, patrol)

        self.behavior_tree = BehaviorTree(root)
        pass



