from pico2d import load_image, get_time, load_font, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a, SDLK_d

import game_world
from state_machine import StateMachine
import game_framework
from ball import Ball

# 전역 변수로 A키 눌림 상태 저장
attackkeydown = 0
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 30.0            # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


time_per_action = 0.3
frames_per_action = 8
actions_per_time = 1.0 / time_per_action
FRAMES_PER_SEC = frames_per_action * actions_per_time

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
    if Boy.set_balls == 0:
        return False
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d

def attack_hold(e):
    return e[0] == 'ATTACK_HOLD'


# 새 이벤트: dir 기반 상태 전이 트리거용
def run_dir(e):
    return e[0] == 'RUN_DIR'


def idle_dir(e):
    return e[0] == 'IDLE_DIR'


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.wait_time = get_time()
        # dir는 키 이벤트로 관리하므로 여기서 초기화하지 않습니다.

    def exit(self, e):
        if space_down(e):
            self.boy.jump()
        pass

    def do(self):
        self.boy.frame = (FRAMES_PER_SEC * game_framework.frame_time + self.boy.frame) % 6
        if get_time() - self.boy.wait_time > 3: # 슬립 흔적기관
            pass

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 6 * 128, 128, 128, 0, '',
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            #self.boy.image.clip_draw(self.boy.frame * 128, 6 * 128, 128, 128, self.boy.x, self.boy.y)
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 6 * 128, 128, 128, 0, 'h',
                                          self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)


class Attack:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.frame = 0
        if e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_d:
            self.boy.fire_ball()
        pass

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (FRAMES_PER_SEC * game_framework.frame_time + self.boy.frame)
        if self.boy.frame >= 4:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

        if attackkeydown:
            self.boy.state_machine.handle_state_event(('ATTACK_HOLD', None))
            pass

    def handle_event(self, event):
        pass

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 2 * 128, 128, 128, 0, '',
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 2 * 128, 128, 128, 0, 'h',
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

    def exit(self, e):
        if space_down(e):
            self.boy.jump()
        pass

    def do(self):
        self.boy.frame = (FRAMES_PER_SEC * game_framework.frame_time + self.boy.frame) % 7
        self.boy.x += self.boy.dir * RUN_SPEED_PPS * game_framework.frame_time
        if self.boy.x < 0:
            self.boy.x = 0
        elif self.boy.x > 800:
            self.boy.x = 800

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 5 * 128, 128, 128, 0, '',
                                               self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        else:
            self.boy.image.clip_composite_draw(int(self.boy.frame) * 128, 5 * 128, 128, 128, 0, 'h',
                                          self.boy.x, self.boy.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)


class Boy:
    money = 0
    dir = 0
    set_balls = 1
    def __init__(self):
        self.x, self.y = 140, 130
        self.frame = 0
        self.face_dir = 1

        self.yv = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.image = load_image('player_sprite_full.png')

        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.ATTACK: {time_out: self.IDLE, a_up: self.ATTACK},
                # 좌우 키의 직접적인 up/down 이벤트 매핑 제거. dir 상태로 전이 처리
                self.IDLE: {space_down: self.IDLE, a_down: self.ATTACK, a_up: self.IDLE, attack_hold: self.ATTACK,
                            run_dir: self.RUN, d_down: self.ATTACK},
                self.RUN: {space_down: self.RUN, idle_dir: self.IDLE, a_down: self.ATTACK, d_down: self.ATTACK,}
            }
        )

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
        try:
            if event.type == SDL_KEYDOWN:
                if event.key == SDLK_RIGHT:
                    Boy.dir += 1
                    self.face_dir = 1
                elif event.key == SDLK_LEFT:
                    Boy.dir -= 1
                    self.face_dir = -1

            elif event.type == SDL_KEYUP:
                if event.key == SDLK_RIGHT:
                    Boy.dir -= 1
                elif event.key == SDLK_LEFT:
                    Boy.dir += 1
        except Exception:
            # event가 None이거나 구조가 다를 경우 예외 무시
            pass




        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb())
        self.font.draw(15, 580, f'{Boy.money:02d}', (0, 0, 0))

    def fire_ball(self):

        print("Fire Ball!")
        ball = Ball(self.x, self.y, self.face_dir)
        game_world.add_object(ball, 1)

    def get_bb(self):
        return self.x - 15, self.y - 80, self.x + 15, self.y + 5

    def jump(self):
        self.yv = 10
        Boy.money += 1

    def handle_collision(self, group, other):
        if group == 'boy:grass':
            self.yv = 0