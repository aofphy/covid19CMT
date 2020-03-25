# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:11:24 2020

@author: Lappawat
"""
import numpy as np
import random 
import matplotlib.pyplot as plt

### Real data
real_infected = [100,103,106,113,115,124,141,146,147,177,212,272,322,411,599]
date = np.arange(0,len(real_infected))

### Prediction
# Define 5 classes of people depending on how to response
# 0 H = (Highy responsible)
# 1 M = (Moderately responsible)
# 2 N = (Normal)
# 3 R = (Risky)
# 4 I = (Infected/Immuned)

Pop_total = 100000
#Pop_ratio = [0.0,0.0,0.0,1.0,0.0] # population in each classes
R_lst     = [2.2,0.0] # contact rate
infected  = 1     # initial infected people
Pop       = np.array([Pop_total-infected, infected])
Pop_ratio = Pop/Pop_total
print(Pop_ratio)
meeting   = 20     # 1 infected people met 20 people
threshold = 4
length    = 30 # predicted length (days)
healed_day= 7

#zeroth day
day = [0]
covid_infected_day = [infected]
covid_infected_tot = [infected]
covid_healed_day   = [0]
covid_healed_tot   = [0]
covid_tot          = [infected]
sampling = infected*meeting
#begin model
for i in range(length):
    count = 0
    for j in range(sampling):
        # Model the meeting between infected people and other people
        ## transmitter
        Rt = np.random.choice(R_lst,p=Pop_ratio)
        ## receptor
        Rr = np.random.choice(R_lst,p=Pop_ratio)
        # meeting
        covid_test = Rt * Rr * np.random.uniform(0,1)
        #print(covid_test)
        if covid_test > threshold:
            count = count +1
            Pop[0] = Pop[0]-1
            Pop[1] = Pop[1]+1
            Pop_ratio = Pop/Pop_total
    day.append(i+1)
    
    # infected cases
    covid_infected_day.append(count)
    covid_infected_tot.append(covid_infected_tot[-1]+count)
    sampling = count*meeting
    
    # healed cases
    if i< healed_day:
        covid_healed_day.append(0) 
    else:
        covid_healed_day.append(covid_infected_day[i-healed_day])  # healed people
    covid_healed_tot.append(covid_healed_tot[-1]+covid_healed_day[-1])
    
    # net cases
    covid_tot.append(covid_infected_tot[-1]-covid_healed_tot[-1])     
    
plt.plot(date, real_infected, 'ro', label='real')
plt.plot(day,covid_infected_tot,'-',label ="infected")
plt.plot(day,covid_healed_tot,'-',label ="healed")
plt.plot(day,covid_tot,'-',label ="net")
plt.xlabel('day')
plt.ylabel('people')
plt.legend()
plt.show()
    