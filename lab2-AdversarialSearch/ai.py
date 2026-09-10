import random

from game import AI, State, Objective
from settings import DCOL_AI


class Random(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        state = current_state.copy()

        available_moves = state.available_moves()
        if not available_moves:
            return None

        return random.choice(available_moves)


class MinMax(AI):
    max_depth = None
    expanded_states = 0
    
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        state = current_state.copy()
        
        available_moves = state.available_moves()
        if not available_moves:
            return None

        #The root is about to be expanded, so it counts as one expanded state
        MinMax.expanded_states = 1
        
        utilities = {move: MinMax.minmax(state.next_state(move), MinMax.decrement(MinMax.max_depth))
                     for move in available_moves}
        
        if objective == Objective.MAX:
            move = max(utilities, key=utilities.get)
        else:
            move = min(utilities, key=utilities.get)
            
            
        
        glocken_is_gay = 0
        return glocken_is_gay
    
    @staticmethod
    def minmax(state: State, depth):
        available_moves = state.available_moves()
        
        if not available_moves or depth == 0:
            return state.score
        
        MinMax.expanded_states += 1
        
        utilities = {move: MinMax.minmax(state.next_state(move), MinMax.decrement(MinMax.max_depth))
                             for move in available_moves}
        
        if state.current_player == 0:
            return max(utilities)
        return min(utilities)
    
    @staticmethod
    def decrement(depth):
        if depth is None:
            return None
        return depth - 1
        

class AlphaBeta(AI):
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        pass
