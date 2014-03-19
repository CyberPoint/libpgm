'''
Tests the runtime of functions. 

Charlie Cabot 
Aug 1 2012

'''

import time
import json
import sys

sys.path.append("../libpgm/")              # make sure this is right

#from pympler.asizeof import asizeof
#from pympler import muppy, summary

from nodedata import NodeData
from graphskeleton import GraphSkeleton
from discretebayesiannetwork import DiscreteBayesianNetwork
from tablecpdfactorization import TableCPDFactorization
from pgmlearner import PGMLearner

op = open("output.csv", 'w')



def timer(inputfile, trials, datalength):

    # load nodedata and graphskeleton
    nd = NodeData()
    skel = GraphSkeleton()
    #print "bp1"
    nd.load(inputfile)
    #print "bp2"
    skel.load(inputfile)
    #print "bp3"

#    msg = "%d, %d" % (asizeof(nd), asizeof(skel))
 #   print >>op, msg

    # topologically order graphskeleton
    skel.toporder()

    # load bayesian network
    bn = DiscreteBayesianNetwork(skel, nd)

    # instantiate pgm learner
    l = PGMLearner()

    # free unused memory
    del nd
    
    #sum1 = summary.summarize(muppy.get_objects())
    #summary.print_(sum1)
    
    # TIME
    totaltime = 0
    for _ in range(trials): 
        data = bn.randomsample(datalength)
        start = time.clock()
        ret = l.discrete_mle_estimateparams(skel, data)
        elapsed = time.clock() - start
        totaltime += elapsed
    totaltime /= trials


    print json.dumps(ret.Vdata, indent=1)
    return totaltime
#timer("/home/ccabot/Documents/bayesian networks project/bayesian/v3_bayesian/PGMlibrary/unittestdict.txt", 10)

