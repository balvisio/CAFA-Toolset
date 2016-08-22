#!/usr/bin/env python
'''
   How to run this program: 
   python Get_taxons.py cafa3targetlist.csv uniprot_sprot.dat.2016_06 > t.txt

   The program takes takes two input files:  
       cafa3targetlist.csv: a file with protein names - one protein per line.
       uniprot_sprot.dat.2016_06: a UniProtKB/SwissProt file 
   The program retreives the taxon id for each protein in the first 
   input file from the second file. Then groups the proteins 
   according to the taxon ids. 

   It outputs these proteins by taxon ids as groups.
   It also has a method (print_protein_dict) which can be invoked to print each protein and 
   its taxon id as retrieved.
'''
import os
import sys
import subprocess
from collections import defaultdict

from Bio import SwissProt as sp

#import Config

config_filename = '.cafarc'

class Get_taxons:
    def __init__(self, tList_fname, sprot_fname):
        # Collect config file entries:
#        self.ConfigParam = Config.read_config(config_filename)
#        self.work_dir = (self.ConfigParam['workdir']).rstrip('/')
        self.work_dir = './workspace' 

        self.tList_fname = self.work_dir + '/' + tList_fname
        self.sprot_fname = self.work_dir + '/' + sprot_fname

    def obtain_taxons(self, protein_dict, fh_sprot): 
        found = False
        for rec in sp.parse(fh_sprot):
            for ac in range(len(rec.accessions)): 
                if rec.accessions[ac] in protein_dict.keys(): 
                    # assign rec.taxonomy_id list to the protein 
                    protein_dict[rec.accessions[ac]] = rec.taxonomy_id 
                    found = True
                    break
            #if found: 
            #    break 
        return protein_dict

    def group_proteins_by_taxons(self, protein_dict):
        taxons = set()
        for v in list(protein_dict.values()):
            taxons = taxons.union(set(v))
        #print(taxons)
        taxon_dict = defaultdict(list)

        for t in list(taxons):
            for p in protein_dict.keys():
                if t in protein_dict[p]:
                    taxon_dict[t].append(p)
        return taxon_dict

    def print_protein_dict(self, protein_dict):
        for k in protein_dict.keys():
            print(k + '\t' + str(protein_dict[k]))
        return None

    def print_taxon_dict(self, taxon_dict):
        for t,p in taxon_dict.items():
            print(t+'\t',', '.join(p))
        return None

    def print_taxon_dict_old(self, taxon_dict):
        # Convert the list elements to integers and then sort it: 
        taxon_nos = sorted(list(map(int,taxon_dict.keys())))
        # convert the list elements back to strings: 
        taxon_ids = list(map(str, taxon_nos))
        # print the taxon id and the corresponding proteins:  
        for t in taxon_ids:
            print(t + '\t',', '.join(taxon_dict[t]))
        return None

    def process_data(self):
        """
        This method creates all the necessary intermediate files
        that are needed to create the desired benchmark sets.
        """
        #print('Checking target proteins in the UniProt-GOA list ...')
        fh_tlist = open(self.tList_fname, 'r')
        # Create a dictionary with the target proteins:
        protein_dict = defaultdict(list)
        for line in fh_tlist:
            protName = line.strip()
            protein_dict[protName] = []
        fh_tlist.close()
        self.obtain_taxons(protein_dict, open(self.sprot_fname, 'r'))
        taxon_dict = self.group_proteins_by_taxons(protein_dict)
        #self.print_protein_dict(protein_dict)
        self.print_taxon_dict(taxon_dict)
        return None

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print (sys.argv[0] + ':')
        print(__doc__)
    else:
        # sys.argv[1]: file containing proteins, one protein in each row
        # sys.argv[2]: SwissProt file to retrieve the taxon ids from
        gt = Get_taxons(sys.argv[1], sys.argv[2])
        gt.process_data()
    sys.exit(0)
