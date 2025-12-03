import random
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector

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

METER = 30

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
        self.y =  180
        self.load_images()
        self.frame = random.randint(0, 3)

        self.count = 1
        self.left = METER / 3
        self.bottom = METER / 2
        self.right = METER / 3
        self.top = METER / 2
        self.now_hp = Boss.max_hp
        # 공격력: 전달받지 않으면 기본값 5
        self.strength = strength
        # 데미지 디바운스용 대기시간 초기화
        self.wait_time = 0
        self.state = IDLE

        # 행동 트리 위한 타이머와 상태 변수
        self.TARGET_SET = False
        self.bx = 0
        self.tx = 1000
        self.inter_cooldown = get_time()
        self.movetime = 0.0

        self.build_behavior_tree()


    def get_bb(self):
        return self.x - self.left * PIXEL_PER_METER, self.y - self.bottom * PIXEL_PER_METER, self.x + self.right * PIXEL_PER_METER, self.y + self.top * PIXEL_PER_METER

    def update(self):
        if self.state != IDLE:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5
        else:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        #self.x = common.boy.x - 6 * PIXEL_PER_METER
        self.behavior_tree.run() # 매 프레임마다 행동 트리 실행




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

    def prepare_chase_target(self):
            # TARGET_SET이 False일 때만 실행 (시퀀스 시작 시 1회 실행됨)
        if not self.TARGET_SET:
            if common.boy.x < common.grass.w / 2:
                self.tx = common.boy.x + 6 * PIXEL_PER_METER  # 목표는 현재 플레이어의 X좌표
            else:
                self.tx = common.boy.x - 6 * PIXEL_PER_METER  # 목표는 현재 플레이어의 X좌표
            self.bx = self.x  # 시작점은 현재 보스의 X좌표
            self.movetime = get_time()  # 이동 시작 시간 기록
            self.TARGET_SET = True  # "설정 완료" 플래그 켜기
            self.state = IDLE

            # 이미 설정되어 있다면 아무것도 하지 않고 성공 반환하여 다음 노드(이동)로 넘어감
        return BehaviorTree.SUCCESS

    def move_linearly(self):
        # 경과 시간 계산
        elapsed_time = get_time() - self.movetime
        duration = 1.0  # 1초 동안 이동

        # 진행률 (0.0 ~ 1.0)
        t = elapsed_time / duration

        # 1초가 아직 안 지났으면 선형 보간 이동
        if t < 1.0:
            # 선형 보간 공식: 시작점 + (목표점 - 시작점) * 진행률
            self.x = self.bx + (self.tx - self.bx) * t
            return BehaviorTree.RUNNING  # 아직 이동 중이므로 RUNNING 반환

        else:
            # 1초가 지났으면 위치를 정확히 목표점으로 맞춤
            self.x = self.tx
            self.state = CRUSH
            self.frame = 0.0  # 공격 모션 시작을 위해 프레임 초기화
            return BehaviorTree.SUCCESS  # 이동 완료

    def check_attack_frame(self):
        # 현재 프레임이 4 이상이면 공격 완료로 판단
        if int(self.frame) >= 4:
            # [중요] 패턴이 완전히 끝났으므로 다음 실행을 위해 플래그를 초기화해줍니다.
            self.TARGET_SET = False
            self.state = IDLE
            self.inter_cooldown = get_time()  # 인터벌 타이머 초기화
            return BehaviorTree.SUCCESS

        # 아직 공격 모션 중(프레임 4 미만)이라면 대기
        return BehaviorTree.RUNNING

    def wait_interval(self):
        if get_time() - self.inter_cooldown >= 3.0:
            return BehaviorTree.FAIL
        else:
            return BehaviorTree.SUCCESS


    def build_behavior_tree(self):
        a_set_target = Action('타겟 위치 고정', self.prepare_chase_target)

        a_move_lerp = Action('선형 보간 이동', self.move_linearly)

        a_check_frame = Action('공격 프레임 확인', self.check_attack_frame)

        # [조립] 추적 후 공격 시퀀스
        root = seq_chase_attack = Sequence('좌표 저장 후 이동 공격', a_set_target, a_move_lerp, a_check_frame)

        a_wait_interval = Action('대기 인터벌', self.wait_interval)

        root = wait_and_attack = Selector('대기 후 공격', a_wait_interval, seq_chase_attack)

        self.behavior_tree = BehaviorTree(root)