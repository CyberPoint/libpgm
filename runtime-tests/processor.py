'''
Processes trials and outputs to a file.

Charlie Cabot
August 1, 2012

'''

from bn_generator import disc_bn_generator
from timer import timer

r = range(500, 5000)[::500]

op = open("output.csv", 'w')
print >>op, "Discrete bn parameter learning. Runtime as a function of datapoints. numvertices=300. numoutcomes=2. indegree=2. max witness size=1."

for dl in r:
    disc_bn_generator(300, 2, 2, "disc_bn_x.txt")
    runtime = timer("disc_bn_x.txt", 1, dl)
    line = "%d, %f" % (dl, runtime)
    print line
    print >>op, line 



