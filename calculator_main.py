from ion import *
from kandinsky import *
from random import *
import math

class Silo:
    def __init__(self,x,y, missiles):
        self.x = x
        self.y = y 
        self.missiles = missiles

    def draw(self):
        fill_rect(self.x,self.y,30,10,(0,254,0))
  
    def delet (self):
        fill_rect(self.x,self.y,30,4,(0,0,0))
        fill_rect(self.x,self.y+4,30,3,(50,50,50))

    def draw_missile_number(self):
        #if self.missiles < 10:
         #   fill_rect(self.x + 10,0,10,10,(50,210,25))
        draw_string((str(self.missiles)),self.x,1,(254,254,254),(0,0,0))


class Anti_missile:
    def __init__(self,x,y,targetx,targety):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.targetx = targetx
        self.targety = targety
        self.explode = False
        self.mouves = 0
        self.explode_frames = 0
        self.explosion_width = 0
        self.explosion_colors = [(254,254,254),(255,0,212)]
        self.explosionc_color_index = 0
        if abs(self.targetx - self.x) > abs(self.targety - self.y):
            if (self.targetx - self.x) < 0:
                self.x_mouvement = -1
            else:
                self.x_mouvement = 1

            self.y_mouvement = (self.targety - self.y) / abs(self.targetx - self.x)
        else:
            self.y_mouvement = -1
            self.x_mouvement = (self.targetx - self.x) / abs(self.targety - self.y)

    def mouve(self):
        for i in range(0,2):
            self.x += self.x_mouvement
            self.y += self.y_mouvement
            set_pixel(round(self.x),round(self.y),(100,0,254))
            self.mouves += 1

    def delet(self):
        xdelet = self.start_x
        ydelet = self.start_y
        for i in range(0,self.mouves):
            xdelet += self.x_mouvement
            ydelet += self.y_mouvement
            set_pixel(round(xdelet),round(ydelet),(0,0,0))
        self.explode = True

    def explosion(self):
        if self.explode_frames % 2 == 0:
            self.explosion_width += 1
            if self.explosion_width > 20:
                self.explosion_width = 20
            fill_rect(round(self.x - (self.explosion_width / 2)), round(self.y - (self.explosion_width / 2)), round(self.explosion_width),round(self.explosion_width),self.explosion_colors[math.floor(self.explosionc_color_index)])
        self.explode_frames += 1
        self.explosionc_color_index += 0.5
        if self.explosionc_color_index == 2:
            self.explosionc_color_index = 0
    
    def delet_explosion(self):

        fill_rect(round(self.x - (self.explosion_width / 2)), round(self.y - (self.explosion_width / 2)), round(self.explosion_width),round(self.explosion_width),(0,0,0))

        
class City:
    def __init__(self,x,y,destroied):
        self.x = x
        self.y = y
        self.destroied = destroied

    def draw(self):
        fill_rect(self.x,self.y,25,7,(0,0,254))

    def delet(self):
        fill_rect(self.x,self.y,25,7,(0,0,0))


class Curser:
    def __init__(self,x,y,side_lenght,colour,colour_main):
        self.x = x
        self.y = y
        self.side_lenght = side_lenght
        self.colour = colour
        self.colour_main = colour_main
        
    def draw(self):
        fill_rect(self.x,self.y - self.side_lenght,1,self.side_lenght,(self.colour))
        fill_rect(self.x,self.y + 1,1,self.side_lenght,(self.colour))
        fill_rect(self.x + 1,self.y,self.side_lenght,1,(self.colour))
        fill_rect(self.x - self.side_lenght,self.y,self.side_lenght,1,(self.colour))

    def mouve(self):
        last_x = self.x
        last_y = self.y
        #set new position
        if keydown(KEY_RIGHT) == True and self.x < 320 - self.side_lenght -1:
            self.x += 1
        if keydown(KEY_LEFT) == True and self.x > 0 + self.side_lenght:
            self.x -= 1
        if keydown(KEY_UP) == True and self.y > 0 + self.side_lenght:
            self.y -= 1
        if keydown(KEY_DOWN) == True and self.y < 222 - 30:
            self.y += 1
        #delet last position
        if last_x != self.x or last_y != self.y:
            fill_rect(last_x,last_y - self.side_lenght,1,self.side_lenght,(self.colour_main))
            fill_rect(last_x,last_y + 1,1,self.side_lenght,(self.colour_main))
            fill_rect(last_x + 1,last_y,self.side_lenght,1,(self.colour_main))
            fill_rect(last_x - self.side_lenght,last_y,self.side_lenght,1,(self.colour_main))
        #draw new position
        fill_rect(self.x,self.y - self.side_lenght,1,self.side_lenght,(self.colour))
        fill_rect(self.x,self.y + 1,1,self.side_lenght,(self.colour))
        fill_rect(self.x + 1,self.y,self.side_lenght,1,(self.colour))
        fill_rect(self.x - self.side_lenght,self.y,self.side_lenght,1,(self.colour))

class Missile:
    def __init__(self,target,speed):
        self.x = randint(10,310)
        self.y = 0
        self.start_x = self.x
        self.start_y = self.y 
        self.target = target[randint(0,len(target)-1)]
        self.speed = speed
        self.x_mouvement = (self.target[0] - self.x)/(self.target[1] - self.y) * self.speed
        self.y_mouvement = 1 * self.speed
        self.summon_frame = randint(1,2500)

    def draw(self):
        set_pixel(round(self.x,1),round(self.y,1),(100,254,0))

    def delet(self):
        xdelet = self.start_x
        ydelet = self.start_y
        for i in range(0, (self.y - self.start_y) / self.speed):
            xdelet += self.x_mouvement
            ydelet += self.y_mouvement
            set_pixel(round(xdelet),round(ydelet),(0,0,0))

    def mouve(self):
        self.x += self.x_mouvement
        self.y += self.y_mouvement
        fill_rect(round(self.x),round(self.y),1,1,(100,254,0))


def draw_background(colour_main,colour_ground):
    fill_rect(0,0,320,218,colour_main)
    fill_rect(0,219,340,5,(colour_ground))

#set up targets, curser and background
draw_background((0,0,0),(254,254,0))

acurser = Curser(100,100,3,(254,254,254),(0,0,0))

#render city and create
acity = City(46,222-7-5,False)
bcity = City(79,222-7-5,False)
ccity = City(112,222-7-5,False)
dcity = City(183,222-7-5,False)
ecity = City(216,222-7-5,False)
fcity = City(249,222-7-5,False)
city_names = [acity,bcity,ccity,dcity,ecity,fcity]
for i in city_names:
    i.draw()

# silo create
asilo = Silo(8,222-9-5,10)
bsilo = Silo(145,222-9-5,10)
gsilo = Silo(282,222-9-5,10)
silo_names = [asilo,bsilo,gsilo]

targets = ((asilo.x+15,asilo.y),(acity.x+12,acity.y),(bcity.x+12,bcity.y),(ccity.x+12,ccity.y),(bsilo.x+15,bsilo.y),(dcity.x+12,dcity.y),(ecity.x+12,ecity.y),(fcity.x+12,fcity.y),(gsilo.x+15,gsilo.y))

while True:
    #silo reset
    for j in silo_names:
        j.draw()
        j.missiles = 10
    a_couldown = 0
    b_couldown = 0
    g_couldown = 0
    list_anti_missile = []

    #acurser.draw()

    #create missiles
    list_missile = []
    name_missile = []
    for j in range(0,randint(15,23)):
        amissile= Missile(targets,0.25)
        name_missile.append(amissile)



    #list_couldown = [a_couldown,b_couldown,g_couldown]
    for e in range(0,3000):
        a_couldown += 1
        b_couldown += 1
        g_couldown += 1

        #sumon missile
        for j in name_missile:
            if j.summon_frame == e:
                list_missile.append(j)
                name_missile.remove(j)
        
        amissile.mouve()
        acurser.mouve()

        #shoot need to compact in class silo.shoot
        if keydown(KEY_ONE) == True and asilo.missiles > 0 and a_couldown >= 10:
            aantimissile = Anti_missile(asilo.x + 15,asilo.y - 1,acurser.x,acurser.y)
            list_anti_missile.append(aantimissile)
            a_couldown = 0
            asilo.missiles += -1
        if keydown(KEY_TWO) == True and bsilo.missiles > 0 and b_couldown >= 10:
            bantimissile = Anti_missile(bsilo.x + 15,bsilo.y - 1,acurser.x,acurser.y)
            list_anti_missile.append(bantimissile)
            b_couldown = 0
            bsilo.missiles += -1
        if keydown(KEY_THREE) == True and gsilo.missiles > 0 and g_couldown >= 10:
            gantimissile = Anti_missile(gsilo.x + 15,gsilo.y - 1,acurser.x,acurser.y)
            list_anti_missile.append(gantimissile)
            g_couldown = 0
            gsilo.missiles += -1
        
        #antimissile loop
        for i in list_anti_missile:
            if i.explode == False:
                i.mouve()
                if i.x < (i.targetx + 1) and  i.x > (i.targetx - 1) and  i.y < (i.targety - 1) or i.y < (i.targety):
                    i.delet()
            else:
                i.explosion()
                if i.explode_frames > 70:
                    i.delet_explosion()
                    list_anti_missile.remove(i)
            #collision
            for j in list_missile:
                if i.x - (i.explosion_width/2) < j.x and i.x + (i.explosion_width/2) > j.x and i.y - (i.explosion_width/2) < j.y and i.y + (i.explosion_width/2) > j.y:
                    j.delet()
                    list_missile.remove(j)
                    del(j)


        #missile loop
        for j in list_missile:
            j.mouve()


        #city loop
        for i in city_names:
            for j in list_missile:
                if j.y >= i.y and j.x >= i.x  and j.x <= (i.x + 25):
                    i.delet()
                    i.destroied = True
                    j.delet()
                    list_missile.remove(j)
                    del(j)

        #silo loop
        for i in silo_names:
            i.draw_missile_number()
            for j in list_missile:
                if j.y >= i.y and j.x >= i.x  and j.x <= (i.x + 30):
                    i.delet()
                    i.missiles = 0
                    j.delet()
                    list_missile.remove(j)
                    del(j)

# keydown(KEY_RIGHT)