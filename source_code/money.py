from pico2d import load_image, draw_rectangle, load_wav
import game_world
import common

METER = 1.8
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 1 meter

class Money:
    image = None
    se = None

    def __init__(self, x=400, y=300, value=1):
        if Money.image is None:
            Money.image = load_image('money.png')
        if Money.se is None:
            Money.se = load_wav('se/coin.mp3')
        self.x = x
        self.y = y
        self.value = value
        # 보이지 않음: 충돌 시에만 보이도록
        self.enabled = False

    def draw(self):
        sx = self.x - common.grass.left
        Money.image.clip_composite_draw(0, 0, 265, 257, 0, '',
                                               sx, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        #draw_rectangle(*self.get_windowbb())

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

    def get_windowbb(self):
        sx = self.x - common.grass.left

        cx = sx
        cy = self.y
        half_w = 50 / 2
        half_h = 50 / 2
        left = cx - half_w
        bottom = cy - half_h
        right = cx + half_w
        top = cy + half_h
        return left, bottom, right, top

    def handle_collision(self, group, other):
        # 'boy:money' 충돌 시 보상 지급 및 자신 제거
        if group == 'boy:money':
            Money.se.play()
            # 자신을 월드에서 제거
            game_world.remove_object(self)

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
