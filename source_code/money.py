from pico2d import load_image, draw_rectangle
import game_world


METER = 1.8
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 1 meter

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
        Money.image.clip_composite_draw(0, 0, 265, 257, 0, '',
                                               self.x, self.y, METER * PIXEL_PER_METER, METER * PIXEL_PER_METER)
        draw_rectangle(*self.get_bb())

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
        if group == 'attack:zombie':
            # 일정 시간(ATTACK_WAIT_TIME) 동안은 추가 데미지를 받지 않도록 디바운스
            if get_time() - self.wait_time >= ATTACK_WAIT_TIME:
                self.wait_time = get_time()
                self.now_hp -= other.strength
                if self.now_hp > 0:
                    # 맞은 곳과 반대로 튕겨야함
                    dx = self.x - other.x
                    if dx == 0:
                        self.knockbackdir = 0.0
                    else:
                        # dx / math.fabs(dx)는 dx의 부호(+1 또는 -1)를 반환
                        self.knockbackdir = dx / math.fabs(dx)
                    self.knockbackspeed = 5
                    pass
                else:
                    # 죽을 때 돈을 드롭
                    money = Money(self.x, self.y, value=5)
                    game_world.add_object(money, 1)
                    # boy:money 충돌 페어에 몬스터 드랍 등록
                    game_world.add_collision_pair('boy:money', None, money)
                    game_world.remove_object(self)
                    other.boy_pointer.hunt_count += 1

    def enable(self):
        self.enabled = True

    def disable(self):
        self.enabled = False
