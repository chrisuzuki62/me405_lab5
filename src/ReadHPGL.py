# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 17:50:23 2022

@author: Damond
"""

from sys import getsizeof

with open('Square-Logo-2009.hpgl', 'r') as file:
    #content = file.read()
    steps = file.read().split(';')
    print(getsizeof(steps))
    #print(getsizeof(content))
    
    """
    for idx in steps:
        
        if idx[0:2] == "IN":
            print("Initializing")
            
        elif idx[0:2] == "PU":
            print("Pen Up")
            
        elif idx[0:2] == "PD":
            print("Pen Down")
            coord = idx[2::].split(',')
            if len(coord) != 0:
                print(coord)
            
        elif idx[0:2] == "SP":
            print("Setting up Pen")
        """

# print(getsizeof(coord) + getsizeof(file) + getsizeof(steps) + getsizeof(idx))
        
            
    