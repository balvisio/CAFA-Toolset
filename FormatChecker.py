#!/usr/bin/python
'''
    This methods in this script check the format of an input file. 
    It has the following methods to check the file format:

    check_gaf_format():
        It checks wheter the format of the file is in GAF. 
        If the file is in GAF format, it returns True
        Otherwise, it returns False

    check_benchmark_format:
        This method returns False:
            if the input file name is an empty string or
            if the file does not exist or
            if the file size is zero or
            if the file is in correct format
        Otherwise, it returns True
'''
import os
import sys
import re
from os.path import basename
import stat

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def check_gaf_format(goa_fh):
    """
    This method checks whether the format of the file given by fname 
    is in GAF 1.0 or GAF 2.0.
    If the file is in GAF format, it returns True
    Otherwise, it returns False.  
    """
    firstline = goa_fh.readline()
    fields = firstline.strip().split('\t')
    if re.search('^\!gaf', firstline):
        return True 
    elif len(fields) == 15:
        return True 
    else:
        return False 

def check_gaf_format_old(fname):
    """
    This method checks whether the format of the file given by fname 
    is in GAF 1.0 or GAF 2.0.

    """
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

def check_benchmark_format(benchmark_fh):
    """
    This method checks the format of a benchmark file. 
    It returns False:
        if the the file is NOT in correct 2-column format
    Otherwise, it returns True
    """
    for lines in benchmark_fh:
        cols = lines.strip().split('\t')
        if len(cols) != 2:
            return False
    return True

def check_benchmark_format_old(benchmarkFile, work_dir):
    """
    This method checks the format of a benchmark file. 
    It returns False:
        the file does not exist or 
        the file size is zero or 
        the the file is NOT in correct format
    Otherwise, it returns True
    """
    if not os.path.exists(work_dir + '/' + benchmarkFile):
        return False 
    elif os.stat(work_dir + '/' + benchmarkFile).st_size == 0:
        return False
    else:
        fh = open(work_dir + '/' + benchmarkFile, 'r')
        for lines in fh:
            cols = lines.strip().split('\t')
            if len(cols) != 2:
                fh.close()
                return False
        fh.close()
        return True

if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print (__doc__)
