import random

from rich import print
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
    max_depth = 8
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
            move = max(utilities, key=lambda m: utilities[m])
        else:
            move = min(utilities, key=lambda m: utilities[m])
            
        print(f"[{DCOL_AI}][AI] [white]MinMax: {MinMax.expanded_states} states expanded, "
              f"utilities {utilities}, playing {move} for a utility of {utilities[move]}")
            
        return move
    
    @staticmethod
    def minmax(state: State, depth):
        available_moves = state.available_moves()
        
        if not available_moves or depth == 0:
            return state.score
        
        MinMax.expanded_states += 1
        
        utilities = [MinMax.minmax(state.next_state(move), MinMax.decrement(depth))
                     for move in available_moves]
        
        if state.current_player == 0:
            return max(utilities)
        return min(utilities)
    
    @staticmethod
    def decrement(depth):
        if depth is None:
            return None
        return depth - 1
        

class AlphaBeta(AI):
    max_depth = 8
    expanded_states = 0
    pruned_branches = 0
    
    @staticmethod
    def best_move(current_state: State, objective: Objective):
        state = current_state.copy()
        
        available_moves = state.available_moves()
        if not available_moves:
            return None

        AlphaBeta.expanded_states = 1
        AlphaBeta.pruned_branches = 0
        
        alpha, beta = float("-inf"), float("inf")
                
        utilities = {}
        
        for move in available_moves:
            utilities[move] = AlphaBeta.alphabeta(
                state.next_state(move), AlphaBeta.decrement(AlphaBeta.max_depth), alpha, beta
            )
            
            if objective == Objective.MAX:
                alpha = max(alpha, utilities[move])
            else:
                beta = min(beta, utilities[move])
        
        if objective == Objective.MAX:
            move = max(utilities, key=lambda m: utilities[m])
        else:
            move = min(utilities, key=lambda m: utilities[m])
        print(f"[{DCOL_AI}][AI] [white]AlphaBeta: {AlphaBeta.expanded_states} states expanded, "
              f"{AlphaBeta.pruned_branches} branches pruned, utilities {utilities}, "
              f"playing {move} for a utility of {utilities[move]}")
            
        return move
    
    @staticmethod
    def alphabeta(state: State, depth, alpha, beta):
        available_moves = state.available_moves()
        
        if not available_moves or depth == 0:
            return state.score
        
        AlphaBeta.expanded_states += 1
        
        if state.current_player == 0:
            value = float("-inf")
            for move in available_moves:
                value = max(value, AlphaBeta.alphabeta(
                    state.next_state(move), AlphaBeta.decrement(depth), alpha, beta))
                alpha = max(alpha, value)
                if value >= beta:
                    AlphaBeta.pruned_branches += 1
                    break
            return value
        
        value = float("inf")
        for move in available_moves:
            value = min(value, AlphaBeta.alphabeta(
                state.next_state(move), AlphaBeta.decrement(depth), alpha, beta))
            beta = min(beta, value)
            if value <= alpha:
                AlphaBeta.pruned_branches += 1
                break
        return value
        
    @staticmethod
    def decrement(depth):
        if depth is None:
            return None
        return depth - 1
