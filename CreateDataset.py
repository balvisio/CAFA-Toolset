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
'''

def parse(infile, ConfigParam=defaultdict):
    work_dir = ConfigParam['workdir']
    t1_input_file = None
    input_basename = basename(infile)
    if os.path.exists(work_dir + '/' + input_basename):
        t1_input_file = input_basename
    elif os.path.exists(infile):
        shutil.move(infile,work_dir)
        t1_input_file = basename(infile)
        print t1_input_file + ' has been moved to work directory'
    else:
        print infile + ' is not available.'
        sys.exit(1)

    if re.search('\.gz$',t1_input_file):
        extracted_file = t1_input_file.replace('.gz','')
        if os.path.exists(work_dir + '/' + extracted_file):
            t1_input_file = ''
            t1_input_file = extracted_file
        elif os.path.exists(extracted_file):
            shutil.move(extracted_file,work_dir)
            t1_input_file = ''
            t1_input_file = extracted_file
        else:
            extracted_file = Zipper.unzipper(t1_input_file, ConfigParam)
            t1_input_file = ''
            t1_input_file = extracted_file

    return t1_input_file

if __name__ == '__main__':
    print 'This program do not run indepedently'
    sys.exit(1) 
