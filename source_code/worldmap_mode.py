from pico2d import *
from boy import Boy
from grass import Grass
import game_world
import game_framework
import home_mode
import play_mode
from game_world import world
from keycap import Keycap

# 현재 프레임에서 활성화된 Keycap 목적지들을 보관
dest_list = []
# Game object class here


def handle_events():
    global running

    event_list = get_events()
    for event in event_list:
        # 스페이스 키로 활성화된 Keycap의 목적지로 이동
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            for k in dest_list:
                if getattr(k, 'enabled', False) and getattr(k, 'dest', None) is not None:
                    try:
                        game_framework.change_mode(k.dest)
                    except Exception:
                        pass
                    break

        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_q:
            game_framework.change_mode(home_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.change_mode(play_mode)
            #game_framework.change_mode(title_mode)
        #elif event.type == SDL_KEYDOWN and event.key == SDLK_i:
            #game_framework.push_mode(item_mode)
            # push mode: 플레이 모드를 유지해야하므로
        else:
            boy.handle_event(event)


def init():
    global boy
    global running
    global dest_list
    running = True

    game_world.collision_pairs = {}

    Grass.image = load_image('map.PNG')

    grass = Grass(30)
    game_world.add_object(grass, 0)
    boy = Boy()
    game_world.add_object(boy, 1)
    game_world.add_collision_pair('boy:grass', boy, grass)

    # 월드맵에 Keycap 추가 (space 아이콘)
    # init마다 dest_list 비우고 새로 채움
    dest_list.clear()
    key1 = Keycap(30, 200, dest=home_mode)
    key2 = Keycap(250, 200, dest=play_mode)
    game_world.add_object(key1, 3)
    game_world.add_object(key2, 3)
    dest_list.append(key1)
    dest_list.append(key2)

    # boy와 Keycap 간 충돌 페어 등록: 'boy:portal'
    # 패턴: 먼저 boy를 왼쪽에 등록하고, 우측 객체들을 별도로 등록
    game_world.add_collision_pair('boy:portal', boy, None)
    game_world.add_collision_pair('boy:portal', None, key1)
    game_world.add_collision_pair('boy:portal', None, key2)


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
