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
        current_state = current_node.get_state()
        
        #Check if goal reached
        if problem.is_goal_state(current_state):
            self.path = current_node.get_path_from_root()
            return self.path
        
        #frontier defined as FIFO queue
        self.frontier = deque()
        self.frontier.append(current_node)
        
        #Track explored nodes for the visualisation tool
        self.explored = []
        
        #reached defined as set of GridPos 
        reached = {problem.get_initial_state()}
        
        while len(self.frontier) > 0:
            current_node = self.frontier.pop() #pops right side of queue
            self.explored.append(current_node) #classify frontier node we about to explore as explored
            
            #s = successor
            for s_node in self.expand(problem, current_node):
                s_state = s_node.get_state()
                
                if problem.is_goal_state(s_state):
                    self.path = s_node.get_path_from_root()
                    return self.path
                
                if s_state not in reached:
                    reached.add(s_state)
                    self.frontier.appendleft(s_node) #appendleft to keep FIFO structure
                        
        return []
    
    def expand(self, problem: SearchProblem, node: SearchNode):
        state = node.get_state()
        successor_list = []
        for successor in problem.get_successors(state):
            cost = node.get_cost() + 1 #problem.ACTION-COST() in coursebook, but it's always 1 in our maze problem
            successor_list.append(SearchNode(successor, node, None, cost))
        return successor_list
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return list(self.explored)