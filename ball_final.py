#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################################
# Copyright © 2021 Tristan Nerson <tristan.nerson.etu@univ-lemans.fr>          #
# Creation Date: Monday, February 22nd 2021, 10:13:03 am                       #
# -----                                                                        #
# 'ball_final.py' is part of the project 'Balle'.                              #
#                                                                              #
# Balle is free software: you can redistribute it and/or modify                #
# it under the terms of the GNU General Public License as published by         #
# the Free Software Foundation, either version 3 of the License, or            #
# (at your option) any later version.                                          #
#                                                                              #
# Balle is distributed in the hope that it will be useful,                     #
# but WITHOUT ANY WARRANTY; without even the implied warranty of               #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                #
# GNU General Public License for more details.                                 #
#                                                                              #
# You should have received a copy of the GNU General Public License            #
# along with Balle.  If not, see <https://www.gnu.org/licenses/>.              #
################################################################################
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl
import numpy as np
import random as rd

"""This project gives "ball" class and "an_animation" class to plot balls trajectories in space"""

# set default parameters of plots in matplotlib
mpl.rcParams['text.usetex'] = True
mpl.rcParams['animation.html'] = 'html5'

# ------------------------------------------------------------------------------------------------ #
#                                            Class ball                                            #
# ------------------------------------------------------------------------------------------------ #

class ball:
    
    def __init__(self,g,n_rebounds,x0,y0,v0,theta,r,t0):
        """Creates an ball object with its parameters, to be animated

        Args:
            g (float): Gravitational acceleration [m/s^2]
            n_rebounds (int): number of rebounds of the balls in the space [-]
            x0 (float): initial position along x of the ball [m]
            y0 (float): initial position along y of the ball [m]
            v0 (float): initial velocity of the ball [m/s]
            theta (float): initial angle of the velocity [rad]
            r (float): restitution coefficient [-]
            t0 (float): time at which the ball is launched [s]
        """
        
        # Parameters
        self.g = g
        self.n_rebounds = n_rebounds
        self.x0 = x0  
        self.v0 = v0  
        self.theta = theta
        self.y0 = y0
        self.r = r
        self.t0 = t0
        
        self.tmax = 2*self.v0*np.sin(self.theta)/g + self.t0  # time at which the ball reaches back the floor [s]
        dt = self.tmax/100
        self.t = np.arange(self.t0, self.tmax, dt)  # time vector [s]

        self.random_generation()
        
# ------------------------------------------------------------------------------------------------ #
        
    def random_generation(self):
        """Calculates the trajectories"""
        
        # model of the ball trajectory --> before first rebound
        # self.x_tot and self.y_tot will be composed of all coordinates
        self.x_tot = self.v0 * np.cos(self.theta) * (self.t-self.t0) + self.x0
        self.y_tot = -self.g/2 * (self.t-self.t0) ** 2 + self.v0 * np.sin(self.theta) * (self.t-self.t0) + self.y0

        self.vr = self.v0 
        
        # model of the ball trajectory --> generalisation        
        for ii in range(1, self.n_rebounds):
            self.x0 = self.vr * np.cos(self.theta) * (self.tmax-self.t0) + self.x0
            self.vr = self.r ** ii * self.v0
            self.t0 = self.tmax

            self.tmax = 2 * self.vr * np.sin(self.theta)/self.g + self.t0

            self.t = np.linspace(self.t0, self.tmax, 100)

            x = self.vr * np.cos(self.theta) * (self.t - self.t0) + self.x0
            y = -self.g/2 * (self.t - self.t0) ** 2 + self.vr * np.sin(self.theta) * (self.t - self.t0) + self.y0

            self.x_tot = np.concatenate((self.x_tot, x))
            self.y_tot = np.concatenate((self.y_tot, y))
            
# ------------------------------------------------------------------------------------------------ #
        
    def the_animation(self,the_interval):
        """Plots the ball's trajectory

        Args:
            the_interval (int): the wanted frames (1 means "many frames/seconds" while 1000 not)
        """
        fig, ax = plt.subplots(1,1,figsize=(9,4))

        plt.plot(self.x_tot, self.y_tot,c="white")
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')

        line, = ax.plot(self.x_tot[0],self.y_tot[0],'o',c="r")

        def animate(tot):
            """Calculates the new data

            Args:
                tot (int): indice of the x_tot and y_tot on which we loop

            Returns:
               [line] (list): a list of axes
            """
            line.set_data(self.x_tot[tot],self.y_tot[tot])
            return [line]

        plt.tight_layout()
        ani = animation.FuncAnimation(fig,animate,np.arange(0,len(self.x_tot)),interval=the_interval,blit=True)
        plt.show()



# ------------------------------------------------------------------------------------------------ #
#                                        Class an_animation                                        #
# ------------------------------------------------------------------------------------------------ #

class an_animation:
    
    def __init__(self,balls):
        """Create an animation of many balls in space

        Args:
            balls (list): a list of "ball" objects
        """
        self.balls = balls
        self.max_len = max([len(self.balls[ii].x_tot) for ii in range(len(self.balls))])
        self.reset_time()
# ------------------------------------------------------------------------------------------------ #
        
    def reset_time(self):
        """If the balls[ii].x_tot or balls[ii].y_tot have the same length, do so"""
        for ii in range(len(self.balls)):
            # stay at the last coordinates while other balls are still moving
            zero_arrayx=np.full((self.max_len-len(self.balls[ii].x_tot)),self.balls[ii].x_tot[-1])
            zero_arrayy=np.full((self.max_len-len(self.balls[ii].x_tot)),self.balls[ii].y_tot[-1])
            self.balls[ii].x_tot = np.concatenate((self.balls[ii].x_tot, zero_arrayx))
            self.balls[ii].y_tot = np.concatenate((self.balls[ii].y_tot, zero_arrayy))
# ------------------------------------------------------------------------------------------------ #
            
    def launch_animation(self,the_interval):
        """launch the animation

        Args:
            the_interval (int): the wanted frames (1 means "many frames/seconds" while 1000 not)
        """
        fig, ax = plt.subplots(1,1,figsize=(9,4))
        plt.xlabel('x [m]')
        plt.ylabel('y [m]')
        self.lines = []
        self.markers = ["o","v","^","<",">","1","2","3","4","s","p","*","h","H","+","x","D","d"]
        
        for ii in range(len(self.balls)): 
            ax.plot(self.balls[ii].x_tot, self.balls[ii].y_tot,c="white")
            line, = ax.plot(self.balls[ii].x_tot[0],self.balls[ii].y_tot[0],marker=rd.choice(self.markers))
            self.lines.append(line)
            
        def animate(tot):
            """Calculates the new data

            Args:
                tot (int): indice of the x_tot and y_tot on which we loop

            Returns:
                self.lines (list): a list of axes
            """
            for ii in range(len(self.balls)): 
                self.lines[ii].set_data(self.balls[ii].x_tot[tot],self.balls[ii].y_tot[tot])
            return self.lines

        plt.tight_layout()
        ani = animation.FuncAnimation(fig,animate,np.arange(0,self.max_len),interval=the_interval,blit=True)
        plt.show()        


# ------------------------------------------------------------------------------------------------ #
#                                             __main__                                             #
# ------------------------------------------------------------------------------------------------ #

if __name__ == '__main__':
    
    mylist = []
    for i in range(12): # number of random balls to generate
        mylist.append(ball(9.81,
                           6,
                           0,
                           0,
                           rd.uniform(2,3),
                           rd.randint(30,85)*np.pi/180,
                           0.8,
                           rd.uniform(0,1)))    

    anim = an_animation(mylist)
    anim.launch_animation(1)
