#!/usr/bin/python

'''
    The methods in this module are written to locate a file. The full 
    description of each method is shown bellow:

    locate_GOAfile:
        This method takes a UniProt-GOA file as input.
        If the file available in the work space, 
            it returns the full pathname to the file. 
        If the file is NOT available in the workspace but is available 
            in the source directory, it copies the file to the workspace
            and then return the full pathname to the file. 
        If the file is not available in the workspace and in the source 
            directory, it quits the program with a message which 
            includes the name of program that invoked this method.

    locate_SwissProtfile:
        Does the same thing as locate_GOAfile. Please see the description for 
        locate_GOAfile.

    Note: locate_GOAfile and locate_SwissProtfile are maintained as two separate 
        methods so that in the future file type specific code could be 
        added if the need arise.   
            
    locate_benchmark_file: 
        This method takes a benchmark file as input.
        If the benchmark file exists in the workspace, it returns True.
        Otherwise, it returns False.  
'''

import os
import sys
import re
import FtpDownload
import Zipper
from collections import defaultdict
from os.path import basename
import shutil
import inspect

def locate_GOAfile(infile, work_dir):
    if os.path.exists(work_dir + '/' + basename(infile)):
        pass
    elif os.path.exists(infile):
        shutil.copy(infile, work_dir)
        print basename(infile) + ' has been copied to workspace.'
    else:
        print (infile + ' is NOT available. Quitting ' + inspect.stack() [1][1] + ' Tool ...')  
        print ('********************************************************************************')
        sys.exit(1)
    return work_dir + '/' + basename(infile)

def locate_SwissProtfile(infile, work_dir):
    if os.path.exists(work_dir + '/' + basename(infile)):
        pass
    elif os.path.exists(infile):
        shutil.copy(infile, work_dir)
        print basename(infile) + ' has been copied to workspace.'
    else:
        print (infile + ' is NOT available. Quitting ' + inspect.stack() [1][1] + ' Tool ...')  
        print ('*********************************************************************')
        sys.exit(1)
    return work_dir + '/' + basename(infile)

def locate_benchmark_file(infile, work_dir):
    if os.path.exists(work_dir + '/' + basename(infile)):
       return True
    else:
      return False

if __name__ == '__main__':
    print (__doc__)
    sys.exit(0) 
