# LAB4 THEORY QUESTIONS

## Part 2 model questions:

### a) What is the risk of melt-down in the power plant during a day if no observations have been made? What if there is icy weather?

3% change of melt-down if no observation has been made. It's still 3% change if icy weather has been observed.

![alt text](Kazam_screenshot_00001.png)
![alt text](Kazam_screenshot_00003.png)


### b) Suppose that both warning sensors indicate failure. What is the risk of a meltdown in that case? Compare this result with the risk of a melt-down when there is an actual pump failure and water leak. What is the difference? The answers must be expressed as conditional probabilities of the observed variables, P(Meltdown|...).

P(Meltdown | PumpFailureWarning=T, WaterLeakWarning=T) = 15%
![alt text](Kazam_screenshot_00004.png)

P(Meltdown | PumpFailure=T, WaterLeak=T) = 20%
![alt text](Kazam_screenshot_00005.png)


### c) The conditional probabilities for the stochastic variables are often estimated by repeated experiments or observations. Why is it sometimes very difficult to get accurate numbers for these? What conditional probabilites in the model of the plant do you think are difficult or impossible to estimate?

Things like pump failures or water leaks are difficult to make observations for since we don't intentionally want to experiment with these dangerous actions. In our model it would likely be difficult/inaccurate to estimate for example P(Meltdown | PumpFailure, WaterLeak) as this is a very specific scenario is probably very unlikely in the real world.


### d) Assume that the "IcyWeather" variable is changed to a more accurate "Temperature" variable instead (don't change your model). What are the different alternatives for the domain of this variable? What will happen with the probability distribution of P(WaterLeak | Temperature) in each alternative? 

We could have something similar to the existing model with a boolean domain (e.g. cold/not cold) which simple and easy to model, but unrealistic since we don't know *how* cold. We could also model it as discrete bins (e.g. very cold/cold/warm/very warm) which is probably still pretty easy to model and more realistic. Or we could go for a continous domain with real degrees instead which would be much more difficult to model but probably the most realistic.

## Part 2 coursebook questions:

### a) What does a probability table in a Bayesian network represent?

A probability table in a Bayesian networks represents a conditional distribution of a node given its parents. For example the tables give P(Meltdown | PumpFailure, WaterLeak).


### b) What is a joint probability distribution? Using the chain rule on the structure of the Bayesian network to rewrite the joint distribution as a product of P(child|parent) expressions, calculate manually the particular entry in the joint distribution of P(Meltdown=F, PumpFailureWarning=F, PumpFailure=F, WaterLeakWaring=F, WaterLeak=F, IcyWeather=F). Is this a common state for the nuclear plant to be in?

The probablitydistribution assigns a probablity to every complete assignment of all variables. p(x1...xn) = (multiplication sum from i to n) P(x_i | paraents(x_i))

Take each node in turn with its own parents:

P(!m, !pfw, !pf, !wlw, !wl, !iw) = p(!iw) * p(!wl | !iw) * p(!pf) * p(!wlw | !wl) * p(!pfw | !pf) * p(!m | !pf, !wl) =  

### c) What is the probability of a meltdown if you know that there is both a water leak and a pump failure? Would knowing the state of any other variable matter? Explain your reasoning!

###  d) Calculate manually the probability of a meltdown when you happen to know that PumpFailureWarning=F, WaterLeak=F, WaterLeakWarning=F and IcyWeather=F but you are not really sure about a pump failure.


## Part 3

###  During the lunch break, the owner tries to show off for his employees by demonstrating the many features of his car stereo. To everyone's disappointment, it doesn't work. How did the owner's chances of surviving the day change after this observation?

The chances of surviving without any observations for the radio is 99%, which is decreased to 98% when the radio isn't working.
![alt text](Kazam_screenshot_00013.png)

### The owner buys a new bicycle that he brings to work every day. The bicycle has the following properties:
* P(bicycle_works) = 0.9
* P(survives | ¬moves ∧ melt-down ∧ bicycle_works) = 0.6
* P(survives | moves ∧ melt-down ∧ bicycle_works) = 0.9 
* How does the bicycle change the owner's chances of survival?

The bicycle increases the owner's chance of survival from 99% to approximately 100%. We calculated this by adding a BicycleWorks node to the graph which is a parent to Survives, and updating the probability table for Survives.
![alt text](Kazam_screenshot_00014.png)


### It is possible to model any function in propositional logic with Bayesian Networks. What does this fact say about the complexity of exact inference in Bayesian Networks? What alternatives are there to exact inference?

If the network can represent any propsitional function, then any SAT instance can be encoded as a Bayesian network. Example:

Take a fromula over vars: A,B,C create one root node per variable  with prior 0.5, and one node per connective whose CPT contains only 0s and 1s. This kind of CPT is a truth table wirtten in probability notation, so those nodes are deterministic functions of their parent with the final node representing the complete formula which is going to be satisfied. 

The roots are coin flips, every assignment has a prob. of 2^n and P(formula=T) equals the number of satisfying assignments divided by 2^n. If this is greater than 0, we can satisfy the formula. 

#### Complexity:

A polynominal inference algortihm would therefore guve a poly-time-SAT solver, which means it is NP-hard. 

It sums over every combination of unobserved variables and the number of combinations doubles with each extra variable. Small networks go fast, larger grows with complexity. 

#### Alternatives
One alternative is rejection sampling where we try random samples and throw away the ones that don't match our logic formula. This wastes a lot of examples when there is few solutions to the problem though.

Instead we could also use likelihood weighting which assigns each sample a weight instead of discarding them. There seems to be different methods for this (e.g. Gibbs sampling) but the general idea is that this should work better, especially when solutions satisfying the problem are rare.


## Part 4
### The owner had an idea that instead of employing a safety person, to replace the pump with a better one. Is it possible, in your model, to compensate for the lack of Mr H.S.'s expertise with a better pump?
With bad pump:
![alt text](Kazam_screenshot_00015.png)

With good pump:
![alt text](Kazam_screenshot_00016.png)

As we can see in these screenshots we reduced the chance of meltdown from 3% to 1%, so yes we can partially replace Mr. H.S. with a better pump. Mr H.S. does however monitor both PumpFailureWarnings and WaterLeakWarnings and since the better pump didn't decrease the chances of WaterLeaks we can only replace him partially (he still monitors the WaterLeaks). If we also did some improvement to the WaterLeak situation we could probably replace him fully.


### Mr H.S. fell asleep on one of the plant's couches. When he wakes up he hears someone scream: "There is one or more warning signals beeping in your control room!". Mr H.S. realizes that he does not have time to fix the error before it is to late (we can assume that he wasn't in the control room at all). What is the chance of survival for Mr H.S. if he has a car with the same properties as the owner? Hint: This question involves a disjunction (A or B) which can not be answered by querying the network as is. How could you answer such questions? Maybe something could be added or modified in the network.
The network as is:
![alt text](Kazam_screenshot_00017.png)

If AnyWarning=T and NoticeWarning=F:
![alt text](Kazam_screenshot_00018.png)

We added the AnyWarning node and set it's probability table in such a way that it's a logical OR, so the A or B disjunction becomes solvable by querying. We can see from the images that the survival rate changes from 100% to 99% when the observations has been made that AnyWarning has happened and that Mr H.S. didn't notice warning.


### What unrealistic assumptions do you make when creating a Bayesian Network model of a person?

We basically reduce a person and their irrational choice of actions into a set of boolean variables. No one is "competent 20% of the time" and is an unrealistic premise for modeling real world problems. Also Mr H.S. could in theory learn to become better at his job over time, but we treat the CPTs as fixed and not something that would change over time.


### Describe how you would model a more dynamic world where for example the "IcyWeather" is more likely to be true the next day if it was true the day before. You only have to consider a limited sequence of days.

We could use a dynamic bayesian network with for example copies of the variables throughout the week. We could then model IcyWeather_1, IcyWeather_2, IcyWeather_3, ... and model the change of IcyWeather for consecutive days as IcyWeather_t --> P(IcyWeather_(t+1)=T). For a limited sequence of days as stated in the question this wouldn't be too complex to model, e.g. 5 days means 5 copies which could be put into our bayesian network applet with ease.