#!/usr/bin/env python
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
        #command = 'grep -c ' + 'A0A010NCN4' + ' ' + self.uniprot_fname
        #os.system(command)
        #sys.exit(0)
        #print('Checking target proteins in the UniProt-GOA list ...')
        fh_tlist = open(self.tList_fname, 'r')
        # Create file handle for output file name:
        for line in fh_tlist:
            protName = line.strip()
            command = 'grep -c ' + protName + ' ' + self.uniprot_fname 
            os.system(command)
            #break
        fh_tlist.close()
        return None

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print (sys.argv[0] + ':')
        print(__doc__)
    else:
        fm = Find_match(sys.argv[1], sys.argv[2])
        fm.search_records()
    sys.exit(0)
