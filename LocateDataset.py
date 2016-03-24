#!/usr/bin/python
import os
import sys
import re
import FtpDownload
import Zipper
from collections import defaultdict
from os.path import basename
import shutil

'''
   Given an input filename or time point, the script calls the FTP utility
   of uniprot-goa to download required files. 
   This script takes a file as input and checks whether it is in the current 
   directory. If the file is already present in the current working 
   directory, it moves it to the workspace folder. If the file is not in 
   the current directory or in the workspace folder, it gives an error 
   message.

   locate_GOAfile: This method tries to locate a GOA filer: 
        If the file is NOT found in the workspace the method copies 
        the file from the source to the workspace.  
        At the end, it returns the filepath.   
        If the method does NOT find the file in the workspace 
        or in the the source directory specificied, it prints 
        error message and exit the program.
'''

def locate_GOAfile(infile, work_dir):
    if os.path.exists(work_dir + '/' + basename(infile)):
        pass
    elif os.path.exists(infile):
        shutil.copy(infile, work_dir)
        print basename(infile) + ' has been copied to workspace.'
    else:
        print infile + ' is not available.'
        sys.exit(1)
    return work_dir + '/' + basename(infile)

def locate_SwissProtfile(infile, work_dir, ConfigParam=defaultdict):
    t1_input_file = None
    input_basename = basename(infile)
    if os.path.exists(work_dir + '/' + input_basename):
        t1_input_file = work_dir + '/' + input_basename
    elif os.path.exists(infile):
        filePath = os.path.dirname(os.path.realpath(infile))
        shutil.copy(infile, work_dir)
        print basename(infile) + ' has been copied to work directory'
        t1_input_file = filePath + '/' + basename(infile)
    else:
        print infile + ' is not available.'
        sys.exit(1)

    return t1_input_file

def locate_benchmark_file(infile, work_dir):
    if os.path.exists(work_dir + '/' + basename(infile)):
       return True 
    else: 
      return False  

if __name__ == '__main__':
    print 'This program do not run indepedently'
    sys.exit(1) 
