from pico2d import load_image, draw_rectangle

class Money:
    image = None

    def __init__(self, x=400, y=300, value=1):
        if Money.image is None:
            Money.image = load_image('money.png')
        self.x = x
        self.y = y
        self.value = value
        # 보이지 않음: 충돌 시에만 보이도록
        self.enabled = False

    def draw(self):
        # 바운딩 박스는 디버그용으로 항상 그림
        draw_rectangle(*self.get_bb())
        if not self.enabled:
            return
        if Money.image:
            Money.image.draw(self.x, self.y)

    def update(self):
        # 각 프레임 기본적으로 비활성화하고, 충돌 처리에서 enable()로 켬
        self.enabled = False

    def get_bb(self):
        cx = self.x
        cy = self.y
        half_w = 50 / 2
        half_h = 50 / 2
        left = cx - half_w
        bottom = cy - half_h
        right = cx + half_w
        top = cy + half_h
        return left, bottom, right, top

    def handle_collision(self, group, other):
        # 'boy:money' 충돌 시 활성화(필요시 다른 동작 추가)
        if group == 'boy:money':
            self.enable()
