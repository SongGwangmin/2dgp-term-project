from pico2d import load_image, draw_rectangle
import game_world
import common

class Keycap:
    image = None

    def __init__(self, x=400, y=300, dest=None):
        if Keycap.image is None:
            Keycap.image = load_image('space.png')
        self.x = x
        self.y = y
        # 목적지 모듈(예: home_mode, play_mode)을 저장
        self.dest = dest
        # 기본적으로 비활성화: 충돌 시에만 보이게 함
        self.enabled = False

    def draw(self):
        draw_rectangle(*self.get_windowbb())
        # 활성화되어 있을 때만 이미지를 그림
        if not self.enabled:
            return
        if Keycap.image:
            sx = self.x - common.grass.left

            Keycap.image.draw(sx, self.y)


    def update(self):
        # 매 프레임 기본적으로 비활성화하고, game_world.handle_collision()에서
        # 충돌이 감지되면 handle_collision이 호출되어 enable()로 상태를 바꿉니다.
        # (game loop 순서: update() -> handle_collision() -> draw())
        self.enabled = False

    def get_bb(self):
        # 중심을 (self.x, self.y - 100)으로 하고, 너비 50, 높이 40으로 바운딩 박스 반환
        cx = self.x
        cy = self.y - 100
        half_w = 50 / 2
        half_h = 40 / 2
        left = cx - half_w
        bottom = cy - half_h
        right = cx + half_w
        top = cy + half_h
        return left, bottom, right, top

    def get_windowbb(self):
        sx = self.x - common.grass.left

        cx = sx
        cy = self.y - 100
        half_w = 50 / 2
        half_h = 40 / 2
        left = cx - half_w
        bottom = cy - half_h
        right = cx + half_w
        top = cy + half_h
        return left, bottom, right, top

    def handle_collision(self, group, other):
        # 'boy:portal'과 충돌하면 활성화하여 space 아이콘을 보이게 함
        if group == 'boy:portal':
            self.enable()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
