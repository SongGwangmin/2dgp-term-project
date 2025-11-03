from pico2d import load_image, get_time
from sdl2 import SDL_KEYDOWN, SDLK_SPACE, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_a

import game_world
from state_machine import StateMachine
from ball import Ball

# 전역 변수로 A키 눌림 상태 저장
attackkeydown = 0


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


def attack_hold(e):
    return e[0] == 'ATTACK_HOLD'


class Idle:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.wait_time = get_time()
        self.boy.dir = 0

    def exit(self, e):
        if space_down(e):
            self.boy.fire_ball()
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 6
        if get_time() - self.boy.wait_time > 3:
            pass

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 128, 6 * 128, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_draw(self.boy.frame * 128, 6 * 128, 128, 128, self.boy.x, self.boy.y)


class Attack:

    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        self.boy.frame = 0
        pass

    def exit(self, e):
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1)
        if self.boy.frame >= 4:
            self.boy.state_machine.handle_state_event(('TIMEOUT', None))

    def handle_event(self, event):
        pass

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 128, 2 * 128, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_draw(self.boy.frame * 128, 2 * 128, 128, 128, self.boy.x, self.boy.y)


class Run:
    def __init__(self, boy):
        self.boy = boy

    def enter(self, e):
        if right_down(e) or left_up(e):
            self.boy.dir = self.boy.face_dir = 1
        elif left_down(e) or right_up(e):
            self.boy.dir = self.boy.face_dir = -1

    def exit(self, e):
        if space_down(e):
            self.boy.fire_ball()
        pass

    def do(self):
        self.boy.frame = (self.boy.frame + 1) % 7
        self.boy.x += self.boy.dir * 5

    def draw(self):
        if self.boy.face_dir == 1:
            self.boy.image.clip_draw(self.boy.frame * 128, 5 * 128, 128, 128, self.boy.x, self.boy.y)
        else:
            self.boy.image.clip_draw(self.boy.frame * 128, 5 * 128, 128, 128, self.boy.x, self.boy.y)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('player_sprite_full.png')

        self.IDLE = Idle(self)
        self.ATTACK = Attack(self)
        self.RUN = Run(self)
        self.state_machine = StateMachine(
            self.IDLE,
            {
                self.ATTACK: {time_out: self.IDLE},
                self.IDLE: {space_down: self.IDLE, a_down: self.ATTACK, attack_hold: self.ATTACK,
                            right_down: self.RUN, left_down: self.RUN,
                            right_up: self.RUN, left_up: self.RUN},
                self.RUN: {space_down: self.RUN, right_up: self.IDLE, left_up: self.IDLE, right_down: self.IDLE,
                           left_down: self.IDLE}}
        )

    def update(self):
        self.state_machine.update()
        # A키가 눌려있으면 매 프레임 ATTACK_HOLD 이벤트 발생
        if attackkeydown:
            self.state_machine.handle_state_event(('ATTACK_HOLD', None))

    def handle_event(self, event):
        # 키 상태를 먼저 갱신
        global attackkeydown
        if event.type == SDL_KEYDOWN and event.key == SDLK_a:
            attackkeydown = 1
        elif event.type == SDL_KEYUP and event.key == SDLK_a:
            attackkeydown = 0
            
        self.state_machine.handle_state_event(('INPUT', event))
        pass

    def draw(self):
        self.state_machine.draw()

    def fire_ball(self):
        print("Fire Ball!")
        ball = Ball(self.x, self.y, self.face_dir * 10)
        game_world.add_object(ball, 1)