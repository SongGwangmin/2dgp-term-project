from pico2d import *
from boy import Boy
from grass import Grass
from place import Place
import game_world
import game_framework
import worldmap_mode

from angry_bird import Angry_Bird
import ending
import common
from boss import Boss

# Game object class here

max_monster_count = 1

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            boy.handle_event(event)


def init():
    global boy
    global running
    running = True
    game_world.collision_pairs = {}
    Grass.image = load_image('bossmap.png')
    boy = Boy()
    game_world.add_object(boy, 2)

    common.boy = boy

    grass = Grass()
    game_world.add_object(grass, 0)

    common.grass = grass

    place = Place()
    game_world.add_object(place, 1)

    boss = Boss()
    game_world.add_object(boss, 1)



    game_world.add_collision_pair('boy:grass', boy, grass)

    # 충돌 페어 등록 (소년-적, 공격-적)
    game_world.add_collision_pair('boy:enemy', boy, None)
    #game_world.add_collision_pair('boy:enemy', None, boss)
    game_world.add_collision_pair('attack:zombie', None, boss)
    # Money 오브젝트 추가 및 충돌 페어 등록
    game_world.add_collision_pair('boy:money', boy, None)


def finish():
    game_world.clear()


def update():
    game_world.update()
    game_world.handle_collision()
    if boy.x < 10:
        game_framework.change_mode(worldmap_mode)
    elif common.grass.w - 10 <= boy.x and max_monster_count <= boy.hunt_count: # 오른쪽 끝 && 몬스터 다 잡음
        print("Boss Defeated! Ending Mode로 이동")
        if Boy.level < 5:
            Boy.level = 5
        game_framework.change_mode(ending)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass

