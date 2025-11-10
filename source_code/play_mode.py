from pico2d import *
from boy import Boy
from grass import Grass
import game_world
import game_framework
import worldmap_mode
import home_mode
from game_world import world
# Game object class here


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            game_framework.change_mode(worldmap_mode)
        else:
            boy.handle_event(event)


def init():
    global boy
    global running
    running = True
    grass = Grass()
    game_world.add_object(grass, 0)
    boy = Boy()
    game_world.add_object(boy, 1)

    game_world.add_collision_pair('boy:grass', boy, grass)


def finish():
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass

def resume():
    pass
