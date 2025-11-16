from pico2d import *
from boy import Boy
from grass import Grass
import game_world
import game_framework
import worldmap_mode
from zombie import Zombie
import home_mode
from game_world import world
# Game object class here

max_monster_count = 4


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
    game_world.collision_pairs = {}
    Grass.image = load_image('forest.png')
    grass = Grass()
    game_world.add_object(grass, 0)
    boy = Boy()
    game_world.add_object(boy, 1)

    game_world.add_collision_pair('boy:grass', boy, grass)
    zombies = [Zombie() for i in range(max_monster_count)]
    game_world.add_objects(zombies, 1)

    for zombie in zombies:
        game_world.add_collision_pair('boy:zombie', None, zombie)
        game_world.add_collision_pair('ball:zombie', None, zombie)


def finish():
    game_world.clear()

def update():
    game_world.update()
    game_world.handle_collision()
    if boy.x > 790 or boy.x < 10:
        game_framework.change_mode(worldmap_mode)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass

def resume():
    pass
