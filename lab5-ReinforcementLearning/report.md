# LAB 5 REPORT
## Part 2

### Question 1.
    Our state so far is the rocket's angle only. We used the discretize2() function to split the full circle -pi to pi into 10 bins of pi/5 = 36 deg each, which gives our our discrete angle state space.

    The reward function is reward = 1 - abs(angle) / pi. If we for example have an angle of 0 we get a reward of 1 (rocket pointing upwards) and having an angle of ±pi gives us the reward zero (pointing downwards), with angles inbetween like ±pi/2 giving a reward of 0.5 (pointing sidewards). We kept the reward always positive, but it's definitely possible to design the reward function so it also/instead uses negative rewards (penalties).

    The four actions the agent can perform are 0 (all engines off), 1 (middle engine on), 2 (left engine on) and 3 (right engine on). Also every action switches off all engines before turning on the one determined by the action, in order to not have several engines on at once.


### Question 2.
    The update formula is: Q(s,a) ← Q(s,a) + α(r + γ*max Q(s',a') − Q(s,a))

    Q(s,a) is Q-Learning's current estimate for how good action a is in state s. α is the learning rate which controls how much we should actually update our Q-table, with a higher LR making us do huge updates and a lower LR meaning we do more careful updates. r is the actual reward (not an estimate) we just got when changing from previous state to new state. γ is the discount factor which is used to control how much the agent prefers immediate reward right now compared to long-term reward in the future. Finally max Q(s',a') is the value of the best action available in the newly entered state s'.
    
    The Q-table contains Q-values for all combinations of states s and actions a. A Q-value basically tells us how big of an expected total future reward we'll get in state s for taking action a and continuing with high-reward actions from there. The Q-values are learned and helps our agent maximize its total long-term reward while training so that we over time can find an optimal policy.


### Question 3.
    The Q-table seems to be initialized with 0 at every position as each action gives 0 reward at the start of the simulator. So when we turn exploration off before learning starts, we basically ask the agent to always pick the highest Q-value even though all of them are 0. This results in the agent always picking action 0 and never turning the engines on, making the agent repeatedly fall to its death and never learning anything useful.