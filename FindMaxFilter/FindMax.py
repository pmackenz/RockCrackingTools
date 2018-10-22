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
    svals = [ x.strip() for x in line.split('\t')]
    if linecount:
        if ( len(svals) != nvals ):
            print('line:', line)
            print(svals)
            raise ValueError
        vals = [ float(x) for x in svals ]
        for i in range(nvals):
            if (vals[i] > maxlist[i]):
                maxlist[i] = vals[i]
            if (vals[i] < minlist[i]):
                minlist[i] = vals[i]
    else:
        # this is the first line
        nvals = len(svals) - 1 # the "- 1" is to fix a bug in our txt files
        maxlist = [ -9999999. for i in range(nvals) ]
        minlist = [ +9999999. for i in range(nvals) ]
    linecount += 1

print('{} columns found:'.format(nvals))
for i in range(nvals):
    print('col {}: min={}   max={}'.format(i+1, minlist[i], maxlist[i]))
    


