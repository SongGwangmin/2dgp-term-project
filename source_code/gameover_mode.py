from pico2d import *
import game_framework
from plate import Plate
import game_world
import home_mode

def init():
    plate = Plate()
    game_world.add_object(plate, 3)

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
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_r:
            game_framework.pop_mode()
            game_framework.change_mode(home_mode)




def pause():
    pass

def resume():
    pass