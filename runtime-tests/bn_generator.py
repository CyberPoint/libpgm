'''
For creating Bayesian network input files

Charlie Cabot 
August 1, 2012

'''
import json

def disc_bn_generator(numvertices, numoutcomes, indegree, outputpath):
    '''
    Creates a graph with a specified number of vertices, where all vertices 
    except the roots have a specified number of parents and a 
    specified number of children.

    Arguments:
        numvertices -- Number of desired vertices
        indegree -- Number of parents for all vertices except the roots
        outputpath -- Path to created .txt file

    Format is as corresponds to the PGMlibrary discrete-CPD Vdata format.
    See PGMlibrary/discretebayesiannetwork.py

    '''
    import random

    op = open(outputpath, 'w')

    # lay out result
    result = dict()
    result["V"] = []
    result["E"] = []
    result["Vdata"] = dict()

    # make vertices
    for x in range(numvertices):
        result["V"].append(str(x))
        result["Vdata"][str(x)] = dict() 
        result["Vdata"][str(x)]["vals"] = []
        result["Vdata"][str(x)]["parents"] = []
        result["Vdata"][str(x)]["children"] = []
        result["Vdata"][str(x)]["cprob"] = dict()
        
        for y in range(numoutcomes):
            result["Vdata"][str(x)]["vals"].append(str(y))
        result["Vdata"][str(x)]["numoutcomes"] = len(result["Vdata"][str(x)]["vals"])

    # make edges 
    for x in range(numvertices):
        for j in range(indegree):
            if x + j + 1 < numvertices:
                result["E"].append([str(x), str(x + j + 1)])
                result["Vdata"][str(x)]["children"].append(str(x + j + 1))
                result["Vdata"][str(x + j + 1)]["parents"].append(str(x))

    # make cprob recursively
    
    # define helper procedures
    def createinterval(n):
        '''divide [0, 1] into n slices"'''
        ret = []
        nret = []
        for i in range(n):
            nret.append(random.random())
        s = sum(nret)
        ret = [x/float(s) for x in nret]
        return ret

    def explore(x, _dict, key, depth, totaldepth):
        '''recursively fill a cprob table'''
        if depth < totaldepth:
            for val in result["Vdata"][result["Vdata"][x]["parents"][depth]]["vals"]:
                ckey = key[:]
                ckey.append(val)
                explore(x, _dict, ckey, depth + 1, totaldepth)
        else:
            _dict[str(key)] = createinterval(result["Vdata"][x]["numoutcomes"])

    for x in range(numvertices):
        if result["Vdata"][str(x)]["parents"]:
            explore(str(x), result["Vdata"][str(x)]["cprob"], [], 0, len(result["Vdata"][str(x)]["parents"]))
        else:
            result["Vdata"][str(x)]["cprob"] = createinterval(result["Vdata"][str(x)]["numoutcomes"])

    print >>op, json.dumps(result)
