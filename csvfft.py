#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from ast import parse
import csv
import numpy as np
import scipy as sp

parser = argparse.ArgumentParser()
parser.add_argument( '--input', required=True )  # input file name
parser.add_argument( '--period', required=True, type=float )  # period
parser.add_argument( '--window', default=None )  # window
parser.add_argument( '--delimiter', choices=['comma', 'tab', 'space'], default='comma' )  # delimiter
#parser.add_argument( '-n', default='' )  # newline character
parser.add_argument( '--figure', action='store_true' )  # show figure
parser.add_argument( '--column', default=1, type=int )  # column number where signal stored
parser.add_argument( '--name', action='store_true' )  # item name
parser.add_argument( '--output', default=None )  # output file name
parser.add_argument( '--overlap', type=int )

try:
    args = parser.parse_args()
except:
    exit()

with open( args.input, 'r' ) as f:
    if args.delimiter == 'comma':
        reader = csv.reader( f, delimiter=',' )
    elif args.delimiter == 'tab':
        reader = csv.reader( f, delimiter='\t' )
    elif args.delimiter == 'space':
        reader = csv.reader( f, delimiter=' ' )

    xs = [row for row in reader]
    
    if args.column == 1 and len(xs[-1]) >= 2:
        print( '* Warning: ', args.input, ' has ', len(xs[-1]), ' columns. *' )

    if args.name:
        xs = [float(x[args.column-1]) for x in xs[1:]]
    else:
        xs = [float(x[args.column-1]) for x in xs]

    

freqs = sp.fft.fftfreq( len(xs), args.period )

if args.window is None:
    pass
else:
    pass

xfs = sp.fft.fft( xs )
# Python:ScipyのFFT（scipy.fftpack）をやってみる。 - がれすたさんのDIY日記
# ガレスタさん
# https://gsmcustomeffects.hatenablog.com/entry/2018/08/10/011034
amplitudes = [np.sqrt( xf.real**2 + xf.imag**2 ) for xf in xfs]

if args.output is None:
    output_file_name = 'fft_result.csv'
else:
    output_file_name = args.output

with open( output_file_name, 'w' ) as f:
    f.write( 'frequency,amplitude\n' )
    for freq, amp in zip(freqs, amplitudes):
        f.write( str(freq) + ',' + str(amp) + '\n' )

if args.figure:
    from matplotlib import pyplot as plt
    plt.plot( freqs, amplitudes )
    plt.show()