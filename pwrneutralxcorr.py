#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy

# create sequence

numpy.random.seed(42)

def cr_cazac(n, M = 1):
    n = int(n)
    assert n > 0
    k = numpy.arange(n)
    if n % 2 == 0:
        return numpy.exp(1j * M * numpy.pi * k*k / n)
    #else
    return numpy.exp(1j * M * numpy.pi * k*(k+1) / n)

seqlen = 65
seq = numpy.random.randint(0,2, seqlen)*2. - 1. #bipolar
#seq = numpy.random.randn(seqlen) #random
seq = cr_cazac(seqlen)


x = numpy.zeros(int(5.5*seqlen), dtype=seq.dtype)

# insert seq into x in 3 different spots with different magnitudes
for i,m in ((0,1), (int(1.5*seqlen), 0.1), (int(3*seqlen), 5.),):
    x[i:i+seq.size] = seq * m

x += (numpy.random.randn(x.size) + 1j * numpy.random.randn(x.size)) / numpy.sqrt(2) * 0.025 #noise on x



import matplotlib.pyplot as plt

plt.clf()
plt.plot(numpy.abs(x), c='b')
plt.gca().set_ylabel("signal", color="blue",fontsize=14)

#correlation and mag correlation
xc = numpy.correlate(x, seq)
mxc = numpy.correlate(numpy.abs(x), numpy.abs(seq))

pwrneutralxc = numpy.abs(xc / mxc) # better to check for 0/0 here!

def partial_pwr_neutral_xcorr(sig, seq, nparts = 2):
    seq = numpy.asarray(seq)
    beg, n = 0, seq.size // nparts
    parts = []
    
    for i in range(nparts):
        part = seq.copy()
        part[:beg] = 0
        if i + 1 < nparts:
            part[beg+n:] = 0
        beg += n
        
        xc = numpy.correlate(x, part)
        mxc = numpy.correlate(numpy.abs(x), numpy.abs(part))
        
        parts.append(xc / mxc)
    
    return numpy.array(parts)

part_xcs = numpy.abs(partial_pwr_neutral_xcorr(x, seq))

ax2 = plt.gca().twinx()
ax2.plot(pwrneutralxc, c='r')
ax2.plot(numpy.mean(part_xcs, axis=0), c='g', label='mean')
ax2.plot(numpy.min(part_xcs, axis=0), c='c', label='min')
ax2.plot(numpy.prod(part_xcs, axis=0), c='y', label='prod')
ax2.set_ylabel("Xcorr / Xcorr(abs)",color="red",fontsize=14)

plt.legend()


plt.show()