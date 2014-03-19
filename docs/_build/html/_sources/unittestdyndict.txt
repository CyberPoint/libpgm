dynamic discrete bayesian network
=================================

This is an example input file for a dynamic Bayesian network with discete CPDs, i.e., a Bayesian network that changes over time wherein the Bayesian network at each time interval is influenced by the outcomes of the Bayesian network in the previous time interval. It is represented by a set of initial CPD data, ``initial_Vdata``, and dynamic CPD data, ``twotbn_Vdata``. See Koller et al. 204 for more on 2-TBN dynamic Bayesian networks. This example provides dynamic CPD data for the same graph skeleton as in the :doc:`discrete case <unittestdict>`::

    {	
        "V": ["Letter", "Grade", "Intelligence", "SAT", "Difficulty"],
        "E": [["Intelligence", "Grade"],
            ["Difficulty", "Grade"],
            ["Intelligence", "SAT"],
            ["Grade", "Letter"]],
        "initial_Vdata": {
            "Letter": {
                "ord": 4,
                "numoutcomes": 2,
                "vals": ["weak", "strong"],
                "parents": ["Grade"],
                "children": None,
                "cprob": {
                    "['A']": [.1, .9],
                    "['B']": [.4, .6],
                    "['C']": [.99, .01]
                }
            },
            
            "SAT": {
                "ord": 3,
                "numoutcomes": 2,
                "vals": ["lowscore", "highscore"],
                "parents": ["Intelligence"],
                "children": None,
                "cprob": {
                    "['low']": [.95, .05],
                    "['high']": [.2, .8]
                }
            },
            
            "Grade": {
                "ord": 2,
                "numoutcomes": 3,
                "vals": ["A", "B", "C"],
                "parents": ["Difficulty", "Intelligence"],
                "children": ["Letter"],
                "cprob": {
                    "['easy', 'low']": [.3, .4, .3],
                    "['easy', 'high']": [.9, .08, .02],
                    "['hard', 'low']": [.05, .25, .7],
                    "['hard', 'high']": [.5, .3, .2]
                }
            },
            
            "Intelligence": {
                "ord": 1,
                "numoutcomes": 2,
                "vals": ["low", "high"],
                "parents": None,
                "children": ["SAT", "Grade"],
                "cprob": [.7, .3]
            },
            
            "Difficulty": {
                "ord": 0,
                "numoutcomes": 2,
                "vals": ["easy", "hard"],
                "parents": None,
                "children": ["Grade"],
                "cprob":  [.6, .4]
            }
        },
        "twotbn_Vdata": {
            "Letter": {
                "ord": 4,
                "numoutcomes": 2,
                "vals": ["weak", "strong"],
                "parents": ["past_Grade", "past_Letter", "Grade"],
                "children": None,
                "cprob": {
                    "['A', 'weak', 'A']": [.1, .9],
                    "['A', 'weak', 'B']": [.15, .85],
                    "['A', 'weak', 'C']": [.05, .95],
                    "['A', 'strong', 'A']": [.1, .9],
                    "['A', 'strong', 'B']": [.1, .9],
                    "['A', 'strong', 'C']": [.1, .9],
                    "['B', 'weak', 'A']": [.47, .53],
                    "['B', 'weak', 'B']": [.4, .6],
                    "['B', 'weak', 'C']": [.4, .6],
                    "['B', 'strong', 'A']": [.4, .6],
                    "['B', 'strong', 'B']": [.41, .59],
                    "['B', 'strong', 'C']": [.42, .58],
                    "['C', 'weak', 'A']": [.99, .01],
                    "['C', 'weak', 'B']": [.99, .01],
                    "['C', 'weak', 'C']": [.99, .01],
                    "['C', 'strong', 'A']": [.99, .01],
                    "['C', 'strong', 'B']": [.99, .01],
                    "['C', 'strong', 'C']": [.99, .01]
                }
            },
            
            "SAT": {
                "ord": 3,
                "numoutcomes": 2,
                "vals": ["lowscore", "highscore"],
                "parents": ["Intelligence"],
                "children": None,
                "cprob": {
                    "['low']": [.95, .05],
                    "['high']": [.2, .8]
                }
            },
            
            "Grade": {
                "ord": 2,
                "numoutcomes": 3,
                "vals": ["A", "B", "C"],
                "parents": ["Difficulty", "Intelligence"],
                "children": ["Letter"],
                "cprob": {
                    "['easy', 'low']": [.3, .4, .3],
                    "['easy', 'high']": [.9, .08, .02],
                    "['hard', 'low']": [.05, .25, .7],
                    "['hard', 'high']": [.5, .3, .2]
                }
            },
            
            "Intelligence": {
                "ord": 1,
                "numoutcomes": 2,
                "vals": ["low", "high"],
                "parents": ["past_Intelligence"],
                "children": ["SAT", "Grade"],
                "cprob": {
                    "['high']": [.7, .3],
                    "['low']": [.7, .3]
                }
            },
            
            "Difficulty": {
                "ord": 0,
                "numoutcomes": 2,
                "vals": ["easy", "hard"],
                "parents": ["past_Difficulty"],
                "children": ["Grade"],
                "cprob": {
                    "['easy']": [.9, .1],
                    "['hard']": [.1, .9]
                }
            }
        }
    }
