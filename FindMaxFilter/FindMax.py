#
# find max and min values in a tab-separated stream
#
# author: Peter Mackenzie-Helnwein
#
# date: Oct 22, 2018
#

import sys

maxlist = []
minlist = []
nvals = 0

linecount = 0

for line in sys.stdin:
    vals = [ float(x.strip()) for x in line.split('\t')]
    if linecount:
        for i in range(nvals):
            if (vals[i] > maxlist[i]):
                maxlist[i] = vals[i]
            if (vals[i] < minlist[i]):
                minlist[i] = vals[i]
    else:
        # this is the first line
        maxlist = vals[:]
        minlist = vals[:]
        nvals = len(vals)
    linecount += 1

print('{} columns found:'.format{nvals})
for i in range(nvals):
    print('col {}: min={}   max={}'.format(i, minlist[i], maxlist[i]))
    


