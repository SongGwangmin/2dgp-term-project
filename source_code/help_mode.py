from pico2d import *
import game_framework
from plate import Plate
import game_world


def init():
    plate = Plate()
    Plate.image = load_image('help.png')
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
    global boy
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 600 - event.y
            if 100 <= x <= 200 and 400 <= y <= 500:
                game_framework.pop_mode()





def pause():
    pass

def resume():
    pass