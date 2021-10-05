#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
from ast import parse
import csv
import numpy as np
import scipy as sp
from scipy import signal

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
parser.add_argument( '--overlap', type=int )  # overlap size
parser.add_argument( '--frame', type=int )  # overlapping frame size
parser.add_argument( '--stft', action='store_true' )  # short time fourier transform

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

if args.overlap is None:
    xss = [xs]
    frame = len(xs)
else:
    """
    1,2,3,4,5,6,7,8,9,10
    75%:4,3,7,  10/1=10, if x*(4-3)+4 < N?, x=(10-4)/1=6
        1,2,3,4
        2,3,4,5
        3,4,5,6
        4,5,6,7
        5,6,7,8
        6,7,8,9
        7,8,9,10
    50%:4,2,4, 10/2=5, if x*(4-2)+4 < N?, x=(10-4)/2=3
        1,2,3,4
        3,4,5,6
        5,6,7,8
        7,8,9,10
    25%:4,1,3, 10/3=3, if x*(4-1)+4 < N?, x=(10-4)/3=2
        1,2,3,4
        4,5,6,7
        7,8,9,10
    0%:4,0,2, if x*(4-0)+4 < N?, x=(10-4)/4=1
        1,2,3,4
        5,6,7,8
    """
    """
    If xs = [1,2,3,4,5,6,7,8,9,10], overlap = 2, frame = 4,
    xss = [[1, 2, 3, 4], [3, 4, 5, 6], [5, 6, 7, 8], [7, 8, 9, 10]]
    """
    frame = args.frame
    overlap = args.overlap
    xss = [xs[i*(frame-overlap):i*(frame-overlap)+frame] for i in range( int((len(xs)-frame)/(frame-overlap))+1 )]

freqs = sp.fft.fftfreq( frame, args.period )

if args.window is not None:
    window = signal.get_window( args.window, frame )
    xss = [xs*window for xs in xss]

xfss = [sp.fft.fft(xs) for xs in xss]

if args.stft:  # short time fourier transform
    # extract the former half of list
    freqs = freqs[:int(len(freqs)/2)]
    xfss = [xfs[:int(len(xfs)/2)] for xfs in xfss]

    # Python:ScipyのFFT（scipy.fftpack）をやってみる。 - がれすたさんのDIY日記
    # ガレスタさん
    # https://gsmcustomeffects.hatenablog.com/entry/2018/08/10/011034
    amplitudess = [[np.sqrt( xf.real**2 + xf.imag**2 ) for xf in xfs] for xfs in xfss]

    if args.output is None:
        output_file_name = 'stft_result.csv'
    else:
        output_file_name = args.output

    with open( output_file_name, 'w' ) as f:
        f.write( 'index,frequency,amplitude\n' )

        for i in range(len(amplitudess)):
            for freq, amp in zip(freqs, amplitudess[i]):
                f.write( str(i) + ',' + str(freq) + ',' + str(amp) + '\n' )

    """
    if args.figure:
        from matplotlib import pyplot as plt
    """
else:
    # Python:ScipyのFFT（scipy.fftpack）をやってみる。 - がれすたさんのDIY日記
    # ガレスタさん
    # https://gsmcustomeffects.hatenablog.com/entry/2018/08/10/011034
    amplitudess = [[np.sqrt( xf.real**2 + xf.imag**2 ) for xf in xfs] for xfs in xfss]
    amplitudes = [np.mean(amps) for amps in zip(*amplitudess)]

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
        plt.yscale( 'log' )
        plt.plot( freqs[:int(len(freqs)/2)], amplitudes[:int(len(freqs)/2)] )
        plt.show()