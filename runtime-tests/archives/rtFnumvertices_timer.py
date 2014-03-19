'''
Tests the runtime of functions. 

Charlie Cabot 
Aug 1 2012

'''

import time
import sys

sys.path.append("/home/ccabot/Documents/bayesian networks project/bayesian/v3_bayesian/PGMlibrary")

from nodedata import NodeData
from graphskeleton import GraphSkeleton
from discretebayesiannetwork import DiscreteBayesianNetwork

def timer(inputfile, trials):

    # load nodedata and graphskeleton
    nd = NodeData()
    skel = GraphSkeleton()
    nd.load(inputfile)
    skel.load(inputfile)

    # topologically order graphskeleton
    skel.toporder()

    # load bayesian network
    bn = DiscreteBayesianNetwork(skel, nd)
    
    # TIME
    totaltime = 0
    for _ in range(trials): 
        start = time.clock()
        ret = bn.randomsample(100)
        elapsed = time.clock() - start
        totaltime += elapsed
    totaltime /= trials

    return totaltime

#timer("/home/ccabot/Documents/bayesian networks project/bayesian/v3_bayesian/PGMlibrary/unittestdict.txt", 10)

