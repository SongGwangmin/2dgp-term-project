from pico2d import *
from boy import Boy
from grass import Grass
import game_world
import game_framework
import trainig_mode
import play_mode
import item_mode
import worldmap_mode
from keycap import Keycap

import common

from game_world import world
# Game object class here

dest_list = []

def handle_events():
    global running

    event_list = get_events()
    for event in event_list:



        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            for k in dest_list:
                if getattr(k, 'enabled', False) and getattr(k, 'dest', None) is not None:
                    try:
                        game_framework.push_mode(k.dest)
                    except Exception:
                        pass
                    break
                else:
                    boy.handle_event(event)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            #game_framework.push_mode(trainig_mode)
            pass
            #push mode: 플레이 모드를 유지해야하므로
        else:
            boy.handle_event(event)


def init():
    global boy
    global running
    global dest_list
    running = True

    game_world.collision_pairs = {}
    Grass.image = load_image('home.png')
    grass = Grass(60)
    game_world.add_object(grass, 0)
    boy = Boy()
    game_world.add_object(boy, 1)
    game_world.add_collision_pair('boy:grass', boy, grass)

    common.boy = boy
    common.grass = grass

    dest_list.clear()
    key1 = Keycap(230, 200, dest=item_mode)
    key2 = Keycap(450, 200, dest=trainig_mode)
    game_world.add_object(key1, 3)
    game_world.add_object(key2, 3)
    dest_list.append(key1)
    dest_list.append(key2)

    game_world.add_collision_pair('boy:portal', boy, None)
    game_world.add_collision_pair('boy:portal', None, key1)
    game_world.add_collision_pair('boy:portal', None, key2)

def finish():
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collision()

    # 맵 이동 - 오른쪽 끝 == 월드맵
    if boy.x > 790:
        game_framework.change_mode(worldmap_mode)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass

def resume():
    pass
