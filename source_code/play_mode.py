from pico2d import *
from boy import Boy
from grass import Grass
import game_world
from game_world import world
# Game object class here


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
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


def finish():
    game_world.clear()

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass

def resume():
    pass
