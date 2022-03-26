# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 19:54:43 2022

@author: natha
"""
import numpy as np

player_dim = [32,32]
missile_dim = [32,16]

def evade_all(board,gamestate,speed):
    
    projectile_list = gamestate.projectiles
    
    for projectile in projectile_list:
        speed = evade(projectile,gamestate,speed)
    return speed
        
def evade(projectile,gamestate,speed):
    
    sec_dist = 1e-5
    eps = 1e-6
    dt = 1e-5
    k=5000
    
    player_pos = np.array(gamestate.controlled_player.position)
    projectile_pos = np.array(projectile.position)
    projectile_speed = np.array(projectile.speed)
    
    #rien que pour toi sacha
    if(-np.linalg.norm(player_pos-projectile_pos) + np.linalg.norm(projectile_pos+projectile_speed*dt-player_pos) < sec_dist):
        
        perp_vit = np.cross(projectile_speed,[0,0,1])
        perp_vit /= np.linalg.norm(perp_vit)
        z_cross = np.cross(projectile_speed,player_pos-projectile_pos)[2]
        #If player-projectile positions is parallel to projectile speed
        #We move to a random direction
        if(np.abs(z_cross) < 1e-16):
            direction = 1
        else:
            direction = np.sign(z_cross)
        
        f_rep = k/(np.linalg.norm(projectile_pos-player_pos)+eps)
        
        speed -= perp_vit*f_rep*direction
    
    return speed
    
    