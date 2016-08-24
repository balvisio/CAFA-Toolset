#!/usr/bin/env python
'''
   How to run this program: 
   python Get_goterms.py cafa3targetlist.csv cafa3targets_sprot.dat > cafa3targets-goterms.txt

   The program takes takes two input files:  
       cafa3targetlist.csv: a file with protein names - one protein per line.
       cafa3targets_sprot.dat: a subset of UniProt database in 
                               UniProtKB/SwissProt file format
   The program retreives the set of GO term information 
   (GO term, Exp Ev Code, Ont) from the second file for each protein in the 
   first input file . Then groups the proteins according to the taxon ids.

   It outputs each protein and the corresponding set of GO term information.
   If a protein in the list is obsolete or does not have any GO term information 
   in the database, it will not print anything about that protein.
'''
import os
import sys
import subprocess
from collections import defaultdict

from Bio import SwissProt as sp

#import Config

config_filename = '.cafarc'

class Get_goterms:
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

    def obtain_goterms(self, goterm_dict, fh_sprot):
        found = False
        for rec in sp.parse(fh_sprot):
            for ac in range(len(rec.accessions)):
                goList = []
                if rec.accessions[ac] in goterm_dict.keys():
                    for crossRef in rec.cross_references:
                        if crossRef[0] == 'GO':
                           goDef = (crossRef[1], (crossRef[3].split(':'))[0], \
                                     crossRef[2][0])
                           goterm_dict[rec.accessions[ac]].add(goDef)
                    found = True
                    break
            #if found: 
                #break 
        return goterm_dict

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
        for p,t in protein_dict.items():
            print(p + '\t' + ','.join(t))
        return None

    def print_taxon_dict(self, taxon_dict):
        for t,p in taxon_dict.items():
            print(t+'\t',', '.join(p))
        return None

    def print_goterm_dict(self, goterm_dict):
        count=0
        for p,v in goterm_dict.items():
            print('>'+p)
            # Print the tuples in the set of GO term information
            # (GO term, Exp Ev. Code, Ont):
            if not v: 
                continue 
            for tp in v: 
                print(','.join(str(e) for e in tp))
                pass
            print('//')
            count+=1
        #print(count)
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

        # Create a dictionary with the target proteins as keys and set of
        # retreived GO term tuple (GO term, Exp Evid Code, Ont) as values:
        goterm_dict = defaultdict(set)

        for line in fh_tlist:
            protName = line.strip()
            protein_dict[protName] = []
            goterm_dict[protName]= set()
        fh_tlist.close()

        #self.obtain_taxons(protein_dict, open(self.sprot_fname, 'r'))
        self.obtain_goterms(goterm_dict, open(self.sprot_fname, 'r'))

        #taxon_dict = self.group_proteins_by_taxons(protein_dict)
        #self.print_protein_dict(protein_dict)
        #self.print_taxon_dict(taxon_dict)
        self.print_goterm_dict(goterm_dict)
        return None

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print (sys.argv[0] + ':')
        print(__doc__)
    else:
        # sys.argv[1]: file containing proteins, one protein in each row
        # sys.argv[2]: SwissProt file to retrieve the taxon ids from
        gt = Get_goterms(sys.argv[1], sys.argv[2])
        gt.process_data()
    sys.exit(0)
