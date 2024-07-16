import pygame as pg

class Setting():

    def __init__(self):
        self.boundary = (1000, 800)
        self.gameboundary = (self.boundary[0], self.boundary[1]-10)
        self.Black = (0,0,0)
        self.tank_num = 15
        self.color = (255,255,255)    
        self.color_light = (170,170,170)  
        self.color_dark = (100,100,100) 
        self.smallfont = pg.font.SysFont('segoeuiemoji',20)
        self.Bigfont = pg.font.SysFont('segoeuiemoji',70)  