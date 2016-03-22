#!/usr/bin/python

import os
import sys
import re
from collections import defaultdict
from os.path import basename
import subprocess
import stat

'''
    This script checks the format of an input file. It has two methods.

    check_gaf_format(): It checks wheter the format of the file is in 
    GAF. If an error is encountered with the format, the program breaks 
    with a message.
    
    check_benchmark_format: This method takes a benchmark file as its input
    and checks for the correctness of its format. This is also the method 
    gets invoked, when this script is used from the command line.  

'''
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_gaf_format(fname):
    if os.stat(fname).st_size == 0:
        print bcolors.WARNING + 'You submitted an empty file: ' + fname + \
            bcolors.ENDC
        sys.exit(1)
    else:
        fhandle = open(fname, 'r')
        firstline = fhandle.readline()
        fields = firstline.strip().split('\t')
        if re.search('^\!gaf', firstline):
            pass
        elif len(fields) == 15:
            pass
        else:
            print bcolors.WARNING + "File format error: " + \
                fname + bcolors.ENDC
            print bcolors.WARNING + "File must be in GAF 1.0 or GAF 2.0 \
                format" + bcolors.ENDC
            fhandle.close()
            sys.exit(1)

def check_benchmark_format(benchmarkFile):
    if not os.path.exists(benchmarkFile): 
        print bcolors.WARNING + 'Warning: Benchmark file ' + \
            basename(benchmarkFile) + ' or the file path does not exist' + \
            bcolors.ENDC
    elif os.stat(benchmarkFile).st_size == 0:
        print bcolors.WARNING + 'Warning: Your submitted benchmark file ' + \
            basename(benchmarkFile) + ' is empty' + bcolors.ENDC
    else:
        fh = open(benchmarkFile, 'r')
        for lines in fh: 
            cols = lines.strip().split('\t') 
            if len(cols) != 2: 
                outfile.close()
                sys.exit(1)

if __name__ == '__main__':
    benchmark_file = sys.argv[1]
    check_benchmark_format(benchmark_file)
