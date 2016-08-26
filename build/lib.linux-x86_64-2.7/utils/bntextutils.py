
'''
Copyright CyberPoint International LLC
All rights reserved

C. Cabot
09-19-13

Functions to construct/modify a json-style txt file to be 
used as a discrete Bayesian network in libpgm.

'''

import json
import sys

def list_edges(path): 
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        for e in j["E"]: 
            print "%s --> %s" % (e[0], e[1])

def list_nodes(path): 
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        for v in j["V"]: 
            print "%s" % (v)

def list_nodedata(path): 
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        for v in j["Vdata"].keys(): 
            print "%s" % (v)

def add_edge(path, edge): 
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        assert edge[0] in j["V"] and edge[1] in j["V"], "bad edge"
        if edge not in j["E"]:
            j["E"].append(edge)
    with open(path, "w") as f:
        json.dump(j, f, indent=2) 

def remove_edge(path, edge): 
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        assert edge in j["E"], "edge not present"
        j["E"].remove(edge)
    with open(path, "w") as f:
        json.dump(j, f, indent=2) 

def add_node(path, node):
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        if node not in j["V"]:
            j["V"].append(node)
    with open(path, "w") as f:
        json.dump(j, f, indent=2)

def remove_node(path, node):
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        assert node in j["V"], "node not present"
        j["V"].remove(node)
        # delete associated Vdata and edges
        if node in j["Vdata"]:
            del j["Vdata"][node]
        for edge in j["E"]:
            if edge[0] == node or edge[1] == node:
                edges.remove(edge)
    with open(path, "w") as f:
        json.dump(j, f, indent=2)

def alter_vdata(path, node):
    _validate(path)
    with open(path, "r") as f:
        j = json.load(f)
        assert node in j["V"], "node not present"
        print "Current node data: "
        print "------------------ "
        try:
            print json.dumps(j["Vdata"][node], indent=2)
        except KeyError: 
            print "[uninitialized! you may create this node data]"
        print "enter new node data: "
        while (1):
            try:
                minij = json.load(sys.stdin)
                break
            except:
                print("malformatted json, try again:")
        j["Vdata"][node] = minij
    with open(path, "w") as f:
        json.dump(j, f, indent=2)

def refresh(path):
    """updates ord, numoutcomes, parents, and children in vdata"""
    with open(path, "r") as f:
        d = json.load(f)

        # topologically order vertices
        Ecopy = [x[:] for x in d["E"]]
        roots = []  
        toporder = []
          
        for vertex in d["V"]:
            # find roots
            roots = d["V"][:]
            for e in Ecopy: 
                try:
                    roots.remove(e[1])
                except:
                    pass
           
        while roots != []: 
            n = roots.pop()
            toporder.append(n)
            for edge in reversed(Ecopy):
                if edge[0] == n:
                    m = edge[1]
                    Ecopy.remove(edge)
                    yesparent = False 
                    for e in Ecopy:
                        if e[1] == m:
                            yesparent = True
                            break
                    if yesparent == False:
                        roots.append(m)
        assert (not Ecopy), ("Graph contains a cycle", Ecopy)
        d["V"] = toporder 

        # clear attributes
        for entry in d["Vdata"]: 
            d["Vdata"][entry]["parents"] = None
            d["Vdata"][entry]["children"] = None
            d["Vdata"][entry]["numoutcomes"] = len(d["Vdata"][entry]["vals"])
            d["Vdata"][entry]["ord"] = d["V"].index(entry)

        # make parents and children
        for edge in d["E"]:
            parent = edge[0]
            child = edge[1] 

            if d["Vdata"][child]["parents"] == None:
                d["Vdata"][child]["parents"] = [] 
            if parent not in d["Vdata"][child]["parents"]:
                d["Vdata"][child]["parents"].append(parent)

            if d["Vdata"][parent]["children"] == None:
                d["Vdata"][parent]["children"] = [] 
            if child not in d["Vdata"][parent]["children"]:
                d["Vdata"][parent]["children"].append(child)

    with open(path, "w") as f:
        json.dump(d, f, indent=2)

def _validate(path): 
    # is json correctly formatted?
    try:
        with open(path) as f:
            json.load(f)
    except:
        raise Exception("The network file you are trying to modify is invalid")

    # do the nodes match the node data?
    with open(path) as f:
        j = json.load(f)
        if not (sorted(j["V"]) == sorted(j["Vdata"].keys())): 
            print "warning: nodes and node data do not match" 

        # are the edges valid? 
        for e in j["E"]:
            if (e[0] not in j["V"]) or (e[1] not in j["V"]):
                print "warning: nodes not found for this edge:",
                print e

