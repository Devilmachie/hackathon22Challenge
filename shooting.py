# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 14:51:42 2022

@author: natha
"""

import numpy as np
import scipy as sp
from scipy.optimize import newton


MISSILE_SPEED = 300

def shooting(x,ennemy_pos,ennemy_speed,player_pos):
    d = np.array([np.cos(x),np.sin(x),0])
    
    ve = ennemy_speed
    vm = MISSILE_SPEED*d
    
    t = (ennemy_pos[0] - player_pos[0])/(vm[0]-ve[0])
    
    pe = ennemy_pos+t*ennemy_speed
    pm = player_pos+t*MISSILE_SPEED*d
    
    return np.linalg.norm(pm-pe)

def shoot_on_ennemy_prevision(gamestate):
    player_pos = np.array(gamestate.controlled_player.position)
    ennemy_pos = np.array(gamestate.other_players[0].position)
    ennemy_speed  = np.array(gamestate.other_players[0].speed)
    
    dir0 = ennemy_pos-player_pos
    #Calcul de l'angle de tir
    angle0 = shoot_dir(dir0)
    x0 = angle0
    
    try: 
        res = newton(shooting,x0=x0,args=(ennemy_pos,ennemy_speed,player_pos))
        if(shooting(res,ennemy_pos,ennemy_speed,player_pos)<0.01):
            return res*180/np.pi
        else:
            return angle0*180/(np.pi)
    except:
        return angle0*180/(np.pi)
    
    
def shoot_dir(direction):
    
    dx = direction[0]
    dy = direction[1]
    L = np.sqrt(dx**2+dy**2)
    
    angle0 = np.arccos(dx/L)
    if(dy<0):
        angle0 = 2*np.pi-angle0
        
    return angle0
    
    
def shoot_corner(gamestate,corner):

    """
    Corner: up or down
    """
    
    ennemy_pos = np.array(gamestate.other_players[0].position)
    player_pos = np.array(gamestate.controlled_player.position)
    x,y = ennemy_pos[0],ennemy_pos[1]
    
    if(corner == 'up'):
        target_1 = np.array([0,200,0])
        target_2 = np.array([-200,0,0])
        if(-x>y): 
            target = target_2
        else:
            target = target_1
    else:
        target_1 = np.array([0,-200,0])
        target_2 = np.array([200,0,0])
        if(-x>y):   
            target = target_1
        else:
            target = target_2
            
    return shoot_dir(target-player_pos)*180/np.pi
        
        
def shooting_decision(world_map,gamestate):
    
    player_pos = np.array(gamestate.controlled_player.position)
    ennemy_pos = np.array(gamestate.other_players[0].position)
    #34 = 125-91
    if( (ennemy_pos[0] < -200 and ennemy_pos[1] > 34) or (ennemy_pos[0] < -34 and ennemy_pos[1] > 200)):
        res = shoot_corner(gamestate,'up')
    elif( (ennemy_pos[0] > 200 and ennemy_pos[1] < -34) or (ennemy_pos[0] > 34 and ennemy_pos[1] < -200)):
        res = shoot_corner(gamestate,'down')
    else:
        res = shoot_on_ennemy_prevision(gamestate)
        
    return res
    
