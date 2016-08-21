#!/usr/bin/env python
'''
    How to run this program:
    python2 match_targetList_gawk.py cafa3targetlist.csv goa_uniprot_all.gaf.2.txt

    The program takes takes two input files:  
    cafa3targetlist.csv: a file with protein names - one protein per line
    goa_uniprot_all.gaf.2.txt: a file with protein names in the first column. 
                               
    The program match each protein from the first file with all the proteins 
    in the first column of the second file and outputs the count. 
'''
import os
import sys
import subprocess

import Config

config_filename = '.cafarc'

class Find_match:
    def __init__(self, tList_fname, uniprot_fname):
        # Collect config file entries:
        self.ConfigParam = Config.read_config(config_filename)
        self.work_dir = (self.ConfigParam['workdir']).rstrip('/')

        self.tList_fname = self.work_dir + '/' + tList_fname
        self.uniprot_fname = self.work_dir + '/' + uniprot_fname

    def search_records(self):
        """
        This method creates all the necessary intermediate files
        that are needed to create the desired benchmark sets.
        """
        #command = '''gawk 'BEGIN {FS="\\t"}  $1=="P04637" {n++} END {print n}' ''' + self.uniprot_fname
        #protName = "P04637"
        #command = '''gawk 'BEGIN {FS="\\t"}  $1=="''' + protName + '''" {n++} END {print n}' ''' + self.uniprot_fname
        #print command
        #os.system(command)
        #sys.exit(0)
        #print('Checking target proteins in the UniProt-GOA list ...')
        fh_tlist = open(self.tList_fname, 'r')
        # Create file handle for output file name:
        for line in fh_tlist:
            protName = line.strip()
            command = '''gawk 'BEGIN {n=0;FS="\\t"}  $1=="''' + protName + '''" {n++} END {print n}' ''' + self.uniprot_fname 
            #print command
            val=os.system(command)
            #break
        fh_tlist.close()
        return None

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print (sys.argv[0] + ':')
        print(__doc__)
    else:
        # sys.argv[1]: a file with protein names, one per line
        # sys.argv[2]: a file with protein names, one per line
        fm = Find_match(sys.argv[1], sys.argv[2])
        fm.search_records()
    sys.exit(0)
