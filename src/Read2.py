# -*- coding: utf-8 -*-
"""
Created on Sat Feb 19 17:50:23 2022

@author: Damond
"""


import psutil
import os

process = psutil.Process(os.getpid())

with open('Square-Logo-2009.hpgl', 'r') as file:
    readable = True
    string = ""
    while readable:
        read = file.read(1)
        if read != ";" and read != "":
            string += read
        else:
            readable = False
        
    print(string)
    
print(process.memory_info().rss)  # in bytes 

            
            