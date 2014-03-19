'''
Processes trials and outputs to a file.

Charlie Cabot
August 1, 2012

'''

from bn_generator import disc_bn_generator
from timer import timer

graphsizes = range(100, 10000)[::100]

op = open("output.csv", 'w')
print >>op, "Forward Sampling in a discrete BN. Runtime as a function of number of vertices. Indegree=3. Numoutcomes=3. Samples=100."

for size in graphsizes:
    disc_bn_generator(size, 3, 3, "disc_bn_x.txt")
    runtime = timer("disc_bn_x.txt", 1)
    line = "%d, %f" % (size, runtime)
    print line
    print >>op, line 



