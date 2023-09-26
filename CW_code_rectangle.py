import tkinter as tk
import random
import math
import numpy as np
import sys


class Line:                                                        # The class Line code is written by myself
    def __init__(self,x,y): 
        self.x = x
        self.y = y
        
    def get_location(self):
        return self.x,self.y
    
    def Draw_a_line1(self,canvas):
        canvas.create_line(self.x,self.y,1000,250,fill = "black",width = 5)
        
    def Draw_a_line2(self,canvas):
        canvas.create_line(self.x,self.y,1000,500,fill = "black",width = 5)
        
    def Draw_a_line3(self,canvas):
        canvas.create_line(self.x,self.y,1000,750,fill = "black",width = 5)
        

class Counter:
    def __init__(self,canvas):
        self.dirtCollected = 0
        self.canvas = canvas
        self.canvas.create_text(70,50,text="Dirt collected: "+str(self.dirtCollected),tags="counter")
        
    def itemCollected(self, canvas):
        self.dirtCollected += 1
        self.canvas.itemconfigure("counter",text="Dirt collected: "+str(self.dirtCollected))


class Bot:
    def __init__(self,namep,canvasp,x_start,y_start):
        self.x = x_start
        self.y = y_start
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.name = namep
        self.ll = 60 #axle width
        self.vl = 0.0
        self.vr = 0.0
        self.turning = 0
        self.moving = random.randrange(50,100)
        self.currentlyTurning = False
        self.canvas = canvasp

    def brain(self):
        if self.currentlyTurning==True:
            self.vl = -2.0
            self.vr = 2.0
            self.turning -= 1
        else:
            self.vl = 5.0
            self.vr = 5.0
            self.moving -= 1
        if self.moving==0 and not self.currentlyTurning:
            self.turning = random.randrange(20,40)
            self.currentlyTurning = True
        if self.turning==0 and self.currentlyTurning:
            self.moving = random.randrange(50,100)
            self.currentlyTurning = False
             

    def draw(self,canvas):
        points = [ (self.x + 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) - 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) - 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x - 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y + 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                   (self.x + 30*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                   (self.y - 30*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                ]
        canvas.create_polygon(points, fill="blue", tags=self.name)

        self.sensorPositions = [ (self.x + 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y - 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta), \
                                 (self.x - 20*math.sin(self.theta)) + 30*math.sin((math.pi/2.0)-self.theta), \
                                 (self.y + 20*math.cos(self.theta)) + 30*math.cos((math.pi/2.0)-self.theta)  \
                            ]
    
        centre1PosX = self.x 
        centre1PosY = self.y
        canvas.create_oval(centre1PosX-15,centre1PosY-15,\
                           centre1PosX+15,centre1PosY+15,\
                           fill="gold",tags=self.name)

        wheel1PosX = self.x - 30*math.sin(self.theta)
        wheel1PosY = self.y + 30*math.cos(self.theta)
        canvas.create_oval(wheel1PosX-3,wheel1PosY-3,\
                                         wheel1PosX+3,wheel1PosY+3,\
                                         fill="red",tags=self.name)

        wheel2PosX = self.x + 30*math.sin(self.theta)
        wheel2PosY = self.y - 30*math.cos(self.theta)
        canvas.create_oval(wheel2PosX-3,wheel2PosY-3,\
                                         wheel2PosX+3,wheel2PosY+3,\
                                         fill="green",tags=self.name)

        sensor1PosX = self.sensorPositions[0]
        sensor1PosY = self.sensorPositions[1]
        sensor2PosX = self.sensorPositions[2]
        sensor2PosY = self.sensorPositions[3]
        canvas.create_oval(sensor1PosX-3,sensor1PosY-3, \
                           sensor1PosX+3,sensor1PosY+3, \
                           fill="yellow",tags=self.name)
        canvas.create_oval(sensor2PosX-3,sensor2PosY-3, \
                           sensor2PosX+3,sensor2PosY+3, \
                           fill="yellow",tags=self.name)
        
   
    def move(self,canvas,registryPassives,dt,x_min,x_max,y_min,y_max):        #I changed the code of the move function to make the robot move in the specified area
        
        if self.x < x_min:                         
            self.x = x_min
        elif self.x >x_max:
            self.x =x_max
        if self.y < y_min:
            self.y =y_min
        elif self.y >y_max:
            self.y =y_max
        
                
        if self.vl==self.vr:
            R = 0
        else:
            R = (self.ll/2.0)*((self.vr+self.vl)/(self.vl-self.vr))
        omega = (self.vl-self.vr)/self.ll
        ICCx = self.x-R*math.sin(self.theta) 
        ICCy = self.y+R*math.cos(self.theta)
        m = np.matrix( [ [math.cos(omega*dt), -math.sin(omega*dt), 0], \
                        [math.sin(omega*dt), math.cos(omega*dt), 0],  \
                        [0,0,1] ] )
        v1 = np.matrix([[self.x-ICCx],[self.y-ICCy],[self.theta]])
        v2 = np.matrix([[ICCx],[ICCy],[omega*dt]])
        newv = np.add(np.dot(m,v1),v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta%(2.0*math.pi) 
        self.x = newX
        self.y = newY
        self.theta = newTheta        
        if self.vl==self.vr: 
            self.x += self.vr*math.cos(self.theta) 
            self.y += self.vr*math.sin(self.theta)
        canvas.delete(self.name)
        self.draw(canvas)

    
    def distanceTo(self,obj):
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )

    def collectDirt(self, canvas, registryPassives, count):
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr,Dirt):
                if self.distanceTo(rr)<30:
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected(canvas)
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives


class WiFiHub:
    def __init__(self,namep,xp,yp):
        self.centreX = xp
        self.centreY = yp
        self.name = namep
        
    def draw(self,canvas):
        body = canvas.create_oval(self.centreX-10,self.centreY-10, \
                                  self.centreX+10,self.centreY+10, \
                                  fill="purple",tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY


class Dirt:
    def __init__(self,namep):
        self.centreX = random.randint(100,900)
        self.centreY = random.randint(100,900)
        self.name = namep

    def draw(self,canvas):
        body = canvas.create_oval(self.centreX-1,self.centreY-1, \
                                  self.centreX+1,self.centreY+1, \
                                  fill="grey",tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY


def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def register(canvas):
    bot_list = []
    #lower_left_bot = []
    registryPassives = []
    noOfBots = 4
    noOfDirt = 500
    line1 = Line(0,250)                                  #The following code is written by myself
    registryPassives.append(line1)
    line1.Draw_a_line1(canvas)
    line2 = Line(0,500)
    registryPassives.append(line2)
    line2.Draw_a_line2(canvas)
    line3 = Line(0,750)
    registryPassives.append(line3)
    line3.Draw_a_line3(canvas)
    for i in range(0,noOfBots):
        if i ==0:
            bot = Bot("Bot"+str(i),canvas,500,125)
            bot_list.append(bot)
            bot.draw(canvas)
        elif i==1:
            bot = Bot("Bot"+str(i),canvas,500,375)
            bot_list.append(bot)
            bot.draw(canvas)
        elif i==2:
            bot = Bot("Bot"+str(i),canvas,500,625)
            bot_list.append(bot)
            bot.draw(canvas)
        elif i==3:
            bot = Bot("Bot"+str(i),canvas,500,875)
            bot_list.append(bot)
            bot.draw(canvas)
            
 
    hub1 = WiFiHub("Hub1",950,50)
    registryPassives.append(hub1)
    hub1.draw(canvas)
    hub2 = WiFiHub("Hub1",50,500)
    registryPassives.append(hub2)
    hub2.draw(canvas)
    for i in range(0,noOfDirt):
        dirt = Dirt("Dirt"+str(i))
        registryPassives.append(dirt)
        dirt.draw(canvas)
    count = Counter(canvas)
    return bot_list ,registryPassives, count

def moveIt(canvas,bot_list,registryPassives,count,moves,window):
    moves += 1
    for rr in bot_list:                                             #The following code is written by myself
        if rr.name == "Bot0":
            rr.brain()
            rr.move(canvas,registryPassives,1.0,0,1000,0,250)
            registryPassives = rr.collectDirt(canvas,registryPassives, count)
        elif rr.name == "Bot1":
            rr.brain()
            rr.move(canvas,registryPassives,1.0,0,1000,250,500)
            registryPassives = rr.collectDirt(canvas,registryPassives, count)
        elif rr.name == "Bot2":
            rr.brain()
            rr.move(canvas,registryPassives,1.0,0,1000,500,750)
            registryPassives = rr.collectDirt(canvas,registryPassives, count)
        elif rr.name == "Bot3":
            rr.brain()
            rr.move(canvas,registryPassives,1.0,0,1000,750,1000)
            registryPassives = rr.collectDirt(canvas,registryPassives, count)
        print(moves)
        numberOfMoves = 1000
        if moves>numberOfMoves:
            window.destroy()
    canvas.after(1,moveIt,canvas,bot_list,registryPassives,count,moves,window)


def runOneExperiment():
    window = tk.Tk()
    canvas = initialise(window)
    bot_list,registryPassives, count = register(canvas)
    moves = 0
    moveIt(canvas,bot_list,registryPassives, count, moves,window)
    window.mainloop()
    return str(count.dirtCollected)


runOneExperiment()