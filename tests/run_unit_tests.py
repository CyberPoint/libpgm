'''
A module that conducts unit tests on all top-level methods within each class.

Created on Jun 20, 2012
@author: ccabot

'''
import unittest
import sys

# add to PYTHONPATH
sys.path.append("../")

from libpgm.dictionary import Dictionary
from libpgm.graphskeleton import GraphSkeleton
from libpgm.orderedskeleton import OrderedSkeleton
from libpgm.discretebayesiannetwork import DiscreteBayesianNetwork
from libpgm.hybayesiannetwork import HyBayesianNetwork
from libpgm.nodedata import NodeData
from libpgm.tablecpdfactor import TableCPDFactor
from libpgm.sampleaggregator import SampleAggregator
from libpgm.tablecpdfactorization import TableCPDFactorization
from libpgm.lgbayesiannetwork import LGBayesianNetwork
from libpgm.dyndiscbayesiannetwork import DynDiscBayesianNetwork
from libpgm.pgmlearner import PGMLearner

class TestNodeData(unittest.TestCase):

    def setUp(self):
        self.nd = NodeData()

    def test_entriestoinstances(self):
        self.nd.load("unittesthdict.txt")
        self.nd.entriestoinstances()
        result = self.nd.nodes["Intelligence"].choose([])
        self.assertTrue(result == 'low' or result == 'high')

class TestGraphSkeleton(unittest.TestCase):

    def setUp(self):
        self.instance = GraphSkeleton()
        self.instance.V = [1,2,3,4,5]
        self.instance.E = [[5,1],[1,2]]
    
    def test_getparents(self):
        self.assertEqual(self.instance.getparents(1), [5])
        self.assertEqual(self.instance.getparents(4), [])
    
    def test_getchildren(self):
        self.assertEqual(self.instance.getchildren(5), [1])
        self.assertEqual(self.instance.getchildren(4), [])
        
    def test_toporder(self):
        self.instance.toporder()
        self.assertTrue(self.instance.V.index(5)<self.instance.V.index(1))
        self.assertTrue(self.instance.V.index(5)<self.instance.V.index(2))

class TestOrderedSkeleton(unittest.TestCase):

    def setUp(self):
        self.os = OrderedSkeleton()
        self.os.load("unittestdict.txt")
        self.gs = GraphSkeleton()
        self.gs.load("unittestdict.txt")

    def test_constructor(self):
        self.assertNotEqual(self.os.V, self.gs.V)
        self.gs.toporder()
        self.assertEqual(self.os.V, self.gs.V)

class TestDiscreteBayesianNetwork(unittest.TestCase):
    
    def setUp(self):
        skel = GraphSkeleton()
        skel.load("unittestdict.txt")
        skel.toporder()
        nodedata = NodeData()
        nodedata.load("unittestdict.txt")
        self.instance = DiscreteBayesianNetwork(skel, nodedata)
        
    def test_randomsample(self):
        randomsample = self.instance.randomsample(5)
        self.assertTrue(randomsample[0]["Difficulty"] == 'easy' or randomsample[0]["Difficulty"] == 'hard')
        for key in randomsample[0].keys():
            self.assertTrue(randomsample[0][key] != "default")
            
    def test_randomsamplewithevidence(self):
    	evidence = dict(Difficulty='easy')
    	randomsample = self.instance.randomsample(10, evidence)
    	for entry in randomsample:
    		self.assertEqual(entry["Difficulty"], 'easy')
        
class TestLGBayesianNetwork(unittest.TestCase):

    def setUp(self):
        nodedata = NodeData()
        nodedata.load("unittestlgdict.txt")
        skel = GraphSkeleton()
        skel.load("unittestdict.txt")
        skel.toporder()

        self.lgb = LGBayesianNetwork(skel, nodedata)
    
    def test_randomsample(self):
        seq = self.lgb.randomsample(1)
        ctr = 0
        for entry in seq[0].keys():
            self.assertTrue(seq[0][entry], float)
            ctr = ctr + 1
        self.assertEqual(ctr, 5)

class TestTableCPDFactor(unittest.TestCase):
    
    def setUp(self):
        skel = GraphSkeleton()
        skel.load("unittestdict.txt")
        skel.toporder()
        nodedata = NodeData()
        nodedata.load("unittestdict.txt")
        self.instance = DiscreteBayesianNetwork(skel, nodedata)
        self.factor = TableCPDFactor("Grade", self.instance)
        self.factor2 = TableCPDFactor("Letter", self.instance)
    
    def test_constructor(self):
        product = 1
        for var in self.factor.card:
            product *= var
        self.assertTrue(len(self.factor.vals) == product)
        for i in range(1, len(self.factor.scope)):
            self.assertTrue(self.factor.stride[self.factor.scope[i]] == self.factor.stride[self.factor.scope[i-1]] * self.factor.card[i-1])
    
    def test_multiplyfactor(self):
        self.factor.multiplyfactor(self.factor2)
        a = [0.03, 0.16000000000000003, 0.297, 0.09000000000000001, 0.032, 0.0198, 0.005000000000000001, 0.1, 0.693, 0.05, 0.12, 0.198, 0.27, 0.24, 0.003, 0.81, 0.048, 0.0002, 0.045000000000000005, 0.15, 0.006999999999999999, 0.45, 0.18, 0.002] 
        b = [3, 2, 2, 2] 
        c = ['Grade', 'Intelligence', 'Difficulty', 'Letter'] 
        d = {'Grade': 1, 'Intelligence': 3, 'Letter': 12, 'Difficulty': 6}
        self.assertEqual(self.factor.vals, a)
        self.assertEqual(self.factor.card, b)
        self.assertEqual(self.factor.scope, c)
        self.assertEqual(self.factor.stride, d)
        
    def test_sumout(self):
        self.factor.sumout("Difficulty")
        a = [0.35, 0.65, 1.0, 1.4, 0.38, 0.22] 
        b = [3, 2] 
        c = ['Grade', 'Intelligence'] 
        d = {'Grade': 1, 'Intelligence': 3}
        self.assertEqual(self.factor.vals, a)
        self.assertEqual(self.factor.card, b)
        self.assertEqual(self.factor.scope, c)
        self.assertEqual(self.factor.stride, d)
        
    def test_reducefactor(self):
        self.factor.reducefactor("Difficulty", 'easy')
        a = [0.3, 0.4, 0.3, 0.9, 0.08, 0.02] 
        b = [3, 2] 
        c = ['Grade', 'Intelligence'] 
        d = {'Grade': 1, 'Intelligence': 3}
        self.assertEqual(self.factor.vals, a)
        self.assertEqual(self.factor.card, b)
        self.assertEqual(self.factor.scope, c)
        self.assertEqual(self.factor.stride, d)
        
    def test_copy(self):
        copy = self.factor.copy()
        self.assertTrue((copy is self.factor) == False)
        self.assertEqual(copy.vals, self.factor.vals)
        self.assertEqual(copy.card, self.factor.card)
        self.assertEqual(copy.scope, self.factor.scope)
        self.assertEqual(copy.stride, self.factor.stride)
        
class TestTableCPDFactorization(unittest.TestCase):
    
    def setUp(self):
        skel = GraphSkeleton()
        skel.load("unittestdict.txt")
        skel.toporder()
        nodedata = NodeData()
        nodedata.load("unittestdict.txt")
        self.bn = DiscreteBayesianNetwork(skel, nodedata)
        self.fn = TableCPDFactorization(self.bn)
    
    def test_constructor(self):
        self.assertTrue(len(self.fn.originalfactorlist) == 5)
        for x in range(5):
            self.assertTrue(isinstance(self.fn.originalfactorlist[x], TableCPDFactor))

    def test_refresh(self):
        evidence = dict(Letter='weak')
        query = dict(Intelligence=['high'])
        result1 = self.fn.specificquery(query, evidence)
        self.fn.refresh() 
        result2 = self.fn.specificquery(query, evidence)
        self.assertEqual(result1, result2) 
                            
    def test_sumproducteliminatevar(self):
        self.fn.refresh()
        self.fn.sumproducteliminatevar("Difficulty")
        yes = 0
        for x in range(len(self.fn.factorlist)):
            if (self.fn.factorlist[x].scope == ['Grade', 'Intelligence']):
                yes += 1 
                index = x
                
        self.assertTrue(yes == 1)
        exp = [0.2, 0.33999999999999997, 0.45999999999999996, 0.74, 0.16799999999999998, 0.09200000000000001]
        for x in range(6):
            self.assertTrue(abs(self.fn.factorlist[index].vals[x] - exp[x]) < .01)

    def test_sumproductve(self):
        input = ["Difficulty", "Grade", "Intelligence", "SAT"]
        self.fn.refresh()
        self.fn.sumproductve(input)
        exp = [.498, .502]
        for x in range(2):
            self.assertTrue(abs(self.fn.factorlist.vals[x] - exp[x]) < .01)
    
    def test_condprobve(self):
        evidence = dict(Grade='C', SAT='highscore')
        query = dict(Intelligence='high')
        self.fn.refresh()
        self.fn.condprobve(query, evidence)
        exp = [.422, .578]
        for x in range(2):
            self.assertTrue(abs(self.fn.factorlist.vals[x] - exp[x]) < .01)
        
    def test_specificquery(self):
        evidence = dict(Difficulty='easy')
        query = dict(Grade=['A', 'B'])
        self.fn.refresh()
        answer = self.fn.specificquery(query, evidence)
        self.assertTrue(abs(answer - .784) < .01)
    
    def test_gibbssample(self):
        evidence = dict(Letter='weak')
        gs = self.fn.gibbssample(evidence, 5)
        self.assertTrue(gs[0]["Difficulty"] == 'easy' or gs[0]["Difficulty"] == 'hard')
        self.assertTrue(len(gs) == 5)
        for entry in gs: 
            self.assertTrue(entry["Letter"] == 'weak')
        
class TestSampleAggregator(unittest.TestCase):
    
    def setUp(self):
        skel = GraphSkeleton()
        skel.load("unittestdict.txt")
        skel.toporder()
        nodedata = NodeData()
        nodedata.load("unittestdict.txt")
        self.bn = DiscreteBayesianNetwork(skel, nodedata)
        agg = SampleAggregator()
        agg.aggregate(self.bn.randomsample(50))
        self.rseq = agg.seq
        self.ravg = agg.avg
        self.fn = TableCPDFactorization(self.bn)
        evidence = dict(Letter='weak')
        agg.aggregate(self.fn.gibbssample(evidence, 51))
        self.gseq = agg.seq
        self.gavg = agg.avg
        
    def test_rseq(self):
        self.assertTrue(len(self.rseq) == 50)
        for key in self.ravg.keys():
            summ = 0 
            for entry in self.ravg[key].keys():
                summ += self.ravg[key][entry]
            self.assertTrue(summ > .99 and summ < 1.01)
            
    def test_gseq(self):
        self.assertTrue(len(self.gseq) == 51)
        for key in self.gavg.keys():
            summ = 0 
            for entry in self.gavg[key].keys():
                summ += self.gavg[key][entry]
            self.assertTrue(summ > .99 and summ < 1.01)
        
class TestHyBayesianNetwork(unittest.TestCase):

    def setUp(self):
        self.nd = NodeData()
        self.nd.load("unittesthdict.txt")
        self.nd.entriestoinstances()
        self.skel = GraphSkeleton()
        self.skel.load("unittestdict.txt")
        self.skel.toporder()
        self.hybn = HyBayesianNetwork(self.skel, self.nd)

    def test_randomsample(self):
        sample = self.hybn.randomsample(1)[0]
        self.assertTrue(isinstance(sample['Grade'], float))
        self.assertTrue(isinstance(sample['Intelligence'], str))
        self.assertEqual(sample["SAT"][-12:], 'blueberries!')

class TestDynDiscBayesianNetwork(unittest.TestCase):

    def setUp(self):
        self.nd = NodeData()
        self.nd.load("unittestdyndict.txt")
        self.skel = GraphSkeleton()
        self.skel.load("unittestdyndict.txt")
        self.skel.toporder()
        self.d = DynDiscBayesianNetwork(self.skel, self.nd)

    def test_randomsample(self):
        sample = self.d.randomsample(10)
        for i in range(1, 10): 
            self.assertEqual(sample[0]['Difficulty'], sample[i]['Difficulty'])


class TestPGMLearner(unittest.TestCase):
    
    def setUp(self):
        # instantiate learner
        self.l = PGMLearner()

        # generate graph skeleton
        skel = GraphSkeleton()
        skel.load("unittestdict.txt")
        skel.toporder()

        # generate sample sequence to try to learn from - discrete
        nd = NodeData()
        nd.load("unittestdict.txt")
        self.samplediscbn = DiscreteBayesianNetwork(skel, nd)
        self.samplediscseq = self.samplediscbn.randomsample(5000)

        # generate sample sequence to try to learn from - discrete
        nda = NodeData()
        nda.load("unittestlgdict.txt")
        self.samplelgbn = LGBayesianNetwork(skel, nda)
        self.samplelgseq = self.samplelgbn.randomsample(10000)

        self.skel = skel

    def test_discrete_mle_estimateparams(self):
        result = self.l.discrete_mle_estimateparams(self.skel, self.samplediscseq)
        indexa = result.Vdata['SAT']['vals'].index('lowscore')
        self.assertTrue(result.Vdata['SAT']['cprob']["['low']"][indexa] < 1 and result.Vdata['SAT']['cprob']["['low']"][indexa] > .9)
        indexb = result.Vdata['Letter']['vals'].index('weak')
        self.assertTrue(result.Vdata['Letter']['cprob']["['A']"][indexb] < .15 and result.Vdata['Letter']['cprob']["['A']"][indexb] > .05)

    def test_lg_mle_estimateparams(self):
        result = self.l.lg_mle_estimateparams(self.skel, self.samplelgseq)
        self.assertTrue(result.Vdata['SAT']['mean_base'] < 15 and result.Vdata['SAT']['mean_base'] > 5)
        self.assertTrue(result.Vdata['Letter']['variance'] < 15 and result.Vdata['Letter']['variance'] > 5)

    def test_discrete_constraint_estimatestruct(self):
        result = self.l.discrete_constraint_estimatestruct(self.samplediscseq)
        self.assertTrue(["Difficulty", "Grade"] in result.E)

    def test_lg_constraint_estimatestruct(self):
        result = self.l.lg_constraint_estimatestruct(self.samplelgseq)
        self.assertTrue(["Intelligence", "Grade"] in result.E)

    def test_discrete_condind(self):
        chi, pv, witness = self.l.discrete_condind(self.samplediscseq, "Difficulty", "Letter", ["Grade"])
        self.assertTrue(pv > .05)
        self.assertTrue(witness, ["Grade"])
        chia, pva, witnessa = self.l.discrete_condind(self.samplediscseq, "Difficulty", "Intelligence", [])  
        self.assertTrue(pva < .05)

    def test_discrete_estimatebn(self):
        result = self.l.discrete_estimatebn(self.samplediscseq)
        self.assertTrue(result.V)
        self.assertTrue(result.E)
        self.assertTrue(result.Vdata["Difficulty"]["cprob"][0])

    def test_lg_estimatebn(self):
        result = self.l.lg_estimatebn(self.samplelgseq)
        self.assertTrue(result.V)
        self.assertTrue(result.E)
        self.assertTrue(result.Vdata["Intelligence"]["mean_base"])
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
