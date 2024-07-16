import pygame as pg
import os
import numpy as np
from threading import Thread
import Game_System

class Tank:
    def __init__(self, x, y, HP, Attack, defense, speed, bullet_speed, boundary, random, screen, type):

        self.screen = screen

        self.x = x
        self.y = y

        self.HP = HP
        self.Attack = Attack
        self.defense = defense
        self.speed = speed
        self.move = 0
        self.type= type

        self.direction = "Up"
        self.bullet_direction = "Up"
        self.bullet_speed = bullet_speed + self.speed
        self.boundary = boundary
        self.destory = False
        self.fire_status = False
        self.random = random
        self.BOOMS = ["./boom/" + file for file in os.listdir("./boom")]

    def Born_Hero(self):
        # load Hero Tank image.
        self.tank_L = pg.image.load("./enemy/MyTankLeft.png")
        self.tank_L_rect = self.tank_L.get_rect()
        self.tank_R = pg.image.load("./enemy/MyTankRight.png")
        self.tank_R_rect = self.tank_R.get_rect()
        self.tank_U = pg.image.load("./enemy/MyTankUp.png")
        self.tank_U_rect = self.tank_U.get_rect()
        self.tank_D = pg.image.load("./enemy/MyTankDown.png")
        self.tank_D_rect = self.tank_D.get_rect()

        # Load Bullet Image
        self.bullet = pg.image.load("./bullet/bullet.png").convert()
        self.bullet_rect = self.bullet.get_rect()

        # Load Tank Image.
        self.image = self.tank_U
        self.image_rect = self.tank_U_rect
        self.Reload_Bullet()

    def Born_NPC(self):
        if self.type == 0:
            f = ["./enemy/GrayLeft.png",
                    "./enemy/GrayRight.png",
                    "./enemy/GrayUp.png", 
                    "./enemy/GrayDown.png" ]
        elif self.type == 1:
            f = ["./enemy/GreenLeft.png",
                    "./enemy/GreenRight.png",
                    "./enemy/GreenUp.png", 
                    "./enemy/GreenDown.png" ]
        elif self.type == 2:
            f = ["./enemy/YellowLeft.png",
                    "./enemy/YellowRight.png",
                    "./enemy/YellowUp.png", 
                    "./enemy/YellowDown.png" ]    
        elif self.type == 3:
            f = ["./enemy/QuickLeft.png",
                    "./enemy/QuickRight.png",
                    "./enemy/QuickUp.png", 
                    "./enemy/QuickDown.png" ]

        # load Hero Tank image.
        self.tank_L = pg.image.load(f[0])
        self.tank_L_rect = self.tank_L.get_rect()
        self.tank_R = pg.image.load(f[1])
        self.tank_R_rect = self.tank_R.get_rect()
        self.tank_U = pg.image.load(f[2])
        self.tank_U_rect = self.tank_U.get_rect()
        self.tank_D = pg.image.load(f[3])
        self.tank_D_rect = self.tank_D.get_rect()

        # Load Bullet image
        self.bullet = pg.image.load("./bullet/bullet.png").convert()
        self.bullet_rect = self.bullet.get_rect()

        # Load Tank Image.
        self.image = self.tank_U
        self.image_rect = self.tank_U_rect
        self.Reload_Bullet()

    def Buff(self, type):
        if type == 0:
            self.HP +=5
        elif type == 1:
            self.Attack += 5
        elif type == 2:
            self.defense += 5
        elif type == 3:
            if self.speed <= 3:
                self.speed += 0.5
                self.bullet_speed += 0.5
        
    def Random_Walk(self):
        if self.random == True:
            self.direction = np.random.choice(["Up", "Down", "Left", "Right"])

        if self.direction == "Up":
            self.image = self.tank_U
            self.image_rect = self.tank_U_rect
        elif self.direction == "Down":
            self.image = self.tank_D
            self.image_rect = self.tank_D_rect
        elif self.direction == "Left":
            self.image = self.tank_L
            self.image_rect = self.tank_L_rect
        elif self.direction == "Right":
            self.image = self.tank_R
            self.image_rect = self.tank_R_rect

    def Check_Boundary(self):
        long,wide = 40,40
        if self.x <= 0:
            self.x = 0
        if self.x >= self.boundary[0]-long:
            self.x = self.boundary[0]-long
        if self.y <= 0:
            self.y = 0
        if self.y >= self.boundary[1]-wide:
            self.y = self.boundary[1]-wide

    def Move(self):
        if self.direction == "Up":
            self.y -= self.speed
            self.image = self.tank_U
            self.image_rect = self.tank_U_rect
        elif self.direction == "Down":
            self.y += self.speed
            self.image = self.tank_D
            self.image_rect = self.tank_D_rect
        elif self.direction == "Left":
            self.x -= self.speed
            self.image = self.tank_L
            self.image_rect = self.tank_L_rect
        elif self.direction == "Right":
            self.x += self.speed
            self.image = self.tank_R
            self.image_rect = self.tank_R_rect
        self.Check_Boundary()

        # Update tank coordinate to new image.
        self.image_rect.x = self.x
        self.image_rect.y = self.y

    def Fire_Bullet(self, direction):
        if direction == "Up":
            self.bullet_rect.y -= self.bullet_speed

        elif direction == "Down":
            self.bullet_rect.y += self.bullet_speed

        elif direction == "Left":
            self.bullet_rect.x -= self.bullet_speed

        elif direction == "Right":
            self.bullet_rect.x += self.bullet_speed

        if (self.bullet_rect.x >= self.boundary[0]-10)|(self.bullet_rect.y >= self.boundary[1]-10):
            self.fire_status = False

        elif (self.bullet_rect.x <= 1)|(self.bullet_rect.y <= 1):
            self.fire_status = False

    def Hit_Enemy(self, enemy_list):
        for a in range(len(enemy_list)):
            e = enemy_list[a]

            if e.destory == False:
                if self.Bullet_Hit(e) == True:
                    self.fire_status = False
                    e.HP = e.HP*(1+e.defense/100) - self.Attack
                    if e.HP<=0:
                        e.destory = True
                        Thread(target=Game_System.play_destory).start()
                        for boom in self.BOOMS:
                            im = pg.image.load(boom)
                            im_rec = im.get_rect()
                            im_rec.x = e.x
                            im_rec.y = e.y
                            self.screen.blit(im, im_rec)
                            #time.sleep(0.01)
                            
                            if self.destory == False:
                                self.screen.blit(self.bullet, self.bullet_rect)
                                self.screen.blit(self.image, self.image_rect)

                            for each in enemy_list:
                                if each.destory == False:
                                    self.screen.blit(each.bullet, each.bullet_rect)
                                    self.screen.blit(each.image, each.image_rect)
                                    each.Move()
                            
                            pg.display.flip()
                        enemy_list[a] = 0
                        self.Buff(e.type)

                    elif e.HP > 0:
                        Thread(target=Game_System.play_defense).start()
        return [i for i in enemy_list if i != 0]
    
    def Hit_Wall(self, wall_list):
        gamerun = True
        for a in range(len(wall_list)):
            e = wall_list[a]

            if self.bullet_rect.colliderect(e[1]) == True:

                if e[2] == 1:
                    wall_list[a] = 0
                    self.fire_status = False
                elif e[2] == 2:
                    if self.Attack > 50:
                        wall_list[a] = 0
                    self.fire_status = False
                elif e[2] == 3:
                    pass
                elif e[2] == 4:
                    pass
                elif e[2] == 5:
                    # Boom home.
                    self.fire_status = False
                    Thread(target=Game_System.play_destory).start()

                    for boom in self.BOOMS:
                        im = pg.image.load(boom)
                        im_rec = im.get_rect()
                        im_rec.x = e[1].x
                        im_rec.y = e[1].y
                        self.screen.blit(im, im_rec)

                        if self.destory == False:
                            self.screen.blit(self.bullet, self.bullet_rect)
                            self.screen.blit(self.image, self.image_rect)
                        
                        pg.display.flip()
                    wall_list[a] = 0
                    gamerun = False
        return [i for i in wall_list if i != 0], gamerun

    def Reload_Bullet(self):


        self.bullet_rect.x = self.x+self.image_rect.size[0]//2
        self.bullet_rect.y = self.y+self.image_rect.size[1]//2
        self.image_rect.x = self.x
        self.image_rect.y = self.y

    def Check_Obj(self, enemy):
        if self.image_rect.colliderect(enemy.image_rect):
            if self.direction == "Up":
                self.y = self.y + 2
            elif self.direction == "Down":
                self.y = self.y - 2
            elif self.direction == "Left":
                self.x = self.x + 2
            elif self.direction == "Right":
                self.x = self.x - 2
            self.Reload_Bullet()

    def Check_Walls(self, wall):
        wall_rect = wall[1]
        wall_choice = wall[2]
        if wall_choice != 3:
            if self.image_rect.colliderect(wall_rect):
                if self.direction == "Up":
                    self.y = self.y + (self.speed+2)
                elif self.direction == "Down":
                    self.y = self.y - (self.speed+2)
                elif self.direction == "Left":
                    self.x = self.x + (self.speed+2)
                elif self.direction == "Right":
                    self.x = self.x - (self.speed+2)

                if self.fire_status == False:   
                    self.Reload_Bullet()

    def Bullet_Hit(self, enemy):
        if self.bullet_rect.colliderect(enemy.image_rect):
            return True
        else:
            return False