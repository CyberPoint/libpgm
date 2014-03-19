libpgm is a set of tools to use probabilistic graphical models to compute
probabilities in multivariate systems. 

To install in your default location for third-party packages, run: 

    [sudo] python setup.py install


Included in this package are:

1. Python modules containing PGM tools (libpgm/)
    dictionary.py
    discretebayesiannetwork.py
    graphskeleton.py
    hybayesiannetwork.py
    lhbayesiannetwork.py
    nodedata.py
    orderedskeleton.py
    pgmlearner.py
    sampleaggregator.py
    tablecpdfactorization.py
    tablecpdfactor.py
    /CPDtypes/discrete.py
    /CPDtypes/crazy.py
    /CPDtypes/lgandd.py
    /CPDtypes/lg.py
2. Unit tests and unit test dictionaries to test functionality (tests/)
    run_unit_tests.py
    unittestdict.txt
    unittestlgdict.txt
    unittesthdict.txt
    unittestdyndict.txt
3. Examples of how to use tools (/examples)
    examples.py
    exampleevidence.txt
    examplequery.txt
    exampledata.txt
4. Documentation (/docs/_build/_html)
    index.html (has links to all documentation pages)

To use this library, one must create an input file or input files for their Bayesian network --
for examples of this, see the unit test dictionaries: 
    unittestdict.txt   -- A sample input file for a discrete-CPD Bayesian
                          network  
    unittestlgdict.txt -- A sample input file for a linear Gaussian-CPD Bayesian
                          network
    unittesthdict.txt  -- A sample input file for a hybrid (any type) CPD
                          Bayesian network
    unittestdyndict.txt -- A sample input file for a dynamic discrete Bayesian
                           network
Once the input file is created, this library allows for the user to execute a 
number of queries and commands. These are listed below, each with a brief
example, a reference to Probabilistic Graphical Models by Koller and Friedman,
and a reference to an example in examples.py.

SAMPLING CAPABILITIES
    1. Generate a sequence of samples from a discrete-CPD Bayesian network:
        Load a "NodeData" instance and a "GraphSkeleton" instance from input
        files. Run the "toporder" method on the GraphSkeleton instance to
        topologically order the graph. Load a "DiscreteBayesianNetwork" instance 
        from the skeleton and node data. Run the "randomsample" method on the 
        DiscreteBayesianNetwork instance to return a sequence of samples.
            Koller reference -- 12.1
            Examples reference -- (1)
    2. Generate a sequence of samples from a linear Gaussian-CPD Bayesian network:
        Same as previous, but use "LGBayesianNetwork" instead of
        "DiscreteBayesianNetwork".
            Koller reference -- 12.1
            Examples reference -- (2)
    3. Generate a sequence of samples from a hybrid (any CPD type) Bayesian network:
        For all of the CPD types, create a module, class, and "choose" method of the
        type found in /CPDtypes/. This method must take in a list of parent outcomes
        and return a properly sampled value for its node. Once this method is
        written, load a "NodeData" instance and a "GraphSkeleton" instance from the input
        file (and run "toporder" on the GraphSkeleton instance). Then run the 
        "entriestoinstances" method on the NodeData instance. Then load a 
        "HyBayesianNetwork" instance from the skeleton and node data.  Then run
        the "randomsample" method on the HyBayesianNetwork instance to
        return a sequence of samples.
            Koller reference -- 14.5.2
            Examples reference -- (3)
    4. Generate a sequence of samples from a discrete-CPD Bayesian network, given evidence:
        Set up the Bayesian network as in (1). Place evidence in a .txt file in
        the format found in exampleevidence.txt. Load a "TableCPDFactorization"
        instance from the DiscreteBayesianNetwork instance. Run the "gibbssample" method
        on the TableCPDFactorization instance which returns a sequence. These
        samples provably get closer to the posterior probability distribution
        (the probability distribution given evidence) over time.
            Koller reference -- 12.3.1
            Examples reference -- (4)

DETERMINISTIC INFERENCE CAPABILITIES (all for discrete-CPD Bayesian networks)
    5. Compute the probability distribution over a specific node or nodes:
        Set up a DiscreteBayesianNetwork instance as in (1). Load a
        TableCPDFactorization instance from the DiscreteBayesianNetwork instance.
        If you have evidence, place it in a dictionary in the style of
        exampleevidence.txt. Place your query in a dictionary in the style of
        examplequery.txt. Load both evidence and query into python dicts. Run
        the "condprobve" method on the TableCPDFactorization instance, with 
        query and evidence dicts as arguments. This will return a factor (an
        alternative form of a probability distribution -- see Koller 104) with 
        the probability distribution over the variables you queried about (it 
        will ignore the outcomes included in your query).
            Koller reference -- 9.3
            Examples reference -- (5)
    6. Compute the exact probability of an outcome:
        Set up a TableCPDFactorization instance, a query dict, and an
        evidence dict in the manner specified by (5). Then run the
        "specificquery" method on the TableCPDFactorization instance with query
        and evidence as arguments. This will return the specific probability
        that the outcomes specified by query will occur given the evidence
        presented.
            Koller reference -- 9.3
            Examples reference -- (6)

APPROXIMATIVE INFERENCE CAPABILITIES
    7. Compute the approximate probability distribution by generating samples:
        Create an SampleAggregator instance. Instantiate a type of Bayesian
        network class that you want to sample. Then run the "aggregate" method
        with a sampling function statement as its argument (e.g.,
        instance.randomsample(100)). This will return the "average" of all
        samples generated, which is an approximate probability distribution.
            Koller reference -- 12.1
            Examples reference -- (7)

BAYESIAN NETWORK LEARNING CAPABILITIES
    8. Learn the CPDs of a discrete Bayesian network, given data and a structure:
        Load a GraphSkeleton instance from an inputfile that holds your graph structure. 
        Transform your data into an inputfile of the format found in
        exampledata.txt. Then load a python dict from that input file
        (using the eval function, or something else). Then create a
        "PGMLearner" instance. Run the "discrete_mle_estimateparams" method with
        the dict of data and the GraphSkeleton instance as arguments. This will return 
        a DiscreteBayesianNetwork instance with the CPDs filled out.
            Koller reference -- 17.2.3
            Examples reference -- (8)
    9. Learn the structure of a discrete Bayesian network, given only data:
        Load the data into a dict in the manner specified in (8). Load a
        PGMLearner instance. Run the "discrete_constraint_estimatestruct" method
        with the data as an argument (p-value threshhold and graph indegree
        constraint are optional arguments as well). This will return a
        GraphSkeleton instance learned from the data.
            Koller reference -- 18.2
            Examples reference -- (9)
    10. Learn the CPDs of a linear Gaussian Bayesian network, given data and a structure:
        Same as (8), but run the "lg_mle_estimateparams" method.
            Koller reference -- 17.2.4
            Examples reference -- (10)
    11. Learn the structure of a linear Gaussian Bayesian network, given only data:
        Same as (9), but run the "lg_constraint_estimatestruct". An additional
        optional argument is the number of bins to use to discretize the continuous
        data.
            Koller reference -- 18.2
            Examples reference -- (11)
    12. Learn entire Bayesian networks (structures and parameters) from data:
        Load the data and the PGMLearner instance as described in (8). Run
        either "discrete_estimatebn" or "lg_estimatebn" depending on whether
        your data is discrete or linear Gaussian. These methods simply combine
        the functions above. They take all the optional arguments.
            Koller reference -- 16-18
            Examples reference -- (12)

DYNAMIC SAMPLING CAPABILITIES
    13. Generate a sequence of samples over time from a dynamic discrete Bayesian network:
        Load a "NodeData" and "GraphSkeleton" instance from proper input files. Run the
        "toporder" method to topologically order the graph skeleton. Instantiate a 
        "DynDiscBayesianNetwork" instance from the NodeData and Graph Skeleton. Run the 
        method "randomsample" on the DynDiscBayesianNetwok to generate a sequence of samples,
        one per time interval, with each influenced by the outcomes of its predecessor.
            Koller reference -- 6.2
            Examples reference -- (13)


--
CyberPoint International 2012
Created by Charlie Cabot
