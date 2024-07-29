import pygame as pg
import Game_System
import Game_Setting

if __name__ == "__main__":
    pg.init()
    setting = Game_Setting.Setting()
    programIcon = pg.image.load("icon/icon.png")
    pg.display.set_icon(programIcon)
    pg.display.set_caption("Tank War")
    screen = pg.display.set_mode(setting.boundary)

    # Start Game.
    Game_System.Game_Menue(screen, setting)
