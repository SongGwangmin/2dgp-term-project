from pico2d import draw_rectangle, get_time
import game_world
import game_framework
import common


class BossAttackHitBox:
    # 공격 히트박스: Boy가 생성하지 않음(나중에 연결할 용도)
    def __init__(self, boss=None, width=50, height=50, x=50, y=0):
        self.boss_pointer = boss
        self.width = width
        self.height = height
        self.strength = boss.strength  # 공격력
        self.x = x
        self.y = 80
        self.timer = get_time()


    def update(self):
        if get_time() - self.timer > 0.2:
            game_world.remove_object(self)

    def draw(self):

        #draw_rectangle(*self.get_windowbb())

    def get_bb(self):

        half_w = self.width / 2
        half_h = self.height / 2
        return self.x - half_w, self.y - half_h , self.x + half_w, self.y + half_h

    def get_windowbb(self):


        sx = self.x - common.grass.left
        half_w = self.width / 2
        half_h = self.height / 2
        return sx - half_w, self.y - half_h, sx + half_w, self.y + half_h

    def handle_collision(self, group, other):
        # 충돌 처리 후 동작은 사용처에서 구현
        if group == 'boy:enemy':
            pass

