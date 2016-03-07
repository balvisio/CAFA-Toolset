#!/usr/bin/python

import os
import sys
import re
from collections import defaultdict
from os.path import basename
import subprocess
import stat

'''
    A script that checks the format and content of input files.
    Mainly written to check format of input files given to the
    Benchmark program.
    Takes in 2 uniprot-goa files as input along with the program mode,
    whether CAFA or non-CAFA
    If an error is encountered with the format, the program breaks
    with a message
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
        print bcolors.WARNING + 'You submitted an empty file: ' + fname + bcolors.ENDC
        sys.exit(1)
    else:
        fhandle = open(fname, 'r')
        firstline = fhandle.readline()
        if firstline.strip() == '!gaf-version: 1.0' or firstline.strip() == '!gaf-version: 2.0'  :
            pass
        else:
            print bcolors.WARNING + "File format error: " + fname + bcolors.ENDC
            print bcolors.WARNING + "File must be in GAF 1.0 or GAF 2.0 format" + bcolors.ENDC
            fhandle.close()
            sys.exit(1)

def check(infile1, infile2, program):
    if program == 'T': # CAFA mode
        if not re.match('\S+\.fasta$', infile1):
            print bcolors.FAIL + 'Incorrect file extension for input file name at time t1' + bcolors.ENDC 
            sys.exit(1)
        elif os.stat(infile1).st_size == 0:
            print bcolors.FAIL + 'You have submitted an empty t1 file.' + bcolors.ENDC 
            sys.exit(1)
        elif re.match('\S+\.fasta$', infile1):
            pattern = '>'
            outfile = open('tmp.txt', 'w')
            subprocess.call(['grep', pattern, infile1], stdout=outfile)
            if not os.stat('tmp.txt').st_size > 0:
                print bcolors.FAIL + 'Probably incorrect format for fasta file.' + bcolors.ENDC 
                sys.exit(1)

        if os.stat(infile2).st_size == 0:
            print 'You have submitted an empty t2 file.'
            sys.exit(1)
        else:
            infile2_handle = open(infile2, 'r')
            firstline = infile2_handle.readline()
            fields = firstline.strip().split('\t')
            if re.search('^\!gaf', firstline):
                pass
            elif len(fields) == 15:
                pass
            else:
                print "Error in t2 file format"
                sys.exit(1)
    elif program == 'F': # non-CAFA mode
        if os.stat(infile1).st_size == 0:
            print 'You have submitted an empty t1 file.'
            sys.exit(1)
        else:
            infile1_handle = open(infile1, 'r')
            firstline = infile1_handle.readline()
            fields = firstline.strip().split('\t')
            if firstline.strip() == '!gaf-version: 2.0': 
                pass
            else:
                print "Error in t1 file format"
                sys.exit(1)

        if os.stat(infile2).st_size == 0:
            print 'You have submitted an empty t2 file.'
            sys.exit(1)
        else:
            infile2_handle = open(infile2, 'r')
            firstline = infile2_handle.readline()
            fields = firstline.strip().split('\t')
            if re.search('^\!gaf', firstline):
                pass
            elif len(fields) == 15:
                pass
            else:
                print "Error in t2 file format"
                sys.exit(1)
        
def checkBenchmarkFormat(benchmarkFile):
    if not os.path.exists(benchmarkFile): 
        print bcolors.WARNING + 'Warning: Benchmark file ' + basename(benchmarkFile) + ' or the file path does not exist' + bcolors.ENDC
    elif os.stat(benchmarkFile).st_size == 0:
        print bcolors.WARNING + 'Warning: Your submitted benchmark file ' + basename(benchmarkFile) + ' is empty' + bcolors.ENDC
    else:
        fh = open(benchmarkFile, 'r')
        for lines in fh: 
            cols = lines.strip().split('\t') 
            if len(cols) != 2: 
                outfile.close()
                sys.exit(1)

if __name__ == '__main__':
    infile1 = sys.argv[1]
    infile2 = sys.argv[2]
    mode = 'F'
    check(infile1, infile2, program)
