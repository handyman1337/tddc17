# LAB4 THEORY QUESTIONS

## Part 2:

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