from pico2d import *
import logo_mode as start_mode
import game_framework


open_canvas()

game_framework.run(start_mode)

close_canvas()


# 플레이모드에 있는 함수들을 메인에서 호출
