from pico2d import *
import game_framework
from plate import Plate
import game_world

plate = None


def init():
    global plate
    plate = Plate()
    Plate.image = load_image('help.png')
    game_world.add_object(plate, 3)


def finish():
    global plate
    if plate is not None:
        game_world.remove_object(plate)
        plate = None


def update():
    game_world.update()
    game_world.handle_collision()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def handle_events():
    event_list = get_events()

    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_MOUSEBUTTONDOWN:
            x, y = event.x, 600 - event.y
            if 100 <= x <= 200 and 400 <= y <= 500:
                game_framework.pop_mode()


def pause():
    pass


def resume():
    pass