from pico2d import load_image, draw_rectangle
import game_world

class Keycap:
    image = None

    def __init__(self, x=400, y=300):
        if Keycap.image is None:
            Keycap.image = load_image('space.png')
        self.x = x
        self.y = y
        # 기본적으로 비활성화: 충돌 시에만 보이게 함
        self.enabled = False

    def draw(self):
        # 활성화되어 있을 때만 이미지와 바운딩 박스를 그림
        if not self.enabled:
            return
        if Keycap.image:
            Keycap.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        # game_world를 검사하여 Boy와 충돌 중인지 확인
        colliding = False
        for layer in game_world.world:
            for o in layer:
                if o.__class__.__name__ == 'Boy':
                    try:
                        if game_world.collide(self, o):
                            colliding = True
                            break
                    except Exception:
                        # 안전하게 무시
                        pass
            if colliding:
                break
        self.enabled = colliding

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

    def handle_collision(self, group, other):
        # 'boy:portal'과 충돌하면 활성화하여 space 아이콘을 보이게 함
        if group == 'boy:portal':
            self.enable()

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
