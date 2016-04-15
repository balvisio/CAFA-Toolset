#!/usr/bin/python

'''
    This module has the definitions of the following methods that can be 
    invoked to locate a file:

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
        If the file is found in the source directory:
            it returns the file path to the source directory
        else if the file is found in the workspace:
            it returns the file path to the workspace
        otherwise:
            it prints and error message and then exits the program.

    Note: The main difference between locate_GOAfile and locate_SwissProtfile
        methods is that locate_GOAfile copies the file to the workspace and
        returns the file path to this workspace, whereas locate_SwissProtfile
        method does not copy the file to the workspace and returns the file
        path to the source of the file.
            
    locate_benchmark_file:
        This method takes a benchmark file as input.
        If the benchmark file exists in the workspace, it returns True.
        Otherwise, it returns False.
'''

import os
import sys
import re
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
    if os.path.exists(infile):
        return infile
    elif os.path.exists(work_dir + '/' + basename(infile)):
        return work_dir + '/' + basename(infile)
    else:
        print (infile + ' is NOT available. Quitting ' + inspect.stack() [1][1] + ' Tool ...')  
        print ('*********************************************************************')
        sys.exit(1)

def locate_benchmark_file(infile, work_dir):
    if os.path.exists(work_dir + '/' + basename(infile)):
       return True
    else:
      return False

if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print (__doc__)
    sys.exit(0) 
