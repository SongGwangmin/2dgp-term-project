from pico2d import *
import game_framework
from plate import Plate
import game_world
import home_mode

def find_boy():
    """game_world.world를 순회하여 클래스 이름이 'Boy'인 객체를 찾아 반환합니다.
    다른 모듈과의 순환 import 문제를 피하기 위해 __class__.__name__으로 비교합니다.
    이 함수는 호출만 할 뿐, 자동으로 다른 곳에서 호출되지는 않습니다.
    """
    for layer in game_world.world:
        for o in layer:
            if o.__class__.__name__ == 'Boy':
                return o
    return None

boy = None

def init():
    plate = Plate()
    game_world.add_object(plate, 3)
    global boy
    boy = find_boy()

def finish():
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collision()

    # 아이템 모드에서 플레이모드가 유지가 되어야 하므로 게임 월드를 계속 업데이트 해줘야한다

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
    pass

def handle_events():
    global boy
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            game_framework.pop_mode()
            game_framework.change_mode(home_mode)
        else:
            boy.handle_event(event)




def pause():
    pass

def resume():
    pass