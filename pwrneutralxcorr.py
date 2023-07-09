#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy

# create sequence

numpy.random.seed(42)

seqlen = 64
seq = numpy.random.randint(0,2, seqlen)*2-1 #bipolar
#seq = numpy.random.randn(seqlen) #random


x = numpy.zeros(5*seqlen)

# insert seq into x in 3 different spots with different magnitudes
for i,m in ((0,1), (int(1.5*seqlen), 0.1), (int(3*seqlen), 5.),):
    x[i:i+seq.size] = seq * m

x += numpy.random.randn(x.size) * 0.05 #noise on x



import matplotlib.pyplot as plt

plt.figure(1)
plt.clf()
plt.plot(x, c='b')
plt.gca().set_ylabel("signal", color="blue",fontsize=14)

#correlation and mag correlation
xc = numpy.correlate(x, seq)
mxc = numpy.correlate(numpy.abs(x), numpy.abs(seq))

pwrneutralxc = xc / mxc # better to check for 0/0 here!

def partial_pwr_neutral_xcorr(sig, seq, nparts = 2):
    seq = numpy.asarray(seq)
    beg, n = 0, seq.size // nparts
    parts = []
    
    for i in range(nparts):
        part = seq.copy()
        part[:beg] = 0
        if i + 1 < nparts:
            part[beg+n:] = 0
        
        xc = numpy.correlate(x, part)
        mxc = numpy.correlate(numpy.abs(x), numpy.abs(part))
        
        parts.append(xc / mxc)
    
    return numpy.array(parts)

part_xcs = partial_pwr_neutral_xcorr(x, seq)

ax2 = plt.gca().twinx()
ax2.plot(pwrneutralxc, c='r')
ax2.plot(numpy.mean(part_xcs, axis=0), c='g', label='mean')
ax2.plot(numpy.min(part_xcs, axis=0), c='c', label='min')
ax2.plot(numpy.prod(part_xcs, axis=0), c='y', label='prod')
ax2.set_ylabel("Xcorr / Xcorr(abs)",color="red",fontsize=14)

plt.legend()


plt.show()