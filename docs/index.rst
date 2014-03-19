.. libpgm documentation master file, created by
   sphinx-quickstart on Tue Aug  7 11:49:49 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to libpgm!
==================

libpgm is an endeavor to make Bayesian probability graphs easy to use. The effort originates from Daphne Koller and Nir Friedman's *Probabilistic Graphical Models* (2009), which provides an in-depth study of probabilistic graphical models and their applications. 

Install from pypi at `http://pypi.python.org/pypi/libpgm <http://pypi.python.org/pypi/libpgm>`_ or download a tarball `here <TODO>`_.

Documentation
-------------

The library consists of a series of importable modules, which either represent types of Bayesian graphs, contain methods to operate on them, or both. The methods' individual documentation pages are found below:

.. toctree::

   dictionary
   graphskeleton
   orderedskeleton
   nodedata
   discretebayesiannetwork
   hybayesiannetwork
   lgbayesiannetwork
   dyndiscbayesiannetwork
   tablecpdfactorization
   tablecpdfactor
   sampleaggregator
   pgmlearner
   CPDtypes


Note that `numpy <http://www.numpy.scipy.org>`_, `scipy <http://www.scipy.org>`_, and Python 2.7 are required for this library.

Capabilities
------------

Briefly, the capabilities of this library are:

    - Sampling
        - Forward sampling in a discrete-CPD Bayesian network
        - Forward sampling in a linear Gaussian-CPD Bayesian network
        - Forward sampling in a hybrid (any CPD type) Bayesian network
        - Forward sampling in a dynamic 2-TBN Bayesian network
        - Gibbs sampling in a discrete-CPD Bayesian network (given evidence)
    - Deterministic Inference
        - Compute the probability distribution over a specific node or nodes in a discrete-CPD Bayesian network (given evidence, if present) 
        - Compute the exact probability of an outcome in a discrete-CPD Bayesian network (given evidence, if present)
    - Approximative Inference
        - Compute the approximate probability distribution by generating samples
    - Learning
        - Learn the CPDs of a discrete-CPD Bayesian network, given data and a structure
        - Learn the structure of a discrete Bayesian network, given only data
        - Learn the CPDs of a linear Gaussian Bayesian network, given data and a structure
        - Learn the strcutre of a linear Gaussian Bayesian network, given only data
        - Learn entire Bayesian networks (structures and parameters) from data

Input files
-----------

Because Bayesian probability graphs are large and contain a lot of data, the library works with .txt files as inputs. The formatting used is JavaScript Object Notation (JSON), with some flexibility (the :doc:`dictionary` module has the capacity to transform python-style dicts to JSON, for instance). Internally, the library stores these files as *json* objects from python's `json <http://docs.python.org/library/json.html>`_ library. For examples of the formatting, and of the particular data required for each different Bayesian network type, see the example input files below:

.. toctree::

   unittestdict
   unittestlgdict
   unittesthdict
   unittestdyndict


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

