# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 13:24:49 2020

@author: Lappawat
"""
import numpy as np


x = 1000           # numbers of samples
p = 1              # percentage of being positive
c = 10             # numbers of group
xp = x*p/100       # numbers of positive
s = 10       # randoms s times
cnt_f = [0]*(c+1)        
t_avg = 0


for j in range(s):
    t = c              # numbers of tests
    cnt = 0
    samples = ['N']*(x)
    pos = x*p/100
    while (pos > 0):
        ind = np.random.randint(0,x)
        if samples[ind] == 'N':
            samples[ind] = 'P'
            pos = pos - 1 
    cnt_pos = samples.count('P')
    #print(cnt_pos)
    samples = np.array(samples).reshape(int(c),int(x/c))
    #print(samples)
    
    tmp = []
    for i in range(len(samples)):
        batch = samples[i]
        if 'P' in batch:
            t = t + int(x/c)
            cnt = cnt + 1
            tmp.append(i)
            #print('found in batch %2d' %i)
    
    t_avg = t_avg + t
    cnt_f[cnt] = cnt_f[cnt]+1
    #print(tmp)
    #print('total numbers of tests: %d' %t)

t_avg = t_avg/s
print(cnt_f)
print('average numbers of tests: %6.1f' %t_avg)
