# -*- coding: utf-8 -*-
"""
Created on Sun Mar 27 10:49:45 2022

@author: natha
"""

from game_simulation import GameSimulation, SnapshotData
from agent import MoveCommand, ShootCommand, Command
import numpy as np
import typing
import shooting
import evasion

def ai_de_la_mort_qui_tue_tout(gamestate: SnapshotData, my_data: typing.Dict) -> Command:
    '''
    This function is the deliverable that the participants need to upload at the end of the event.
    
    It has to return either a MoveCommand((dx, dy, 0.0)), where dx and dy are float value. 
    (The vector is normalized to 1).
    
    Or it can return a ShootCommand(angle), where the angle is in degrees and in counterclockwise order.
    (Angle 0.0 corresponds to EAST, 270.0° to SOUTH etc...)
    
    The gamestate variable is a collection of information containing the player data as well as the projectile data.
    Please check the SnapshotData class in the agent.py script.
    
    The my_data variable is a dictionnary that persists each time that the function is called. Its an utilitary
    that can be used by the participants at will. 
    
    Its also returned at the END of the game simulation, so it can be used for everything.
    
    The obstactles in game are always the same and described in another document.  Feel free to hardcode them inside the function.
    '''
    if my_data.get('counter') is None:
        my_data['counter'] = 1
    else:
        my_data['counter'] += 1
        
    player_pos = gamestate.controlled_player.position
        
    if player_pos[0] > 0:
        speed = np.array([-1.0, 0.0, 0.0])
        speed = evasion.evade_all(None,gamestate,speed)
        return MoveCommand((speed[0],speed[1],speed[2]))
    elif(np.abs(player_pos[0]) > 100 and np.abs(player_pos[1]) > 100):
        speed = -np.array(gamestate.controlled_player.position)
        speed = evasion.evade_all(None,gamestate,speed)
        return MoveCommand((speed[0],speed[1],speed[2]))
    
    if(evasion.should_evade(gamestate)):
        speed = np.array([0.0, 0.0, 0.0])
        speed = evasion.evade_all(None,gamestate,speed)
        return MoveCommand((speed[0],speed[1],speed[2]))
    else:
        res = shooting.shooting_decision(None,gamestate)
        return ShootCommand(res)
