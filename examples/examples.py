'''
This module contains some example uses of the PGM library. 

It is intended to be viewed as sample code, but every entry may be run. 
Simply untoggle the print statement of an entry and run the module to see 
that entry in action.

'''
import json
import sys

# add to PYTHONPATH
sys.path.append("../")

from libpgm.nodedata import NodeData
from libpgm.graphskeleton import GraphSkeleton
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.lgbayesiannetwork import LGBayesianNetwork
from libpgm.hybayesiannetwork import HyBayesianNetwork
from libpgm.dyndiscbayesiannetwork import DynDiscBayesianNetwork
from libpgm.tablecpdfactorization import TableCPDFactorization
from libpgm.sampleaggregator import SampleAggregator
from libpgm.pgmlearner import PGMLearner

# (1) ---------------------------------------------------------------------
# Generate a sequence of samples from a discrete-CPD Bayesian network

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittestdict.txt")
skel.load("../tests/unittestdict.txt")

# topologically order graphskeleton
skel.toporder()

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)

# sample 
result = bn.randomsample(10)

# output - toggle comment to see
#print json.dumps(result, indent=2)

# (2) ----------------------------------------------------------------------
# Generate a sequence of samples from a linear Gaussian-CPD Bayesian network

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittestlgdict.txt")
skel.load("../tests/unittestdict.txt")

# topologically order graphskeleton
skel.toporder()

# load bayesian network
lgbn = LGBayesianNetwork(skel, nd)

# sample 
result = lgbn.randomsample(10)

# output - toggle comment to see
#print json.dumps(result, indent=2)

# (3) ----------------------------------------------------------------------
# Generate a sequence of samples from a hybrid (any CPD type) Bayesian network.

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittesthdict.txt")
skel.load("../tests/unittestdict.txt")

# topologically order graphskeleton
skel.toporder()

# convert nodes to class instances
nd.entriestoinstances()

# load bayesian network
hybn = HyBayesianNetwork(skel, nd)

# sample 
result = hybn.randomsample(10)

# output - toggle comment to see
#print json.dumps(result, indent=2)

# (4) ------------------------------------------------------------------------
# Generate a sequence of samples from a discrete-CPD Bayesian network, given evidence

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittestdict.txt")
skel.load("../tests/unittestdict.txt")

# toporder graph skeleton
skel.toporder()

# load evidence
evidence = dict(Letter='weak')

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)

# load factorization
fn = TableCPDFactorization(bn)

# sample 
result = fn.gibbssample(evidence, 10)

# output - toggle comment to see
#print json.dumps(result, indent=2)

# (5) --------------------------------------------------------------------------
# Compute the probability distribution over a specific node or nodes

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittestdict.txt")
skel.load("../tests/unittestdict.txt")

# toporder graph skeleton
skel.toporder()

# load evidence
evidence = dict()
query = {"Grade":['A']}

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)

# load factorization
fn = TableCPDFactorization(bn)

# calculate probability distribution
result = fn.condprobve(query, evidence)

# output - toggle comment to see
#print json.dumps(result.vals, indent=2)
#print json.dumps(result.scope, indent=2)
#print json.dumps(result.card, indent=2)
#print json.dumps(result.stride, indent=2)

# (6) ---------------------------------------------------------------------------
# Compute the exact probability of an outcome

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittestdict.txt")
skel.load("../tests/unittestdict.txt")

# toporder graph skeleton
skel.toporder()

# load evidence
evidence = dict(Letter='weak')
query = dict(Intelligence=['high'])

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)

# load factorization
fn = TableCPDFactorization(bn)

# calculate probability distribution
result = fn.specificquery(query, evidence)

# output - toggle comment to see
#print result

# (7) --------------------------------------------------------------------------
# Compute the approximate probability distribution by generating samples

# load nodedata and graphskeleton
nd = NodeData()
skel = GraphSkeleton()
nd.load("../tests/unittestdict.txt")
skel.load("../tests/unittestdict.txt")

# topologically order graphskeleton
skel.toporder()

# load bayesian network
bn = DiscreteBayesianNetwork(skel, nd)

# build aggregator
agg = SampleAggregator()

# average samples
result = agg.aggregate(bn.randomsample(10))

# output - toggle comment to see
#print json.dumps(result, indent=2)

# (8) --------------------------------------------------------------------------
# Learn the CPDs of a discrete Bayesian network, given data and a structure:

# say I have some data
data = bn.randomsample(200)

# and a graphskeleton
skel = GraphSkeleton()
skel.load("../tests/unittestdict.txt")

# instantiate my learner 
learner = PGMLearner()

# estimate parameters
result = learner.discrete_mle_estimateparams(skel, data)

# output - toggle comment to see
#print json.dumps(result.Vdata, indent=2)

# (9) -------------------------------------------------------------------------
# Learn the structure of a discrete Bayesian network, given only data:

# say I have some data
data = bn.randomsample(2000)

# instantiate my learner 
learner = PGMLearner()

# estimate parameters
result = learner.discrete_constraint_estimatestruct(data)

# output - toggle comment to see
#print json.dumps(result.E, indent=2)

# (10) -----------------------------------------------------------------------
# Learn the structure of a linear Gaussian Bayesian network, given data and a 
# structure

# say I have some data
data = lgbn.randomsample(200)

# and a graphskeleton
skel = GraphSkeleton()
skel.load("../tests/unittestdict.txt")

# instantiate my learner 
learner = PGMLearner()

# estimate parameters
result = learner.lg_mle_estimateparams(skel, data)

# output - toggle comment to see
#print json.dumps(result.Vdata, indent=2)

# (11) ----------------------------------------------------------------------
# Learn a structure of a linear Gaussian Bayesian network, given only data

# say I have some data
data = lgbn.randomsample(8000)

# instantiate my learner 
learner = PGMLearner()

# estimate parameters
result = learner.lg_constraint_estimatestruct(data)

# output - toggle comment to see
#print json.dumps(result.E, indent=2)

# (12) -----------------------------------------------------------------------
# Learn entire Bayesian networks

# say I have some data
data = lgbn.randomsample(8000)

# instantiate my learner 
learner = PGMLearner()

# estimate parameters
result = learner.lg_estimatebn(data)

# output - toggle comment to see
#print json.dumps(result.E, indent=2)
#print json.dumps(result.Vdata, indent=2)

# say I have some data
data = bn.randomsample(2000)

# instantiate my learner 
learner = PGMLearner()

# estimate parameters
result = learner.discrete_estimatebn(data)

# output - toggle comment to see
#print json.dumps(result.E, indent=2)
#print json.dumps(result.Vdata, indent=2)

# (13) -----------------------------------------------------------------------
# Forward sample on dynamic Bayesian networks

# read input file
path = "../tests/unittestdyndict.txt"
f = open(path, 'r')
g = eval(f.read())

# set up dynamic BN
d = DynDiscBayesianNetwork()
skel = GraphSkeleton()
skel.V = g["V"]
skel.E = g["E"]
skel.toporder()
d.V = skel.V
d.E = skel.E
d.initial_Vdata = g["initial_Vdata"]
d.twotbn_Vdata = g["twotbn_Vdata"]

# forward sample
seq = d.randomsample(10)

# output - toggle comment to see
#print json.dumps(seq, indent=2)
