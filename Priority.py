import tkinter as tk
import random
import math
import numpy as np
import sys
import queue

class Bin:                                      # The class Bin code is written by myself
    def __init__(self,canvas):
        self.canvas = canvas
        self.Upper_left_x = 880
        self.Upper_left_y = 480
        self.Bottom_right_x = 920
        self.Bottom_right_y = 520
        self.centreX = 900
        self.centreY = 500
        self.name = "Bin"
        
    def draw(self,canvas):
        canvas.create_rectangle(self.Upper_left_x,self.Upper_left_y,self.Bottom_right_x,self.Bottom_right_y ,fill = 'Black',tags = self.name)

    def getLocation(self):
        return self.centreX, self.centreY

    
                
class Counter():
    def __init__(self,canvas):
        self.name = 0
        self.x = 50
        self.y = 50
        self.canvas = canvas
        self.garbage_capacity = 0                          # The flowing code is written by myself
        self.dirtCollected = 0
        self.canvas.create_text(self.x+200,self.y,text="Garbage capacity: "+str(self.garbage_capacity),tags ="capacity")             # The flowing code is written by myself
        self.canvas.create_text(self.x,self.y,text="Dirt collected: "+str(self.dirtCollected),tags = "dirtCollected")                
        
        
    def itemCollected(self,canvas):
        self.dirtCollected +=1  
        self.canvas.itemconfigure("dirtCollected",text = "Dirt collected: "+str(self.dirtCollected))
        
    def Garbage_Capacity(self,canvas):                                             # The flowing code is written by myself
        self.garbage_capacity +=1
        self.canvas.itemconfigure("capacity",text ="Garbage capacity: "+str(self.garbage_capacity))

        
        
    
class Bot:
    def __init__(self,namep,canvasp):
        self.x = 500
        self.y = 500
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.name = namep
        self.ll = 60
        self.vl = 0.0
        self.vr = 0.0
        self.battery = 800
        self.turning = 0                                    
        self.moving = random.randrange(50,100)     
        self.currentlyTurning = False
        self.canvas = canvasp
        self.map = np.zeros((10,10))
    
    def collect_dirt(self):  
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
            
    def go_to_charger(self,chargerL,chargerR):                            # The flowing code is written by myself
        if self.battery<400:
            if chargerR>chargerL:
                self.vl = 2.0
                self.vr = -2.0
            elif chargerR<chargerL:
                self.vl = -2.0
                self.vr = 2.0
            if abs(chargerR-chargerL)<chargerL*0.1: 
                self.vl = 5.0
                self.vr = 5.0
        if chargerL+chargerR>200 and self.battery<1000:
            self.vl = 0.0
            self.vr = 0.0
            
    def go_to_bin(self,lightL_to_bin, lightR_to_bin,count):                   # The flowing code is written by myself
        if lightR_to_bin>lightL_to_bin:
            self.vl = 2.0
            self.vr = -2.0
        elif lightR_to_bin<lightL_to_bin:
            self.vl = -2.0
            self.vr = 2.0
        if abs(lightR_to_bin-lightL_to_bin)<lightL_to_bin*0.1:
            self.vl = 5.0
            self.vr = 5.0
        
                
    def brain(self,chargerL,chargerR,lightL_to_bin, lightR_to_bin,count):            # The flowing code is written by myself
        task_queue = queue.PriorityQueue()

        CLEAN_DUST_PRIORITY = 3
        CHARGE_BATTERY_PRIORITY = 2
        EMPTY_TRASH_PRIORITY = 1
        
        if count.garbage_capacity >= 30:
            task_queue.put((EMPTY_TRASH_PRIORITY, "empty_trash"))
        if self.battery < 400:
            task_queue.put((CHARGE_BATTERY_PRIORITY, "charge_battery"))
        task_queue.put((CLEAN_DUST_PRIORITY, "clean_dust"))
                
        task = task_queue.get()[1]
        if task == "clean_dust":
            self.collect_dirt()
            pass
        elif task == "charge_battery":
            self.go_to_charger(chargerL,chargerR)
            pass
        elif task == "empty_trash":
            self.go_to_bin(lightL_to_bin, lightR_to_bin,count)
            pass
 
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
        canvas.create_text(self.x,self.y,text=str(self.battery),tags=self.name)

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
        
    def move(self,canvas,registryPassives,dt,count):
        if self.battery>0:
            self.battery -= 1
        if self.battery==0:
            self.vl = 0
            self.vr = 0
        for rr in registryPassives:                                         # The flowing code is written by myself
            if isinstance(rr,Charger) and self.distanceTo(rr)<80:
                self.battery += 10
        for rr in registryPassives:
            if isinstance(rr,Bin) and self.distanceTo(rr)<80 and count.garbage_capacity>0:
                count.garbage_capacity-=1
                 
                
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
        if self.x<0.0:
            self.x=999.0
        if self.x>1000.0:
            self.x = 0.0
        if self.y<0.0:
            self.y=999.0
        if self.y>1000.0:
            self.y = 0.0
        canvas.delete(self.name)
        self.draw(canvas)
        self.updateMap()
        

    def senseCharger(self, registryPassives):
        lightL = 0.0
        lightR = 0.0
        for pp in registryPassives:
            if isinstance(pp,Charger):
                lx,ly = pp.getLocation()
                distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                                       (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
                distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                                       (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )
                lightL += 200000/(distanceL*distanceL)
                lightR += 200000/(distanceR*distanceR)
        return lightL, lightR
    
    def senseBin(self, registryPassives):                                    # The flowing code is written by myself
        lightL_to_bin = 0.0
        lightR_to_bin = 0.0
        for pp in registryPassives:
            if isinstance(pp,Bin):
                lx,ly = pp.getLocation()
                distanceL = math.sqrt( (lx-self.sensorPositions[0])*(lx-self.sensorPositions[0]) + \
                                       (ly-self.sensorPositions[1])*(ly-self.sensorPositions[1]) )
                distanceR = math.sqrt( (lx-self.sensorPositions[2])*(lx-self.sensorPositions[2]) + \
                                       (ly-self.sensorPositions[3])*(ly-self.sensorPositions[3]) )
                lightL_to_bin += 200000/(distanceL*distanceL)
                lightR_to_bin += 200000/(distanceR*distanceR)
        return lightL_to_bin, lightR_to_bin
    

    def distanceTo(self,obj):
        xx,yy = obj.getLocation()
        return math.sqrt( math.pow(self.x-xx,2) + math.pow(self.y-yy,2) )

    def collectDirt(self, canvas,registryPassives,count):
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr,Dirt):
                if self.distanceTo(rr)<30 and count.garbage_capacity<30:            # The flowing code is written by myself
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected(canvas)
                    count.Garbage_Capacity(canvas)
                    # print (count.dirtCollected)
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives
    
    def updateMap(self):
        xMapPosition = int(math.floor(self.x/100))
        yMapPosition = int(math.floor(self.y/100))
        self.map[xMapPosition,yMapPosition] = 1
        self.drawMap()
        
    def drawMap(self):
        for i in range(0,10):
            for j in range(0,10):
                if self.map[i][j] == 1:
                    self.canvas.create_rectangle(100*i,100*j,100*i+100,100*j+100,fill="pink",width=0,tags="map")
        self.canvas.tag_lower("map")



class Charger:
    def __init__(self,namep):
        self.centreX = 100
        self.centreY = 500
        self.name = namep
        
    def draw(self,canvas):
        body = canvas.create_oval(self.centreX-10,self.centreY-10, \
                                  self.centreX+10,self.centreY+10, \
                                  fill="gold",tags=self.name)

    def getLocation(self):
        return self.centreX, self.centreY


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
    



def buttonClicked(x,y,registryActives):
    for rr in registryActives:
        if isinstance(rr,Bot):
            rr.x = x
            rr.y = y

def initialise(window):
    window.resizable(False,False)
    canvas = tk.Canvas(window,width=1000,height=1000)
    canvas.pack()
    return canvas

def register(canvas,noofbots):
    registryActives = []
    registryPassives = []
    # noOfBots = 1
    bin = Bin(canvas)                                        # The flowing code is written by myself
    registryPassives.append(bin)
    bin.draw(canvas)
    noOfDirt = 300
    for i in range(0,noofbots):
        bot = Bot("Bot"+str(i),canvas)
        registryActives.append(bot)
        bot.draw(canvas)
    charger = Charger("Charger")
    registryPassives.append(charger)
    charger.draw(canvas)
    hub1 = WiFiHub("Hub1",950,50)
    # registryPassives.append(hub1)
    # hub1.draw(canvas)
    hub2 = WiFiHub("Hub1",50,500)
    # registryPassives.append(hub2)
    # hub2.draw(canvas)    
    for i in range(0,noOfDirt):
        dirt = Dirt("Dirt"+str(i))
        registryPassives.append(dirt)
        dirt.draw(canvas)
    canvas.bind( "<Button-1>", lambda event: buttonClicked(event.x,event.y,registryActives) )
    count = Counter(canvas)
    registryPassives.append(count)
    return registryActives, registryPassives,count

def moveIt(canvas,registryActives,registryPassives,count,count_move,window):
    for rr in registryActives:
        chargerIntensityL, chargerIntensityR = rr.senseCharger(registryPassives)
        lightL_to_bin, lightR_to_bin = rr.senseBin(registryPassives)
        rr.brain(chargerIntensityL, chargerIntensityR,lightL_to_bin, lightR_to_bin,count)
        rr.move(canvas,registryPassives,1.0,count)
        registryPassives = rr.collectDirt(canvas,registryPassives,count)
        count_move +=1
        print(count_move)
        if count_move>=2000:
            # print("total moves is: "+str(count_move)+ " total collected dirt is : "+str(count.dirtCollected))
            window.destroy()           
    canvas.after(1,moveIt,canvas,registryActives,registryPassives,count,count_move,window)

def runOneExperiment(noofbots):
    window = tk.Tk()
    canvas = initialise(window)
    registryActives, registryPassives,count = register(canvas,noofbots)
    count_move = 0
    moveIt(canvas,registryActives,registryPassives,count,count_move,window)
    window.mainloop()
    return count.dirtCollected

print("dirtCollected : " +str(runOneExperiment(1)))
