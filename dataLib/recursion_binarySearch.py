# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 13:32:49 2021

@author: kingw
"""

"""
Work on:
    definig target air property for search(atitude, temp, density, etc)
        maybe convert to a pandas based instead of just lists to handle this
"""

def atmProperties(table, target):
    n = len(data)
    up = n
    down = 0
    ind = round(n/2,0)
    out = []
    
    recur_binarySearch_interp(table, out, target, up, down, ind)
    
def interpolate(data,targetup,down):
    up_array = data[up]
    down_array = data[down]
    
    up_target = 0
    down_target = 0
    
    value = []
    for i in range(len(up_array)):
        value[i] = up_array[i] + (target - up_target) * (down_array[i] - up_array[i]) / (down_target - up_target)
    
    return value
    
    
def recur_binarySearch_interp(data,target,up,down,ind):
    if len(out) == 0:
        value = data[ind]
        if value > target:
            up = ind
        elif value < target:
            down = ind
        elif value == target:
            #lead to terminal
            down = ind
            
        range_mag = abs(up-down)
        ind = down + round(range_mag/2,0)
        
        #lead to terminal case
        if range_mag == 1:
            out = [up,down]
            
        recur_binarySearch_interp(data,target,up,down,ind)
    else:
        #terminal cases
        if len(out) == 2:
            interpolate(data,target,up,down)
        else:
            return value
        
            