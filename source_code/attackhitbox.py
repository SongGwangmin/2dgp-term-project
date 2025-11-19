from pico2d import draw_rectangle
import game_world
import game_framework


class AttackHitBox:
    # 공격 히트박스: Boy가 생성하지 않음(나중에 연결할 용도)
    def __init__(self, boy=None, width=50, height=50, offset_x=50, offset_y=0):
        self.boy = boy
        self.width = width
        self.height = height
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.enabled = False
        self.x = 0
        self.y = 0

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False

    def update(self):
        # 활성화되어 있으면 항상 보이의 위치에 맞춰 따른다
        if self.boy is None:
            return
        if self.enabled:
            # face_dir가 1이면 오른쪽, -1이면 왼쪽으로 offset 적용
            self.x = self.boy.x + self.offset_x * (self.boy.face_dir if hasattr(self.boy, 'face_dir') else 1)
            self.y = self.boy.y + self.offset_y

    def draw(self):
        if not self.enabled:
            return
        # 히트박스를 시각화하고 싶으면 draw_rectangle 사용
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        # 비활성화 시 충돌을 일으키지 않도록 널 박스 반환
        if not self.enabled:
            return 0, 0, 0, 0
        half_w = self.width / 2
        half_h = self.height / 2
        return self.x - half_w, self.y - half_h, self.x + half_w, self.y + half_h

    def handle_collision(self, group, other):
        # 충돌 처리 후 동작은 사용처에서 구현
        if group == 'attack:zombie':
            # 기본 동작: 히트가 발생하면 비활성화
            self.disable()

