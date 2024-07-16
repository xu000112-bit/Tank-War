import pygame as pg
import sys
import time
import numpy as np
from threading import Thread
import Game_Class

def play_manue():
    if pg.mixer.music.get_busy() == True:
        pg.mixer.music.stop()
    pg.mixer.music.load("./musics/MainMenu.mp3")
    pg.mixer.music.play()
    time.sleep(74)
    pg.mixer.music.stop()

def play_attack():
    if pg.mixer.music.get_busy() == True:
        pg.mixer.music.stop()
    pg.mixer.music.load("./musics/tank-attack.wav")
    pg.mixer.music.play()
    time.sleep(0.035)
    pg.mixer.music.stop()

def play_destory():
    if pg.mixer.music.get_busy() == True:
        pg.mixer.music.stop()
    pg.mixer.music.load("./musics/boom.wav")
    pg.mixer.music.play()
    time.sleep(0.25)
    pg.mixer.music.stop()

def play_defense():
    if pg.mixer.music.get_busy() == True:
        pg.mixer.music.stop()
    pg.mixer.music.load("./musics/defense.mp3")
    pg.mixer.music.play()
    time.sleep(0.1)
    pg.mixer.music.stop()

def play_start():
    if pg.mixer.music.get_busy() == True:
        pg.mixer.music.stop()
    pg.mixer.music.load("./musics/start.wav")
    pg.mixer.music.play()
    time.sleep(74)
    pg.mixer.music.stop()

def play_add():
    if pg.mixer.music.get_busy() == True:
        pg.mixer.music.stop()
    pg.mixer.music.load("./musics/add.wav")
    pg.mixer.music.play()
    time.sleep(1)
    pg.mixer.music.stop()

def load_walls(wall_list, screen):
    for e in wall_list:
        screen.blit(e[0], e[1])

def gen_walls(boundary, screen):

    # Design Map.
    map = np.int64(np.random.uniform(size = (boundary[0]//50, boundary[1]//50))>0.7)
    kernel = np.ones(map.shape)
    kernel[kernel.shape[0]//2, kernel.shape[1]-1] = 0
    kernel[kernel.shape[0]//2, kernel.shape[1]-2] = 0
    kernel[kernel.shape[0]//2+1, kernel.shape[1]-2] = 0
    kernel[kernel.shape[0]//2-1, kernel.shape[1]-2] = 0
    kernel[kernel.shape[0]//2-1, kernel.shape[1]-1] = 0
    kernel[kernel.shape[0]//2+1, kernel.shape[1]-1] = 0
    kernel[:, kernel.shape[1]-1] = 0
    map = map*kernel

    # Pick Random Generated Wall Position.
    paint = []
    for pixel_x in range(map.shape[0]):
        for pixel_y in range(map.shape[1]):
            if map[pixel_x, pixel_y] == 1:
                paint.append((pixel_x, pixel_y))

    # Generate Random Walls.
    wall_list = []
    for e in paint:
        choice = np.random.random_integers(1,4)
        wall = pg.image.load("./walls/"+str(choice)+".png")
        wall_rect = wall.get_rect()
        wall_rect.x = e[0]*50
        wall_rect.y = e[1]*50
        screen.blit(wall, wall_rect)
        wall_list.append((wall, wall_rect, choice))

    # Generate Home.    
    home = pg.image.load("./walls/5.png")
    home_rect = home.get_rect()
    home_rect.x = map.shape[0]//2*50
    home_rect.y = (map.shape[1]-1)*50
    screen.blit(home, home_rect)
    wall_list.append((home, home_rect, 5))

    # Brick Sround it.
    wall = pg.image.load("./walls/1.png")
    wall_rect = wall.get_rect()
    wall_rect.x =  map.shape[0]//2*50
    wall_rect.y = (map.shape[1]-2)*50
    screen.blit(wall, wall_rect)
    wall_list.append((wall, wall_rect, 1))
    
    wall = pg.image.load("./walls/1.png")
    wall_rect = wall.get_rect()
    wall_rect.x = (map.shape[0]+2)//2*50
    wall_rect.y = (map.shape[1]-2)*50
    screen.blit(wall, wall_rect)
    wall_list.append((wall, wall_rect, 1))

    wall = pg.image.load("./walls/1.png")
    wall_rect = wall.get_rect()
    wall_rect.x = (map.shape[0]-2)//2*50
    wall_rect.y = (map.shape[1]-2)*50
    screen.blit(wall, wall_rect)
    wall_list.append((wall, wall_rect, 1))

    wall = pg.image.load("./walls/1.png")
    wall_rect = wall.get_rect()
    wall_rect.x = (map.shape[0]-2)//2*50
    wall_rect.y = (map.shape[1]-1)*50
    screen.blit(wall, wall_rect)
    wall_list.append((wall, wall_rect, 1))

    wall = pg.image.load("./walls/1.png")
    wall_rect = wall.get_rect()
    wall_rect.x = (map.shape[0]+2)//2*50
    wall_rect.y = (map.shape[1]-1)*50
    screen.blit(wall, wall_rect)
    wall_list.append((wall, wall_rect, 1))

    return wall_list

def Generate_NPC(enemy_list, screen, setting, num):

    for each in range(num):
        p_x = np.random.random_integers(setting.boundary[0])
        p_y = 0
        tank_type = np.random.randint(low=0, high=4)

        # Qucik Tank
        if tank_type == 3:
            ta = Game_Class.Tank(x = p_x, 
                    y = p_y,
                    HP = 5,
                    Attack = 3,
                    defense = 0,
                    speed = 2,
                    bullet_speed = 7.5,
                    boundary = setting.gameboundary,
                    random = True, 
                    screen = screen,
                    type=tank_type)

        # Heavy Tank
        elif tank_type == 1:
            ta = Game_Class.Tank(x = p_x, 
                    y = p_y,
                    HP = 40,
                    Attack = 30,
                    defense = 0,
                    speed = 0.5,
                    bullet_speed = 2.5,
                    boundary = setting.gameboundary,
                    random = True,
                    screen = screen,
                    type=tank_type)
        
        # Speedy Tank
        elif tank_type == 2:
            ta = Game_Class.Tank(x = p_x, 
                    y = p_y,
                    HP = 5,
                    Attack = 15,
                    defense = 0,
                    speed = 1,
                    bullet_speed = 7.5,
                    boundary = setting.gameboundary,
                    random = True,
                    screen = screen,
                    type=tank_type)
        
        # Normal Tank
        elif tank_type == 0:
            ta = Game_Class.Tank(x = p_x, 
                    y = p_y,
                    HP = 10,
                    Attack = 10,
                    defense = 0,
                    speed = 1,
                    bullet_speed = 5,
                    boundary = setting.gameboundary,
                    random = True,
                    screen = screen,
                    type=tank_type)
        ta.Born_NPC()
        enemy_list.append(ta)
    return enemy_list

def Game_End(screen, setting, hero, enemy_list, wall_list):

    # Main Program loop
    while True:

        # Deal with Event.
        for event in pg.event.get():
            if event.type == pg.QUIT:
                print("Quit")
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                # Check if the key is 'S'
                if event.key == pg.K_ESCAPE:
                    Game_Menue(screen, setting)

                if event.key == pg.K_SPACE:
                    Game_Start(screen, setting, hero, enemy_list, wall_list)

        # Background.
        screen.fill(setting.Black)

        # Refresh Hero.
        hero.move = 0
        if hero.destory == False:
            screen.blit(hero.bullet, hero.bullet_rect)
            screen.blit(hero.image, hero.image_rect)            
        
        # Refresh Enemy.
        for a in range(len(enemy_list)):

            e = enemy_list[a]
            # Random Walk.
            if e.destory == False:
                screen.blit(e.bullet, e.bullet_rect)
                screen.blit(e.image, e.image_rect)


        # Refresh Screen.
        load_walls(wall_list, screen)
        text=setting.smallfont.render("🏠 Esc ▶️ Whitespace", True, setting.color)
        screen.blit(text, ((10, setting.boundary[1]-30)))
        pg.display.flip()
        pg.time.Clock().tick(100)

def Game_Menue(screen, setting):

    Thread(target=play_manue, daemon=True).start()

    width = screen.get_width()  
    height = screen.get_height()  
    
    Quit_text = setting.smallfont.render('EXIT' , True , setting.color)
    Start_text = setting.smallfont.render('NEW GAME' , True , setting.color)
    title_text = setting.Bigfont.render('💥STEEL TITAN CONCLICT💥' , True , setting.color)

    rec_size = (180, 60)

    Start_rec = Start_text.get_rect()
    Start_rec.center = (width//2, height//2)

    Quit_rec = Quit_text.get_rect()
    Quit_rec.center = (width//2, height//2+height//8)

    title_rec = title_text.get_rect()
    title_rec.center = (width//2, height//2-height//4)
    
    while True:  
        
        for ev in pg.event.get():  
            
            if ev.type == pg.QUIT:  
                pg.quit()
                sys.exit()
                
            #checks if a mouse is clicked  
            if ev.type == pg.MOUSEBUTTONDOWN:  
                
                if Quit_rec[0] <= mouse[0] <= Quit_rec[0]+rec_size[0] and Quit_rec[1] <= mouse[1] <= Quit_rec[1]+rec_size[1]:  
                    pg.quit()
                    sys.exit()

                if Start_rec[0] <= mouse[0] <= Start_rec[0]+rec_size[0] and Start_rec[1] <= mouse[1] <= Start_rec[1]+rec_size[1]:
                    wall_list = gen_walls(setting.boundary, screen)
                    hero = Game_Class.Tank(x = setting.boundary[0]//2-50*3, 
                                y = setting.boundary[1],
                                HP = 10,
                                Attack = 10,
                                defense = 0,
                                speed = 1,
                                bullet_speed = 5,
                                boundary = setting.gameboundary,
                                random = False,
                                screen = screen, type = 100)
                    hero.Born_Hero()
                    enemy_list = []
                    enemy_list = Generate_NPC(enemy_list, screen, setting, setting.tank_num)

                    # Play Start Music.
                    Thread(target=play_start, daemon=True).start()
                    time.sleep(2)
                    Game_Start(screen, setting, hero, enemy_list, wall_list)

        # fills the screen with a color  
        screen.fill(setting.Black)   
        mouse = pg.mouse.get_pos()  
        
        # Quit.
        if Quit_rec.x <= mouse[0] <= Quit_rec.x+rec_size[0] and Quit_rec.y <= mouse[1] <= Quit_rec.y+rec_size[1]:  
            pg.draw.rect(screen,setting.color_light,[Quit_rec.center[0]-rec_size[0]//2,Quit_rec.center[1]-rec_size[1]//2,rec_size[0],rec_size[1]])
        else:  
            pg.draw.rect(screen,setting.color_dark,[Quit_rec.center[0]-rec_size[0]//2,Quit_rec.center[1]-rec_size[1]//2,rec_size[0],rec_size[1]])

        # Start
        if Start_rec.x <= mouse[0] <= Start_rec.x+rec_size[0] and Start_rec.y <= mouse[1] <= Start_rec.y+rec_size[1]:  
            pg.draw.rect(screen,setting.color_light,[Start_rec.center[0]-rec_size[0]//2,Start_rec.center[1]-rec_size[1]//2,rec_size[0],rec_size[1]])
        else:  
            pg.draw.rect(screen,setting.color_dark,[Start_rec.center[0]-rec_size[0]//2,Start_rec.center[1]-rec_size[1]//2,rec_size[0],rec_size[1]])
        
        # superimposing the text onto our button
        screen.blit(Quit_text, Quit_rec)
        screen.blit(Start_text, Start_rec)
        screen.blit(title_text, title_rec)
        
        # updates the frames of the game  
        pg.display.update()

def Game_Start(screen, setting, hero, enemy_list, wall_list):

    # Game Run.
    gamerun = True

    # Main Program loop
    while True:

        # Deal with Event.
        for event in pg.event.get():
            # Quit event
            if event.type == pg.QUIT:
                print("Quit")
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    Game_End(screen, setting, hero, enemy_list, wall_list)
            
                if event.key == pg.K_SPACE:
                    if hero.destory == False:
                        if hero.fire_status == False:
                            hero.fire_status = True
                            hero.bullet_direction = hero.direction
                            t2 = Thread(target=play_attack, daemon=True)
                            t2.start()

        # Background.
        screen.fill(setting.Black)

        # Event 1: press key to move hero.
        key = pg.key.get_pressed()
        if hero.destory == False:
            if key[pg.K_LEFT] == True:
                hero.direction = "Left"
                hero.move = hero.speed
                hero.Move()

            elif key[pg.K_RIGHT] == True:
                hero.direction = "Right"
                hero.move = hero.speed
                hero.Move()

            elif key[pg.K_UP] == True:
                hero.direction = "Up"
                hero.move = hero.speed
                hero.Move()

            elif key[pg.K_DOWN] == True:
                hero.direction = "Down"
                hero.move = hero.speed
                hero.Move()
            else:
                hero.move = 0

        # Event 2: Hero Fire.
        if hero.fire_status == True:
            hero.Fire_Bullet(hero.bullet_direction)
            enemy_list = hero.Hit_Enemy(enemy_list)
            wall_list, gamerun = hero.Hit_Wall(wall_list)

            if gamerun == False:
                Game_End(screen, setting, hero, enemy_list, wall_list)
                
        # Refresh Hero.
        if hero.fire_status == False:
            hero.Reload_Bullet()

        # Update Hero.
        if hero.destory == False:
            screen.blit(hero.bullet, hero.bullet_rect)
            screen.blit(hero.image, hero.image_rect)            

        for wal in wall_list:
            hero.Check_Walls(wal)
        
        # Refresh Enemy.
        for a in range(len(enemy_list)):

            e = enemy_list[a]
            e.Check_Obj(hero)
            hero.Check_Obj(e)

            # Enemy Cese Fire
            if e.fire_status == False:
                e.Reload_Bullet()

            for other in range(len(enemy_list)):
                if enemy_list[other] != e:
                    e.Check_Obj(enemy_list[other])

            for wal in wall_list:
                e.Check_Walls(wal)
            
            # Random direction.
            if np.random.uniform() > 0.98:
                e.Random_Walk()

            # Random Open Fire.
            if np.random.uniform() > 0.98:
                if e.fire_status == False:
                    e.fire_status = True
                    e.bullet_direction = e.direction

            # Random Walk.
            if e.destory == False:
                e.move = e.speed
                e.Move()
                screen.blit(e.bullet, e.bullet_rect)
                screen.blit(e.image, e.image_rect)

            # Enemy Open Fire
            if e.fire_status == True:
                e.Fire_Bullet(e.bullet_direction)
                wall_list, gamerun = e.Hit_Wall(wall_list)
                if len(e.Hit_Enemy([hero])) == 0:
                    gamerun = False
                if gamerun == False:
                    Game_End(screen, setting, hero, enemy_list, wall_list)

        # Random Adding Tank.
        if np.random.uniform() > 0.9995:
            enemy_list = Generate_NPC(enemy_list, screen, setting, 1)
            Thread(target=play_add, daemon=True).start()

        # Refresh Screen.
        load_walls(wall_list, screen)
        # Show Statistics.
        text=setting.smallfont.render("❤️ "+str(int(hero.HP))+"   " + "⚔️ "+str(int(hero.Attack))+"   "+"🛡️ "+str(int(hero.defense))+"   "+"🏃 "+str(hero.speed)+"   "+"⏸️ Esc",
                                       True, setting.color)
        screen.blit(text, ((10, setting.boundary[1]-30)))
        pg.display.flip()
        pg.time.Clock().tick(100)
