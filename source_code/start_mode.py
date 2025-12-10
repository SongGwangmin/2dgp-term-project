from pico2d import *
import game_framework
from grass import Grass
import game_world
import help_mode
import home_mode
import common
from boy import Boy

def init():
    grass = Grass()
    Grass.bgm.set_volume(32)
    Grass.bgm.repeat_play()
    Grass.image = load_image('start.png')
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
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 600 - event.y
            if 300 <= x <= 500 and 100 <= y <= 200:
                game_framework.change_mode(home_mode)
            elif 300 <= x <= 500 and 0 <= y <= 100:
                game_framework.push_mode(help_mode)





def pause():
    pass

def resume():
    pass