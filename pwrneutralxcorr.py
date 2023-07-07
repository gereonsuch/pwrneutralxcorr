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

plt.plot(x, c='b')
plt.gca().set_ylabel("signal", color="blue",fontsize=14)

#correlation and mag correlation
xc = numpy.correlate(x, seq)
mxc = numpy.correlate(numpy.abs(x), numpy.abs(seq))

pwrneutralxc = xc / mxc # better to check for 0/0 here!

ax2 = plt.gca().twinx()
ax2.plot(pwrneutralxc, c='r')
ax2.set_ylabel("Xcorr / Xcorr(abs)",color="red",fontsize=14)


plt.show()