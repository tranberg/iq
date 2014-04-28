import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import sys

"""
Script that uses population sizes and mean IQs to build a compound population
and calculate the effect on the standard deviation.

Example on how to call the script:
python distribution.py data.txt show verbose all

The first argument is the file containing the data. Explanations of the rest:
show:       show figure while running
verbose:    extra output

Only one of the two following can be used at a time:
all:        shows individual countries in the figure
summed:     shows aggregation of all countries in the figure

"""

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

def plotter(figtype,x,y):
    # Plotting of distributions.
    # Remember to add a legend at some point.
    xx = (x[:-1]*sd)+mid[0]
    y *= normfactor 
    plt.figure()
    if figtype == 'all':
        plt.plot(xx,y[:,0],'b')
        for i in range(nd-1):
            plt.plot(xx,y[:,i+1],'c')
        plt.plot(xx,y[:,-1],'r')
    elif figtype == 'summed':
        plt.plot(xx,y[:,0],'b')
        plt.plot(xx,y[:,-1],'c')
        plt.plot(xx,y[:,-2],'r')
    plt.xlabel('IQ')
    plt.ylabel('Number of people')
    plt.title('People vs. IQ distributions')
    plt.axis([np.min(mid)-50,np.max(mid)+50,0,1.1*np.max(y)])
    plt.savefig('iqsum_'+str(len(data))+'_'+figtype+'.png')
    print('Saved figure iqsum_'+str(len(data))+'_'+figtype+'.png')
    if show == 1:
        plt.show()

infile = sys.argv[1]    # specifies what file to load. Include extension.
modes = str(sys.argv)

if 'show' in modes:
    show = 1
else:
    show = 0
if 'verbose' in modes:
    verbose = 1
else:
    verbose = 0
if (('all' not in modes) and ('summed' not in modes)):
    raise Exception('No plotting mode selected. Use \'all\' or \'summed\'.')
if (('all' in modes) and ('summed' in modes)):
    raise Exception('Too many plotting mode selected. Use only \'all\' or \'summed\'.')
if ('all' in modes):
    figtype = 'all'
elif ('summed' in modes):
    figtype = 'summed'

# Load distribution data from file
data = np.loadtxt(infile,delimiter=',',skiprows=1)
print('Loaded '+str(len(data))+' distributions')

nd = len(data)  # number of distributions
dx = 0.0001     # step size, smaller is better
sd = 15         # we assume all distributions have standard deviation of 15
sdrange = 5     # range of standard deviations to include

mid = data[:,1]     # the mean IQs of the populations. 
pop = data[:,0]     # population sizes
printer('pop sizes: '+str(pop))
printer('mean IQs: '+str(mid))

x = np.arange(-sdrange,sdrange+dx,dx)   # x axis is IQ
intmids = x[:-1]+.5*dx                  # midpoints of all intervals

normfactor = (1/dx)/(sd*sdrange*2)      # factor for normalising y axis

# Build all distributions and combine them
if 'all' in modes:
    y = np.zeros((len(x)-1,nd+1)) # y axis is number of people.
    for i in range(nd+1):
        if i < nd:
            d = (mid[0]-mid[i])/sd
            y[:,i] = (norm.cdf(x[:-1]+dx+d)-norm.cdf(x[:-1]+d))*pop[i]
        else:
            y[:,i] = np.sum(y,1)

    plotter(figtype,x,y)

    # Calculate sd in compound distribution and compare to the master
    sdds = []
    for j in range(nd+1):
        sdds.append(stdd(intmids,y[:,j]))
    printer('Standard deviations: '+str(sdds))
    print('Increase in standard deviation from dominant population to compound:')
    sdinc = (sdds[-1]-sdds[0])/sdds[0]*100
    print(str(round(sdinc,4))+'%')

elif 'summed' in modes:
    y = np.zeros((len(x)-1,nd+2)) # y axis is number of people.
    for i in range(nd+2):
        if i < nd:
            d = (mid[0]-mid[i])/sd
            y[:,i] = (norm.cdf(x[:-1]+dx+d)-norm.cdf(x[:-1]+d))*pop[i]
        elif i == nd:
            y[:,i] = np.sum(y,1)
        else:
            y[:,i] = np.sum(y[:,1:-2],1)
    plotter(figtype,x,y)

    # Calculate sd in compound distribution and compare to the master
    sdds = []
    for j in range(nd+1):
        sdds.append(stdd(intmids,y[:,j]))
    printer('Standard deviations: '+str(sdds))
    print('Increase in standard deviation from dominant population to compound:')
    sdinc = (sdds[-1]-sdds[0])/sdds[0]*100
    print(str(round(sdinc,4))+'%')
