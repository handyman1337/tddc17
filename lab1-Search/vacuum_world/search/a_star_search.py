from typing import List
import heapq
from vacuum_world.search.search_node import SearchNode
from vacuum_world.search.problem import SearchProblem
from vacuum_world.world.grid_pos import GridPos
from .base_search import BaseSearch


class AStarNode(SearchNode):    
    def __init__(self, state, parent, action, cost, h):
        super().__init__(state, parent, action, cost)
        self.h = h
        self.f = cost + h
    
    def __lt__(self, other):
        return self.f < other.f

#We use Manhattan distance as heuristic as it's admissable for city-block
#problems like the vacuum cleaner problem we're working with here.
#This is because every action changes one coordinate by 1 at a cost of 1,
#so no path can be shorter. Also it was kind of a hint from grid_pos.py ;)
class AStarSearch(BaseSearch):

    def __init__(self):
        super().__init__()
    
    def heuristic(self, state: GridPos, problem: SearchProblem) -> int:
        return state.distance_manhattan(problem.goal_state)
    
    def search(self, problem: SearchProblem) -> List[SearchNode]:
        
        self.path = []
        
        initial_state = problem.get_initial_state()
        current_node = AStarNode(initial_state, None, None, 0.0, self.heuristic(initial_state, problem))
        
        #frontier is a priority queue (min-heap) ordered by f
        self.frontier = []
        heapq.heappush(self.frontier, current_node)
        
        #Track explored nodes for the visualisation tool
        self.explored = []
        
        #reached is a lookup table with key: problem state and value: node
        reached = {initial_state: current_node}
        
        while len(self.frontier) > 0:
            current_node = heapq.heappop(self.frontier)
            current_state = current_node.get_state()
            
            self.explored.append(current_node) #classify frontier node we about to explore as explored
            
            if problem.is_goal_state(current_state):
                self.path = current_node.get_path_from_root()
                return self.path
            
            #s = successor
            for s_node in self.expand(problem, current_node):
                s_state = s_node.get_state()
                
                if s_state not in reached or s_node.get_cost() < reached[s_state].get_cost():
                    reached[s_state] = s_node
                    heapq.heappush(self.frontier, s_node)
        
        return []
    
    
    def expand(self, problem: SearchProblem, node: SearchNode):
        state = node.get_state()
        successor_list = []
        for successor in problem.get_successors(state):
            cost = node.get_cost() + 1 #problem.ACTION-COST() in coursebook, but it's always 1 in our maze problem
            h = self.heuristic(successor, problem)
            successor_list.append(AStarNode(successor, node, None, cost, h))
        return successor_list
    
    def get_frontier_nodes(self) -> List[SearchNode]:
        return list(self.frontier)
    
    def get_explored_nodes(self) -> List[SearchNode]:
        return list(self.explored)