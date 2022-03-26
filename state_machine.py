# -*- coding: utf-8 -*-
"""
Created on Sat Mar 26 18:18:10 2022

@author: natha
"""
from agent import MoveCommand, ShootCommand, Command

class State_Machine:
    
    
    
    def __init__(self):
        state = 0
        
    def IA(self,gamestate,my_data):
        
        if(self.state == 1):
            decision = self.state_1(gamestate,my_data)
            
        
        if(decision[0] == 0):
            return MoveCommand(decision[1])
        else:
            return ShootCommand(decision[1])
        
        
    def state_1(self,gamestate,my_data):
        
        #ANALYSE DATA 
        
        #TAKE DECISION
        
        #1. Evade
        #2. Move to 
        #3. Shoot
            
        
        return 0