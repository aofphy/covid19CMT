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
length    = 120        # predicted length (days)
meeting   = 10         # 1 infected people can meet 20 people
healed_day= 14         # infected people will be healed in 7 days after being infected

# Define 3 classes of people depending on how to response
# 0 H = (Highy responsible)
# 1 M = (Moderately responsible)
# 2 R = (Risky)
Pop       = [1E7,3E7,2E7]
Pop_tot   = sum(Pop)
R_lst     = [0.1,0.2,0.4] # contact rate
init_infect  = [0,10,0]
for i in range(len(Pop)):
    Pop[i] = Pop[i]-init_infect[i]

#Day 0
day      = [0]
Normal   = [[] for i in range(len(Pop))] # never being infected
Infect   = [[] for i in range(len(Pop))] # sum of being infected and used to
Heal     = [[] for i in range(len(Pop))] # be healed
Net      = [[] for i in range(len(Pop))] # still being infected
for i in range(len(Pop)):
    Normal[i].append(Pop[i])     
    Infect[i].append(init_infect[i])          
    Heal[i].append(0)                   
    Net[i].append(Infect[i][0] - Heal[i][0])  

#begin model
for i in range(length):
    day.append(i+1)
    ### group j meet k
    for j in range(len(Pop)):
        new_infect = 0
        for k in range(len(Pop)):
            Rate  = R_lst[j]*R_lst[k]*meeting
            ### new total infected people
            new_infect = new_infect + Rate*Net[k][-1]*Normal[j][-1]/Pop_tot
        Infect[j].append(Infect[j][-1] + new_infect)
        
        ### new normal people
        Normal[j].append(Normal[j][-1]-new_infect)
        ### new healed people
        if i <= healed_day:
            Heal[j].append(0)
        else:
            new_healed = Infect[j][i-healed_day]-Infect[j][i-healed_day-1]
            Heal[j].append(Heal[j][-1]+new_healed)
        ### new net
        Net[j].append(Infect[j][-1]-Heal[j][-1])
        print('day: %2d Normal: %10.1f Infected: %10.1f Healed: %10.1f Net: %10.1f //%10.1f' %(i,Normal[j][-1],Infect[j][-1],Heal[j][-1],Net[j][-1],new_infect))

#plt.plot(date, real_infected, 'ro', label='real')
for j in range(len(Pop)):
    plt.plot(day,Normal[j],'-',label ="Normal_"+str(j))
    plt.plot(day,Infect[j],'-',label ="Infected_"+str(j))
    plt.plot(day,Heal[j],'-',label ="Healed_"+str(j))
    plt.plot(day,Net[j],'-',label ="Net_"+str(j))
    plt.xlabel('day')
    plt.ylabel('people')
    plt.legend()
    plt.show()

#changing list into nparray
Normal = np.array(Normal)
Infect = np.array(Infect)
Heal   = np.array(Heal)
Net    = np.array(Net)
Normal_sum = np.zeros(len(Normal[0]))
Infect_sum = np.zeros(len(Infect[0]));
Heal_sum = np.zeros(len(Heal[0]))
Net_sum = np.zeros(len(Net[0]))
for j in range(len(Pop)):
    Normal_sum = Normal_sum + Normal[j]
    Infect_sum = Infect_sum + Infect[j]
    Heal_sum   = Heal_sum   + Heal[j]
    Net_sum    = Net_sum    + Net[j]

plt.plot(day,Normal_sum,'-',label ="Normal")
plt.plot(day,Infect_sum,'-',label ="Infected")
plt.plot(day,Heal_sum,'-',label ="Healed")
plt.plot(day,Net_sum,'-',label ="Net")
plt.xlabel('day')
plt.ylabel('people')
plt.legend()
plt.show()

