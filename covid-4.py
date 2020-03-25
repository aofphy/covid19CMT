# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 13:11:24 2020

@author: Lappawat
"""
import numpy as np
import matplotlib.pyplot as plt

### Real data
real_infected = [100,103,106,113,115,124,141,146,147,177,212,272,322,411,599,721]
date = np.arange(0,len(real_infected))

### Prediction

############### Parameters ##########################
ini_infected  = 10     # initial infected people
length    = 150     # predicted length (days)
meeting   = 10     # 1 infected people can meet 20 people
healed_day= 14      # infected people will be healed in 7 days after being infected
Pop_total = 6E7
# Define 3 classes of people depending on how to response
# 0 H = (Highy responsible)
# 1 M = (Moderately responsible)
# 2 R = (Risky)
Pop       = 6E7
R_lst     = 0.15 # contact rate
Pop = Pop-ini_infected
#Day 0
Normal   = [Pop]                # never being infected
Infect   = [ini_infected]          # sum of being infected and used to
Heal     = [0]                     # be healed
Net      = [Infect[0] - Heal[0]]   # still being infected
day      = [0]
### group 0 meet 0
Rate      = R_lst*R_lst*meeting
#begin model
for i in range(length):
    ### new total infected people
    day.append(i+1)
    new_infect = Rate * Normal[-1]/Pop * Net[-1]
    Infect.append(Infect[-1] + new_infect)
    ### new normal people
    Normal.append(Normal[-1]-new_infect)
    ### new healed people
    if i <= healed_day:
        Heal.append(0)
    else:
        new_healed = Infect[i-healed_day]-Infect[i-healed_day-1]
        Heal.append(Heal[-1]+new_healed)
    ### new net
    Net.append(Infect[-1]-Heal[-1])
    print('day: %2d Normal: %10.1f Infected: %10.1f Healed: %10.1f Net: %10.1f //%5.3f' %(i,Normal[-1],Infect[-1],Heal[-1],Net[-1],Rate * Normal[-1]/Pop))

#plt.plot(date, real_infected, 'ro', label='real')
plt.plot(day,Normal,'-',label ="Normal")
plt.plot(day,Infect,'-',label ="Infected")
plt.plot(day,Heal,'-',label ="Healed")
plt.plot(day,Net,'-',label ="Net")
plt.xlabel('day')
plt.ylabel('people')
plt.legend()
plt.show()

