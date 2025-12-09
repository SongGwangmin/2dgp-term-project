from pico2d import *
import game_framework
from grass import Grass
import game_world
import common
from boy import Boy

def init():
    grass = Grass()
    Grass.image = load_image('ending.png')
    game_world.add_object(grass, 3)
    common.grass = grass
    common.boy = Boy()
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






def pause():
    pass

def resume():
    pass