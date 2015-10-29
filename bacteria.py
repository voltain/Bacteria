#!/usr/bin/env python
from random import randint
import math
import copy
from Tkinter import *
root = Tk()

class Space(object):    
    #Space is the area where the bacteria lives
        
    def __init__(self,size):
        self.size=size
        self.structure = [[0 for x in xrange(size)] for x in xrange(size)] #space is define as two dimensional matrix, currently empty. It will be filled with food.
        self.amountOfFood=0
            
    def generateFood(self,amountOfFood):
        #inital generation of food. This happends only oce, because the environment must be for all bacterias same.
        for i in range(amountOfFood):
            x= randint(0,self.size-1)
            y= randint(0,self.size-1)
            self.structure[x][y]=1

class Bacteria(object):
    def __init__(self,spacex):
        self.direction="U" #initial direction, U means UP. So the bacteria looks "up".
        self.dna=[]
        self.fitness=0
        self.space=spacex #passing information of the space to Bacteria
        self.x=int(math.ceil(self.space.size/2)) #initial centred position in matrix
        self.y=int(math.ceil(self.space.size/2)) #initial centred position in matrix

    def moveMe(self,how):
        #initialise moving the Bactria
        
        if how==1:
            self.moveForward()
            
        if how==2:
            self.turnLeft()
            
        if how==3:
            self.turnRight()
        
        self.eatFood()
        
    def moveMeRandomly(self):
        #moves Bacteria randomnly for initial Generation
        
        rand=randint(1,3)
        
        if rand==1:
            self.moveForward()
            
        if rand==2:
            self.turnLeft()
            
        if rand==3:
            self.turnRight()
        
        self.eatFood() #check if on there is food on the spot
        self.recordToDNA(rand) #records the movement to DNA
    
    #definition of MOVEMENTS - move forward, turn left, turn right    
    def moveForward(self):
        #moving the Bacteria forward according to the direction the Bacteria is facing, stopping in case Bacteria would hit the wall of the Space
        
        c=0
        r=0
        
        if self.direction=="U":
            r=-1
            
        if self.direction=="D":
            r=1
            
        if self.direction=="L":
            c=-1  
            
        if self.direction=="R":
            c=1
        
        #Stopping Bacteria in case of hitting the wall, if not ... moves the bacteria to new location        
        if (self.x+r>=1) and (self.x+r<=self.space.size) and (self.y+c>=1) and (self.y+c<=self.space.size):
            self.x=self.x+r
            self.y=self.y+c
        
    
    def turnRight(self):
        if self.direction=="U":
            self.direction="R"
            return
            
            
        if self.direction=="D":
            self.direction="L"
            return
        
        if self.direction=="L":
            self.direction="U"
            return
        
        if self.direction=="R":
            self.direction="D"
            return
        
    def turnLeft(self):
        if self.direction=="U":
            self.direction="L"
            return
            
            
        if self.direction=="D":
            self.direction="R"
            return
        
        if self.direction=="L":
            self.direction="D"
            return
        
        if self.direction=="R":
            self.direction="U"
            return
    
    def recordToDNA(self,rand):
        self.dna.append(rand)
        
    def eatFood(self):
        if self.space.structure[self.x-1][self.y-1]==1:
            self.fitness=self.fitness+1
            self.space.structure[self.x-1][self.y-1]=0
           
            
class Scientist(object):
    #Scientist is person who observes all bacterias and picks the best one based on their fitness. Scientist also stimulates reproduction of the bacterias.
    #Scientist also draws the Fittest one's movement
    
    def __init__(self,bacterias,space):
        self.bacterias=bacterias #list of all bacterias from current Generation
        self.theFittest=0
        self.bacteriaList=[]
        self.equalSpace=space
        
    def pickTheFittest(self):
        bacteriaIDMaximum=0 
        maxfitness=0
        
        #finds the best Bacteria by the best fitness by going through all bacterias in this Generation
        for i in range(1,len(self.bacterias)-1):
            if self.bacterias[i].fitness>maxfitness:
                bacteriaIDMaximum=i
                maxfitness=self.bacterias[i].fitness
        
        self.theFittest= self.bacterias[bacteriaIDMaximum]
        
    def printTheFittest(self):               
        print "The fittest is the Bactery with fitness ", self.theFittest.fitness," and with DNA = ",self.theFittest.dna
        
    def reproduceTheFittest(self,amountOfBacteries,mutationChance):
    
        self.bacteriaList=[0 for x in range(1,amountOfBacteries+2)] #kills previous Generation
        

        for bacteriaID in range(1,amountOfBacteries):
            
            
            self.bacteriaList[bacteriaID]=copy.deepcopy(self.theFittest) #the first Bacteria of the Generation the exact Fittest one's copy
            
            #initializing position and direction of new Bacteria
            self.bacteriaList[bacteriaID].x=int(math.ceil(self.equalSpace.size/2))
            self.bacteriaList[bacteriaID].y=int(math.ceil(self.equalSpace.size/2))
            self.bacteriaList[bacteriaID].direction="U"
            self.bacteriaList[bacteriaID].space=copy.deepcopy(self.equalSpace) #environment needs to be same as for other Bacterias.
            
            
            
            if bacteriaID>1: #First Bacteria must be identical copy of the Fittest, because mutated successors of the Fittest might be worse. If this happens, Scientist will pick again the current Fittest
                self.bacteriaList[bacteriaID].fitness=0
                
                for i in range(0,len(self.bacteriaList[bacteriaID].dna)):
                    
                    mutationChanceRand=randint(0,100) #chance of mutation depends on initial setting                    
                    
                    if mutationChanceRand>=mutationChance:
                        mutation=randint(1,3)
                        
                        self.bacteriaList[bacteriaID].dna[i]=mutation
                        
                        self.bacteriaList[bacteriaID].moveMe(mutation)
                    else:                        
                        self.bacteriaList[bacteriaID].moveMe(self.bacteriaList[bacteriaID].dna[i])

        self.bacterias=copy.deepcopy(self.bacteriaList) #new generation is loaded

    def playTheFittest(self):
        
        #copies the ultimate Fittest to Winner. Just in case we would like to do something with the Fittest
        #initialisation
        self.theWinner=copy.deepcopy(self.theFittest)        
        self.theWinner.x=int(math.ceil(self.equalSpace.size/2))
        self.theWinner.y=int(math.ceil(self.equalSpace.size/2))
        self.theWinner.direction="U"
        self.theWinner.fitness=0       
        
        
        for step in self.theWinner.dna:
            
            self.drawMoveMe(step,equalSpace)
                     
            canvas.update()
            canvas.after(10) #waits a bit, because it would be too fast if 0
            #canvas.delete(ALL) # This erases everything on the canvas. to speedup
            canvas.update()
            
    def drawMoveMe(self,step,equalSpace):
        #graphical representation of the Winners movement
        
        if step==1:
            c=0
            r=0
        
            if self.theWinner.direction=="U":
                r=-1
            
            if self.theWinner.direction=="D":
                r=1
            
            if self.theWinner.direction=="L":
                c=-1  
            
            if self.theWinner.direction=="R":
                c=1
                
            if (self.theWinner.x+r>=1) and (self.theWinner.x+r<=equalSpace.size) and (self.theWinner.y+c>=1) and (self.theWinner.y+c<=equalSpace.size):
                self.theWinner.x=self.theWinner.x+r
                self.theWinner.y=self.theWinner.y+c
        
        if step==2:
            if self.theWinner.direction=="U":
                self.theWinner.direction="L"
                return
            
            
            if self.theWinner.direction=="D":
                self.theWinner.direction="R"
                return
        
            if self.theWinner.direction=="L":
                self.theWinner.direction="D"
                return
        
            if self.theWinner.direction=="R":
                self.theWinner.direction="U"
                return
        
        if step==3:
            if self.theWinner.direction=="U":
                self.theWinner.direction="R"
                return
            
            
            if self.theWinner.direction=="D":
                self.theWinner.direction="L"
                return
        
            if self.theWinner.direction=="L":
                self.theWinner.direction="U"
                return
        
            if self.theWinner.direction=="R":
                self.theWinner.direction="D"
                return
        
        
        if equalSpace.structure[self.theWinner.x-1][self.theWinner.y-1]==1:
            self.theWinner.fitness=self.theWinner.fitness+1
            equalSpace.structure[self.theWinner.x-1][self.theWinner.y-1]=0
        
        drawSpace(equalSpace)

def drawcircle(canv,x,y,rad,color):
    canv.create_oval(x-rad,y-rad,x+rad,y+rad,width=0,fill=color)

    
def drawSpace(equalSpace):
    
    numberofDots=equalSpace.size 
    sizeOfdot=10
    
    for i in range(0,numberofDots):
        for j in range(0,numberofDots):
            
            if equalSpace.structure[i][j]==1:
                circ1e=drawcircle(canvas,sizeOfdot*4+sizeOfdot*4*i,sizeOfdot*4+sizeOfdot*4*j,sizeOfdot,'gold')
            else:
                circ1e=drawcircle(canvas,sizeOfdot*4+sizeOfdot*4*i,sizeOfdot*4+sizeOfdot*4*j,sizeOfdot,'white')
                
    circ1e=drawcircle(canvas,sizeOfdot*4+sizeOfdot*4*(theObserver.theWinner.x-1),sizeOfdot*4+sizeOfdot*4*(theObserver.theWinner.y-1),sizeOfdot,'blue')
    
    generationText = canvas.create_text(10, 4*numberofDots*(sizeOfdot+0.5), anchor="nw")
    fitnessText = canvas.create_text(10, 4*numberofDots*(sizeOfdot+1), anchor="nw")
    
    
#INITIALISATION   
#===================================================
        
#ini for Space
size=9
amountOfFood=3
amountofGenerations=100

#ini for Bacteria
amountOfBacteries=100
mutationChance=25
bacteriaList=[0 for x in range(1,amountOfBacteries+2)]

#GENERATE THE SPACE
#creates original Space which will be same for all bacterias in order to have same condition
equalSpace=Space(size)
equalSpace.generateFood(amountOfFood)

#ini for graphical output
numberofDots=size  
sizeOfdot=10
canvas = Canvas(width=((numberofDots+1)*4)*sizeOfdot, height=((numberofDots+4)*4)*sizeOfdot, bg='white')
canvas.pack(expand=YES, fill=BOTH)

#PROCESS
#===================================================


#Phase 1: Creation of first Generation
for bacteriaID in range(1,amountOfBacteries):
    
    bacteriaList[bacteriaID]=Bacteria(copy.deepcopy(equalSpace))
    
    for i in range(1,(size*size)+1):
        bacteriaList[bacteriaID].moveMeRandomly()

#Phase 2 & 3: Picking the Fittest and Reproduction with mutation
theObserver=Scientist(bacteriaList,equalSpace) #creation of the Scientist who will handle the picking of the fittest and reproduce new generation


for generation in range(1,amountofGenerations):
    theObserver.pickTheFittest()
    theObserver.reproduceTheFittest(amountOfBacteries,mutationChance)    
    
#Phase 4: Showing the results
theObserver.playTheFittest()
theObserver.printTheFittest()


root.mainloop()
