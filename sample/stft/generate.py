#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

FREQ = 50
SAMPLE_FREQ = 1000
N_SAMPLES = 20000

omega = 2.0 * np.pi * FREQ

ts = [1.0/float(SAMPLE_FREQ)*float(i) for i in range(N_SAMPLES)]
xs = [np.sin(omega*t) + 0.1*np.sin(2.0*omega*t) for t in ts[:int(N_SAMPLES/2)]]
xs += [np.sin(omega*t) + 0.1*np.sin(4.0*omega*t) for t in ts[int(N_SAMPLES/2):]]

with open( 'input.csv', 'w' ) as f:
    f.write( 't\tx\n' )
    for t, x in zip(ts, xs):
        f.write( str(t) + '\t' + str(x) + '\n' )