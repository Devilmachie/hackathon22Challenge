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
import pathFinding

def ai_de_la_mort_qui_tue_tout(gamestate: SnapshotData, my_data: typing.Dict) -> Command:

    if my_data.get('counter') is None:
        my_data['counter'] = 1
    else:
        my_data['counter'] += 1
        
    if(my_data.get('info_map') is None):
        my_data['info_map'] = pathFinding.initObjects()
        
    player_pos = gamestate.controlled_player.position
        
    if(np.abs(player_pos[0]) > 100 and np.abs(player_pos[1]) > 100):
        speed = pathFinding.goTo(my_data['info_map'][0],my_data['info_map'][1],player_pos,[0,0,0])
        #speed = -np.array(gamestate.controlled_player.position)
        speed = evasion.evade_all(None,gamestate,speed)
        return MoveCommand((speed[0],speed[1],speed[2]))
    
    if(evasion.should_evade(gamestate)):
        speed = np.array([0.0, 0.0, 0.0])
        speed = evasion.evade_all(None,gamestate,speed)
        return MoveCommand((speed[0],speed[1],speed[2]))
    else:
        res = shooting.shooting_decision(None,gamestate)
        return ShootCommand(res)
