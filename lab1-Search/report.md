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