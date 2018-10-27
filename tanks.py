#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:18:02 2018

@author: David Sung

TA: Mondal
"""
import numpy as np
import matplotlib.pyplot as plt

tank1Color = 'b'
tank2Color = 'r'
obstacleColor = 'k'

##### functions provided to you #####
def getNumberInput (prompt, validRange = [-np.Inf, np.Inf]):
    """displays prompt and converts user input to a number
    
       in case of non-numeric input, re-prompts user for numeric input
       
       Parameters
       ----------
           prompt : str
               prompt displayed to user
           validRange : list, optional
               two element list of form [min, max]
               value entered must be in range [min, max] inclusive
        Returns
        -------
            float
                number entered by user
    """
    while True:
        try:
            num = float(input(prompt))
        except Exception:
            print ("Please enter a number")
        else:
            if (num >= validRange[0] and num <= validRange[1]):
                return num
            else:
                print ("Please enter a value in the range [", validRange[0], ",", validRange[1], ")") #Python 3 sytanx
            
    return num  



##### functions you need to implement #####
def trajectory (x0,y0,v,theta,g = 9.8, npts = 10000):
    """
    finds the x-y trajectory of a projectile
    
    parameters
    ----------
    x0 : float 
        initial x - position
    y0 : float
        initial y - position, must be >0
        initial velocity
    theta : float
        initial angle (in degrees)
    g : float (default 9.8)
        acceleration due to gravity
    npts : int
        number of points in the sample
    
    returns
    -------
    (x,y) : tuple of np.array of floats
        trajectory of the projectile vs time
    
    notes
    -----
    trajectory is sampled with npts time points between 0 and 
    the time when the y = 0 (regardless of y0)
    y(t) = y0 + vsin(theta) t - 0.5 g t^2
    0.5g t^2 - vsin(theta) t - y0 = 0
    t_final = v/g sin(theta) + sqrt((v/g)^2 sin^2(theta) + 2 y0/g)
    """
    
    #convert degrees to radians
    theta = np.deg2rad(theta)
    #equation for x and y component velocity
    velocity_x = v*np.cos(theta)
    velocity_y = v*np.sin(theta)
    
    #equation for finding the time it takes for projectile to hit ground (y=0)
    t_final = (velocity_y/g)+np.sqrt((velocity_y/g)**2+(2*y0/g))
    #make a time array from 0 to the time the projectile hits ground
    t = np.linspace(0,t_final,npts)
    
    #empty x and y position array
    position_x = []
    position_y = []
    
    #for each time interval, calculate the x and y position of the projectile and append to position array
    for time in t: 
        position_x.append(x0+velocity_x*time)
        position_y.append(y0+velocity_y*time-0.5*g*time**2)
        
    #return the x and y position array
    return position_x, position_y


def firstInBox (x,y,box):
    """
    finds first index of x,y inside box
    
    paramaters
    ----------
    x,y : np array type
        positions to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    -------
    int
        the lowest j such that
        x[j] is in [left,right] and 
        y[j] is in [bottom,top]
        -1 if the line x,y does not go through the box
    """

    #check all the data points in the x and y position array to see if any points are within the box area
    for j in range(0,len(x)):
        #if any points in the x and y array are within the box, return the index 
        if x[j] >= box[0] and x[j] <= box[1] and y[j] >= box[2] and y[j] <= box[3]:
            return j
    #if the projectile does not hit the box, return the value -1
    return -1
    
###function already given to us
def endTrajectoryAtIntersection (x,y,box):
    """
    portion of trajectory prior to first intersection with box
    
    paramaters
    ----------
    x,y : np array type
        position to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    ----------
    (x,y) : tuple of np.array of floats
        equal to inputs if (x,y) does not intersect box
        otherwise returns the initial portion of the trajectory
        up until the point of intersection with the box
    """
    
    i = firstInBox(x,y,box)
    
    #if the value of i is less than 0, it means that the projectile did not hit the box
    #returns just the original x and y position array
    if (i < 0):
        return (x,y)
    
    #if the projectile hits the box, then return the new x, y position array
    return (x[0:i],y[0:i])




def tankShot (targetBox, obstacleBox, x0, y0, v, theta, g = 9.8):
    """
    executes one tank shot
    
    parameters
    ----------
    targetBox : tuple
        (left,right,bottom,top) location of the target
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    x0,y0 :floats
        origin of the shot
    v : float
        velocity of the shot
    theta : float
        angle of the shot
    g : float 
        accel due to gravity (default 9.8)
    returns
    --------
    int
        code: 0 = miss, 1 = hit
        
    hit if trajectory intersects target box before intersecting
    obstacle box
    draws the truncated trajectory in current plot window
    """
    
    #get the x,y position of the shot given the initial position, velocity, and angle
    position_x_shot, position_y_shot = trajectory(x0,y0,v,theta,g=9.8,npts=10000)
    
    #check if the trajectory hits the obstalce ebox
    hit_obstacle = firstInBox(position_x_shot, position_y_shot, obstacleBox)
    
    #if the trajectory hits the obstacle box
    if hit_obstacle != -1:
        #find the new trajectory (stop trajectory where it hits obstacle box) and plot
        shot_trajectory_x, shot_trajectory_y = endTrajectoryAtIntersection (position_x_shot, position_y_shot, obstacleBox)
        plt.plot(shot_trajectory_x, shot_trajectory_y)
        showWindow()
        #returns a miss
        return 0
    #if the trajectory misses the obstacle
    elif hit_obstacle == -1:
        #check if the trajectory hits the target box
        hit_target = firstInBox(position_x_shot, position_y_shot, targetBox)
        #if the trajectory misses the target box, plot the projectory
        if hit_target == -1:
            shot_trajectory_x, shot_trajectory_y = endTrajectoryAtIntersection(position_x_shot, position_y_shot, targetBox)
            plt.plot(shot_trajectory_x, shot_trajectory_y)
            showWindow()
            #return a miss 
            return 0
        #if the trajectory hits the target box 
        elif hit_target != -1:
            #find the new trajectory (stop trajectory where it hits the target box) and plot
            shot_trajectory_x, shot_trajectory_y = endTrajectoryAtIntersection (position_x_shot, position_y_shot, targetBox)
            plt.plot(shot_trajectory_x, shot_trajectory_y)
            showWindow()
            #return a hit value
            return 1
    
def oneTurn (tank1box, tank2box, obstacleBox, playerNum, g = 9.8):   
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    returns
    -------
    int
        code 0 = miss, 1 or 2 -- that player won
    
    clears figure
    draws tanks and obstacles as boxes
    prompts player for velocity and angle
    displays trajectory (shot originates from center of tank)
    returns 0 for miss, 1 or 2 for victory
    """        
    #draw a new board for each new turn
    drawBoard(tank1box,tank2box,obstacleBox,playerNum)
   
    if playerNum == 1:
        print()
        print("**********Player 1 Turn**********")
        velocity = getNumberInput("Velocity of shot: ", validRange = [0,np.Inf])
        #angle should be from 0 to 90 for player 1
        theta = getNumberInput("Angle: ", validRange = [0,90])

    elif playerNum == 2:
        print()
        print("**********Player 2 Turn**********")
        velocity = getNumberInput("Velocity of shot: ", validRange = [0,np.Inf])
        #angle should be from 90 to 180 for player 2
        theta = getNumberInput("Angle: ", validRange = [90,180])
    
    if playerNum == 1:
        #for player 1, the initial position is the center of tank 1
        x0 = (tank1box[0]+tank1box[1])/2
        y0 = (tank1box[2]+tank1box[3])/2
        #determine if player 1 hit tank 2 (target box)
        result = tankShot(tank2box, obstacleBox, x0, y0, velocity, theta, g = 9.8 )
    elif playerNum == 2:
        #for player 2, the initial positon is the center of tank 2
        x0 = (tank2box[0]+tank2box[1])/2
        y0 = (tank2box[2]+tank2box[3])/2
        #determine if player 2 hit tank 1 (target box)
        result = tankShot(tank1box, obstacleBox, x0, y0, velocity, theta, g = 9.8 )
       
    #if the player miss, return 0
    if result == 0:
        return 0
    #if the player hit the target, return the player's number
    elif result == 1:
        return playerNum


#function given to us
def showWindow():
    """
    shows the window -- call at end of drawBoard and tankShot
    """
    plt.draw()
    plt.pause(0.001)
    plt.show()


def drawBoard (tank1box, tank2box, obstacleBox, playerNum):
    """
    draws the game board, pre-shot
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
 
    """    
    #draw the tanks and obstacle box
    drawBox(tank1box,tank1Color)
    drawBox(tank2box,tank2Color)
    drawBox(obstacleBox,obstacleColor)
    plt.xlim(0,100)
    plt.ylim(0,100)
    

    showWindow() #this makes the figure window show up

#function was given to us
def drawBox(box, color):
    """
    draws a filled box in the current axis
    parameters
    ----------
    box : tuple
        (left,right,bottom,top) - extents of the box
    color : str
        color to fill the box with, e.g. 'b'
    """    
    x = (box[0], box[0], box[1], box[1])
    y = (box[2], box[3], box[3], box[2])
    ax = plt.gca()
    ax.fill(x,y, c = color)


def playGame(tank1box, tank2box, obstacleBox, g = 9.8):
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    """
    #start with player 1
    playerNum = 1
    
    #start with player 1 turn
    victory = oneTurn(tank1box,tank2box, obstacleBox, playerNum, g=9.8)
    
    #if player 1 misses, continue playing until someone wins (when victory != 0)
    while victory == 0:
        #clear the board every time a new turn begins
        Refresh = input("Press Enter to Continue ")
        while Refresh != "":
            Refresh = input("Press Enter to Continue ")
        if Refresh == "":
            plt.clf()
        #if the player misses, change player
        playerNum = 3-playerNum
        #new player gets to shoot tank
        victory = oneTurn(tank1box,tank2box, obstacleBox, playerNum, g=9.8)
        
    #when a player hits a target, victory = 1 if player 1 won and victory = 2 if palyer 2 won
    if victory == 1 or victory == 2:
        print()
        #print who won
        print ("**********PLAYER", playerNum, "WINS!**********")




##### fmain -- edit box locations for new games #####
def main():
    tank1box = [10,15,0,5]
    tank2box = [90,95,0,5]
    obstacleBox = [40,60,0,50]
    playGame(tank1box, tank2box, obstacleBox)
    

#don't edit the lines below;
if __name__== "__main__":
    main()  
        
    