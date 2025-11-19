from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_d, SDLK_LSHIFT

import game_world
from state_machine import StateMachine
import game_framework
from ball import Ball
from attackhitbox import AttackHitBox

# 전역 변수로 A키 눌림 상태 저장
attackkeydown = 0
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0            # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

#km/h -> m/s : 1000/3600 = 1/3.6
# 그럼 대시 스피드는 dash_speed * 1/3.6 * PIXEL_PER_METER
DELTA_DASH_SPEED_KMPH = 360



time_per_action = 0.3
frames_per_action = 8
actions_per_time = 1.0 / time_per_action
FRAMES_PER_SEC = frames_per_action * actions_per_time

attacktime_per_action = 0.3
attackframes_per_action = 4
attackactions_per_time = 1.0 / attacktime_per_action
ATTACK_FRAMES_PER_SEC = attackframes_per_action * attackactions_per_time

# Hit 상태를 위한 짧은 애니메이션(프레임 수 2)
hit_time_per_action = 0.2
hit_frames_per_action = 2
hit_actions_per_time = 1.0 / hit_time_per_action
HIT_FRAMES_PER_SEC = hit_frames_per_action * hit_actions_per_time

# Death 상태를 위한 애니메이션 설정
death_time_per_action = 0.3
death_frames_per_action = 4
death_actions_per_time = 1.0 / death_time_per_action
DEATH_FRAMES_PER_SEC = death_frames_per_action * death_actions_per_time

METER = 5

GRAVITY = 9.8  # 중력 가속도 (m/s²)

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

time_out = lambda e: e[0] == 'TIMEOUT'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def a_down(e):
    global attackkeydown
    if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a:
        attackkeydown = 1
        return True
    return False


def a_up(e):
    global attackkeydown
    if e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_a:
        attackkeydown = 0
        return True
    return False

def d_down(e):
    if Boy.set_slash == 0:
        return False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def attack_hold(e):
    return e[0] == 'ATTACK_HOLD'


# 새 이벤트: dir 기반 상태 전이 트리거용
def run_dir(e):
    return e[0] == 'RUN_DIR'


def idle_dir(e):
    return e[0] == 'IDLE_DIR'

def shift_down(e):
    if Boy.set_dash == 0:
        return False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT

# 적 충돌 이벤트 판정
def enemy_collide(e):
    return e[0] == 'ENEMY_COLIDE'

# 적 사망(보이 사망) 이벤트
def enemy_death(e):
    if e[0] == 'ENEMY_DEATH':
        Boy.frame = 0
        return True
    return False


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.dash = False
        # dir는 키 이벤트로 관리하므로 여기서 초기화하지 않습니다.

    def exit(self, e):
        if space_down(e):
            if self.boy.yv == 0 and self.boy.y <= 130:
                self.boy.jump()
        pass

    def do(self):
        Boy.frame = (FRAMES_PER_SEC * game_framework.frame_time + Boy.frame) % 6


    def draw(self):
        if self.boy.face_dir == 1:
            charinpit = ''
        else:
            charinpit = 'h'

        if self.boy.yv == 0 and self.boy.y <= 130:
            self.boy.image.clip_composite_draw(int(Boy.frame) * 128, 6 * 128, 128, 128, 0, charinpit,
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)

        else:
            # self.boy.image.clip_draw(self.boy.frame * 128, 6 * 128, 128, 128, self.boy.x, self.boy.y)
            self.boy.image.clip_composite_draw(2 * 128, 4 * 128, 128, 128, 0, charinpit,
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER,
                                               METER * PIXEL_PER_METER)


class Attack:

    def __init__(self, boy):
        self.boy = boy


    def enter(self, e):
        Boy.frame = 0
        self.attack_dir = self.boy.face_dir
        if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d:
            self.boy.fire_ball()
        # 시작 시 히트박스 비활성화
        if hasattr(self.boy, 'attack_hitbox'):
            self.boy.attack_hitbox.disable()
        pass

    def exit(self, e):
        # 상태 종료 시 히트박스 비활성화 보장
        if (self.boy, 'attack_hitbox'):
            self.boy.attack_hitbox.disable()
        pass

    def do(self):
        Boy.frame = (ATTACK_FRAMES_PER_SEC * game_framework.frame_time + Boy.frame)
        # 프레임 인덱스 기반 히트박스 제어: 정확히 2일 때 활성화, 4 이상이면 비활성화
        try:
            frame_idx = int(Boy.frame)
        except Exception:
            frame_idx = 0
        if hasattr(self.boy, 'attack_hitbox'):
            if frame_idx == 2:
                self.boy.attack_hitbox.enable()
            elif frame_idx >= 4:
                self.boy.attack_hitbox.disable()
            else:
                self.boy.attack_hitbox.disable()

        if Boy.frame >= 4:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

        if attackkeydown:
            self.boy.state_machine.handle_state_event(('ATTACK_HOLD', None))
            pass

    def handle_event(self, event):
        pass

    def draw(self):
        if self.attack_dir == 1:
            self.boy.image.clip_composite_draw(int(Boy.frame) * 128, 2 * 128, 128, 128, 0, '',
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            self.boy.image.clip_composite_draw(int(Boy.frame) * 128, 2 * 128, 128, 128, 0, 'h',
                                          self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)


class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        # dir은 handle_event에서 관리되므로 여기서는 face_dir만 갱신
        if self.boy.dir > 0:
            self.boy.face_dir = 1
        elif self.boy.dir < 0:
            self.boy.face_dir = -1

        if shift_down(e):
            if self.boy.dash == False:
                self.boy.dash = True
                self.boy.dash_speed = RUN_SPEED_KMPH * 3
        else:
            self.boy.dash = False

    def exit(self, e):
        if space_down(e):
            if self.boy.yv == 0 and self.boy.y <= 130:
                self.boy.jump()
        pass

    def do(self):
        Boy.frame = (FRAMES_PER_SEC * game_framework.frame_time + Boy.frame) % 7
        if self.boy.dash:
            self.boy.x += self.boy.dir * self.boy.dash_speed * 1/3.6 * PIXEL_PER_METER * game_framework.frame_time
            self.boy.dash_speed -= DELTA_DASH_SPEED_KMPH * game_framework.frame_time
            if self.boy.dash_speed < RUN_SPEED_KMPH / 2:
                self.boy.dash = False
        else:
            self.boy.x += self.boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.boy.x < 0:
            self.boy.x = 0
        elif self.boy.x > 800:
            self.boy.x = 800



    def draw(self):
        if self.boy.face_dir == 1:
            charinpit = ''
        else:
            charinpit = 'h'

        if self.boy.dash:
            self.boy.image.clip_composite_draw(5 * 128, 5 * 128, 128, 128, 0, charinpit,
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER,
                                               METER * PIXEL_PER_METER)
        elif self.boy.yv == 0 and self.boy.y <= 130:
            self.boy.image.clip_composite_draw(int(Boy.frame) * 128, 5 * 128, 128, 128, 0, charinpit,
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            # self.boy.image.clip_draw(self.boy.frame * 128, 6 * 128, 128, 128, self.boy.x, self.boy.y)
            self.boy.image.clip_composite_draw(2 * 128, 4 * 128, 128, 128, 0, charinpit,
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER,
                                               METER * PIXEL_PER_METER)



class Hit:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        # 히트 시작 시 프레임 초기화
        Boy.frame = 0

    def exit(self, e):
        pass

    def do(self):
        # 짧은 히트 애니메이션 진행, 프레임이 끝나면 IDLE로 전이
        Boy.frame = (HIT_FRAMES_PER_SEC * game_framework.frame_time + Boy.frame)
        if Boy.frame >= hit_frames_per_action:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def handle_event(self, event):
        pass

    def draw(self):
        # 히트 애니메이션 그리기 (attack과 비슷한 방식으로 처리)
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(int(Boy.frame) * 128, 3 * 128, 128, 128, 0, '',
                                                self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            self.boy.image.clip_composite_draw(int(Boy.frame) * 128, 3 * 128, 128, 128, 0, 'h',
                                                self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)


class Death:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        pass

    def exit(self, e):
        pass

    def do(self):
        # 죽음 애니메이션 진행, 끝나면 게임오버 모드로 전환
        Boy.frame = (DEATH_FRAMES_PER_SEC * game_framework.frame_time + Boy.frame)
        if Boy.frame >= death_frames_per_action:
            try:
                import gameover_mode
                game_framework.push_mode(gameover_mode)
            except Exception:
                pass


    def draw(self):
        # 죽음 애니메이션 그리기 (임시로 Hit과 다른 행을 사용)
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(min(int(Boy.frame), 3) * 128, 0 * 128, 128, 128, 0, '',
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            self.boy.image.clip_composite_draw(min(int(Boy.frame), 3) * 128, 0 * 128, 128, 128, 0, 'h',
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)


class Boy:
    money = 20
    dir = 0
    frame = 0
    set_slash = 0
    set_dash = 0
    strength = 1
    max_hp = 100.0
    hpbar = None
    hpblank = None
    def __init__(self):
        self.x, self.y = 140, 130
        self.face_dir = 1
        self.yv = 0
        # wait_time을 init에서 초기화해 Idle.enter와 충돌 처리에서 사용
        self.wait_time = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.image = load_image('player_sprite_full.png')
        self.dash = False
        self.dash_speed = 0.0
        self.hunt_count = 0
        self.now_hp = Boy.max_hp
        if Boy.hpbar == None:
            Boy.hpbar = load_image('hpbar.png')
        if Boy.hpblank == None:
            Boy.hpblank = load_image('hpblank.png')
        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.RUN = Run(self)
        self.HIT = Hit(self)
        self.DEATH = Death(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.ATTACK: {time_out: self.IDLE, a_up: self.ATTACK, enemy_collide: self.HIT, enemy_death: self.DEATH},
                # 좌우 키의 직접적인 up/down 이벤트 매핑 제거. dir 상태로 전이 처리
                self.IDLE: {space_down: self.IDLE, a_down: self.ATTACK, a_up: self.IDLE, attack_hold: self.ATTACK,
                            run_dir: self.RUN, d_down: self.ATTACK, enemy_collide: self.HIT, enemy_death: self.DEATH},
                self.RUN: {space_down: self.RUN, idle_dir: self.IDLE, a_down: self.ATTACK, d_down: self.ATTACK,
                           shift_down: self.RUN, enemy_collide: self.HIT, enemy_death: self.DEATH},
                self.HIT: {time_out: self.IDLE},
                self.DEATH: {run_dir: self.DEATH, idle_dir: self.DEATH}
            }
        )

        # 생성 시 공격 히트박스 하나를 만들어 self에 저장하고 game_world에 등록
        self.attack_hitbox = AttackHitBox(self, width=60, height=40, offset_x=50, offset_y=10)
        game_world.add_object(self.attack_hitbox)
        game_world.add_collision_pair('attack:zombie', self.attack_hitbox, None)

    def update(self):
        self.state_machine.update()
        # A키가 눌려있으면 매 프레임 ATTACK_HOLD 이벤트 발생
        if attackkeydown:
            self.state_machine.handle_state_event(('ATTACK_HOLD', None))

        if Boy.dir != 0:
            self.state_machine.handle_state_event(('RUN_DIR', self))
        else:
            self.state_machine.handle_state_event(('IDLE_DIR', self))

        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER
        self.yv -= GRAVITY * game_framework.frame_time  # m/s

        # dir 기반 상태 전이 이벤트는 handle_event에서 방향키 입력이 있을 때만 보냄
        pass

    def handle_event(self, event):
        # 방향키 상태를 누를 때마다 dir을 ++/-- 하여 여러 키 동시 입력도 처리
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_RIGHT:
                Boy.dir += 1
                self.face_dir = 1
            elif event.key == SDLK_LEFT:
                Boy.dir -= 1
                self.face_dir = -1
            print(Boy.dir)
        elif event.type == SDL_KEYUP:
            if event.key == SDLK_RIGHT:
                Boy.dir -= 1
            elif event.key == SDLK_LEFT:
                Boy.dir += 1
            print(Boy.dir)

        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        self.font.draw(15, 570, f'money: {Boy.money:02d}$', (255, 255, 0))
        Boy.hpblank.clip_draw_to_origin(0, 0, 5, 5, 10, 580, 200, 5)
        Boy.hpbar.clip_draw_to_origin(0, 0, 5, 5, 10, 580, 200 * (self.now_hp / Boy.max_hp), 5)


    def fire_ball(self):
        print("Fire Ball!")
        ball = Ball(self.x, self.y, self.face_dir, self)
        game_world.add_object(ball, 1)
        game_world.add_collision_pair('attack:zombie', ball, None)

    def get_bb(self):
        return self.x - 15, self.y - 80, self.x + 15, self.y + 5

    def jump(self):
        self.yv = 10
        #Boy.money += 10

    def handle_collision(self, group, other):
        if group == 'boy:grass':
            self.yv = 0
        # 적과 충돌하면 wait_time으로 디바운스 체크 후 ENEMY_COLIDE 또는 ENEMY_DEATH 이벤트 발생
        if group == 'boy:enemy':
            if get_time() - self.wait_time >= hit_time_per_action * 2:
                self.now_hp -= other.strength
                if self.now_hp <= 0:
                    self.now_hp = 0
                    self.wait_time = get_time()
                    self.state_machine.handle_state_event(('ENEMY_DEATH', other))
                else:
                    self.wait_time = get_time()
                    self.state_machine.handle_state_event(('ENEMY_COLIDE', other))
