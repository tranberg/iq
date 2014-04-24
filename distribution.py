import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

"""
Script that uses population sizes and mean IQs to build a compound population
and calculate the effect on the standard deviation.
"""

# Set to 1 if you want to see plots.
show = 1

# Set to 1 if you want to see printouts.
verbose = 1

def printer(string):
    if verbose == 1:
        print(string)
        
def stdd(values, weights):
    """
    Return the standard deviation of the given values.
    """
    average = np.average(values, weights=weights)
    variance = np.average((values-average)**2, weights=weights)
    return np.sqrt(variance)

# Load distribution data from file
data = np.loadtxt('data.txt',delimiter=',',skiprows=1)
printer('Loaded '+str(len(data))+' distributions')

nd = len(data)  # number of distributions
dx = 0.001      # step size, smaller is better
sd = 15         # we assume all distributions have standard deviation of 15
sdrange = 2     # range of standard deviations

mid = data[:,1]     # the mean IQs of the populations. 
pop = data[:,0]     # population sizes
printer('pop sizes: '+str(pop))
printer('mean IQs: '+str(mid))

x = np.arange(-sdrange*sd,sdrange*sd+dx,dx) # x axis is IQ
y = np.zeros((len(x)-1,nd+1)) # y axis is number of people. Last column contains
                              # the compound distribution

intmids = x[:-1]+.5*dx      # midpoints of all intervals

# Build all distributions and combine them
for i in range(nd+1):
    if i < nd:
        d = (mid[0]-mid[i])/sd
        y[:,i] = (norm.cdf(x[:-1]+dx+d)-norm.cdf(x[:-1]+d))*pop[i]
    else:
        y[:,i] = np.sum(y,1)

# Plotting of distributions.
# Remember to add a legend at some point.
if show == 1:
    xx = (x[:-1]*sd)+mid[0]
    plt.figure()
    for i in range(nd):
        plt.plot(xx,y[:,i],'b')
    plt.plot(xx,y[:,-1],'r')
    plt.xlabel('IQ')
    plt.ylabel('Number of people')
    plt.title('People vs. IQ distributions')
    plt.axis([np.min(mid)-50,np.max(mid)+50,0,1.1*np.max(y)])
    plt.show()

# Calculate sd in compound distribution and compare to the master
sdds = []
for j in range(nd+1):
    sdds.append(stdd(intmids,y[:,j]))
printer('Standard deviations: '+str(sdds))
printer('Increase in standard deviation from dominant population to compound:')
sdinc = (sdds[-1]-sdds[0])/sdds[0]*100
printer(str(round(sdinc,4))+'%')

