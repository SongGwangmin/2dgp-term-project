from pico2d import *
import game_framework
from pannel import Pannel
import game_world
import play_mode
import home_mode
import worldmap_mode

def init():
    global pannel

    pannel = Pannel()
    game_world.add_object(pannel, 2)

def finish():

    global pannel
    game_world.remove_object(pannel)
    del pannel

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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_0:
                play_mode.boy.item = None
                game_framework.pop_mode()
            elif event.key == SDLK_1:
                play_mode.boy.item = 'Ball'
                game_framework.pop_mode()
            elif event.key == SDLK_2:
                play_mode.boy.item = 'BigBall'
                game_framework.pop_mode()
            elif event.key == SDLK_q:
                game_framework.pop_mode() # 아이템 모드에서 빠져나올 때는 홈모드로 돌아가야하므로 pop_mode
                game_framework.change_mode(worldmap_mode)
            else:
                home_mode.boy.handle_event(event)
        else:
            home_mode.boy.handle_event(event)


def pause():
    pass

def resume():
    pass