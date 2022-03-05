# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 17:50:23 2022

@author: Damond
"""

from matplotlib import pyplot as plt

not_finished = True
buffer = ""

X = []
Y = []

with open('Test.hpgl', 'r') as file:
    while not_finished:
        boolean = True
        while boolean:
            char = file.read(1)
            if char == "":
                not_finished = False
                boolean = False
            elif char == ";":
                boolean = False
            else:
                buffer += char
        
        if buffer[0:2] == "IN":
            pass
            # print("Initializing")
            
        elif buffer[0:2] == "PU":
            pass
            # print("Pen Up")
            
        elif buffer[0:2] == "PD":
            pass
            # print("Pen Down")
            
        elif buffer[0:2] == "SP":
            pass
            # print("Setting up Pen")
        
        coord = buffer[2::].split(',')
        if len(coord) >= 2:
            x = 0
            y = 1
            for pp in range(len(coord)//2):
                X.append(int(coord[x]))
                Y.append(int(coord[y]))
                x += 2
                y += 2
            
        buffer = ""
        boolean = True
        
plt.plot(X, Y)