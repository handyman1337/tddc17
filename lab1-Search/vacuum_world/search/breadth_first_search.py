from typing import List
from collections import deque
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from .base_search import BaseSearch


class BreadthFirstSearch(BaseSearch):

    def __init__(self):
        super().__init__()
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        
        self.path = []
        
        initial_state = problem.get_initial_state()
        current_node = SearchNode(initial_state, None, None, 0.0)
        path_nodes = [current_node]
        
        steps = 0
        
        while steps < self.max_depth: #TODO: Unsure if it should be steps or current_depth here?
            current_state = current_node.get_state()
            
            #Check if goal reached
            if problem.is_goal_state(current_state):
                self.path = path_nodes
                return self.path
            
            #frontier defined as FIFO queue
            frontier = deque()
            frontier.append(current_node)
            
            #reached defined as set of GridPos 
            reached = {problem.get_initial_state()}
            
            while len(frontier) > 0:
                current_node = frontier.pop() #pops right side of queue
                
                #Get all possible successors/children
                successors = problem.get_successors(current_state)
                
                if not successors:
                    break
                
                for successor in successors:
                    if problem.is_goal_state(successor):
                        return successor
                    
                    if successor not in reached:
                        reached.add(successor)
                        frontier.appendleft(successor) #appendleft to keep FIFO structure
                        
        return []
    
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return []
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return []