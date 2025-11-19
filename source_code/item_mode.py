from pico2d import *
import game_framework
from pannel import Pannel
from sold_out import Sold_out
import game_world
import play_mode
import home_mode
import worldmap_mode

def init():
    global pannel
    pannel = Pannel(0)
    Pannel.image = load_image('item_select.png')
    game_world.add_object(pannel, 2)

def finish():

    global pannel
    game_world.remove_object(pannel)
    del pannel

def update():
    game_world.update()
    game_world.handle_collision()
    # 맵 이동 - 오른쪽 끝 == 월드맵
    if home_mode.boy.x > 790:
        game_framework.pop_mode()
        game_framework.change_mode(worldmap_mode)

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
        elif event.type  == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 600 - event.y
            select = pannel.click_colision(x, y)
            if select == 1:
                if home_mode.Boy.money >= 5 and home_mode.Boy.set_slash == 0:
                    home_mode.Boy.money -= 5
                    home_mode.Boy.set_slash = 1
            if select == 2:
                if home_mode.Boy.money >= 5 and home_mode.Boy.set_dash == 0:
                    home_mode.Boy.money -= 5
                    home_mode.Boy.set_dash = 1
            elif select == 3:
                game_framework.pop_mode()

        elif event.type == SDL_MOUSEMOTION:
            x, y = event.x, 600 - event.y
            pannel.mousemove_colision(x, y)
        else:
            home_mode.boy.handle_event(event)


def pause():
    pass

def resume():
    pass