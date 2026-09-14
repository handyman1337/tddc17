# LAB1 THEORY QUESTIONS

## 1. What is the difference between Breadth-First Search and Uniform Cost Search in a domain where the cost of each action is 1?

Main difference between BFS and UCS:
* BFS explores by layers in the search tree. All nodes do step 1 down, then from this layer we do 1 more step down, etc. Here we use a FIFO queue.

* UCS explores by cheapest path so far in the search tree. We traverse to the next node that gives us the lowest total cost this far. Here we use a priority queue.

In the vacuum world problem every action costs 1, which makes the number of steps in the path and the total cost of the path equal to each other. For example, to reach a node 3 steps down the path will have the cost 3. The priority queue of UCS therefore will become a FIFO queue in this specific example and we will process the nodes in the same order for both algorithms. This means BFS and UCS are basically the same algorithm when applied to the vacuum world problem.


## 2. Suppose that h1 and h2 are admissible heuristics (used in A*). Which of the following are also admissible? Justify your answers.

Heuristics are admissable if they never overestimate, meaning that they are allowed to be optimistic, but _not_ pessimistic. Let's call the true cost to the goal h*. The heuristics provided in the questions are then optimal if h_i ≤ h* where we know the components h_1 and h_2 are admissable.

### (h_1 + h_2)/2

h_1 ≤ h*, h_2 ≤ h*

--> h_1 + h_2 ≤ 2h*

--> (h_1 + h_2)/2 ≤ h*

--> The given heuristic is admissable!


### 2h_1

h_1 ≤ h*

--> 2h_1 ≤ 2h*

--> The given heuristic is **not** admissable, because it's not ≤ h*.


### max(h_1, h_2)

h_1 ≤ h*, h_2 ≤ h*

--> max(h_1, h_2) ≤ h*

--> The given heuristic is admissable! (picking either h_1 or h_2 will still be admissable due to both of them being admissable by themselves)


## 3. For each of the following search algorithms, determine whether they are complete and optimal. Give a quick explanation why.

Definitions of terminology:
* Complete = If there exists a solution, the algorithm will find it.
* Optimal = The solution found will always be the one with lowest cost.

BFS: It checks the search space layer by layer, so it will find the solution eventually and is therefore **complete**. It finds the least deep solution so it's **only optimal when all steps have the same cost**.

DFS: We keep going down in the same branch in the search tree until we reach the bottom. If there are loops in the search tree we will get stuck, and therefore DFS is **not complete**. It's **not optimal** either since we finish once we have found the first solution and we don't check the whole search space.

UCS: Since we continually look for the lowest cost path, we will gradually check the entire search space so it is **complete**. We check the paths in order from lower to higher total path cost, so by definition we will also find the **optimal** solution. 

Iterative deepening: This is DFS with depth limits that we continually increase. We will therefore fully check every layer of the search tree in a similar fashion to BFS, which makes this algorithm **complete**. We check only the number of steps instead of total path cost, meaning that it's **only optimal when all steps have the same cost**.

Bidirectional: Here we start two searches, one from the starting node and one backwards from the goal, and then we keep going until the searches meet in the middle (see image on coursebook page 91 for illustration). This means that the algorithm is **complete only if both directions use BFS**. Similarly if both sides BFS bidirectional search will be **only optimal when all steps have the same cost**.

Greedy best-first search: Here we always expand the node that is closest to the goal according to some heuristic e.g. straight-line distance. By following this algorithm we will therefore go down some branch and investigating deeply rather than layer by layer (similarly to DFS). Greedy best-first search is therefore **not complete** and **not optimal** either.

A*: This algorithm is identical to UCS with the difference that we calculate search costs by using the total cost to reach a node g + the heuristic h (UCS uses only g). Similarly to UCS, it is **complete** as we check lower to higher total cost paths meaning we will eventually find the solution if there is one. It is **only optimal if h is admissable**, which is explained in the question above.