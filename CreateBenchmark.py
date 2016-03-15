#!/usr/bin/env python
import sys
import os
import re
from collections import defaultdict

'''
   This script filters the Limited-Knowledge(LK) and No-Knowledge(NK) 
   benchmark proteins.

   For LK-benchmarks: it extracts the proteins whose annotation did not have 
   experimental evidence in a particular ontology at time t1 but gained 
   experimental evidence for that ontology at time t2. It creates three 
   LK-benchmark files - one for each ontology. 

   For NK-benchmarks: it extracts the proteins that did not have experimental 
   evidence in any of the three ontologies at time t1 but gained experimental 
   evidence at some ontology at time t2. This option creates three NK-benchmark 
   files - one for each ontology.

   The filtered proteins are stored in SIX 2-column tab delimited files - one 
   file for each ontology - for both LK and NK types. Thus, filter_benchmark() 
   module creates total SIX files.
'''

def create_benchmarks(t1_iea, t1_exp, t2_exp):
   # Create dictionaries with <protein, GO terms> 
   #  as <key, values> pairs from t1_exp file
    t1_dict_mfo = defaultdict(lambda:set()) # initialize dictionaries 
    t1_dict_bpo = defaultdict(lambda:set())
    t1_dict_cco = defaultdict(lambda:set())
    t1_exp_handle = open(t1_exp, 'r') # open t1_exp file
    for lines in t1_exp_handle: # populate t1_dict with entries from t1_exp
        cols = lines.strip().split('\t')
        if len(cols) < 15: # skip the lines in the header section
            continue  
        if cols[8] == 'F': # column 8: Ontology group
            t1_dict_mfo[cols[1]].add(cols[4])#col 1: protein name, col 2: GO ID
        elif cols[8] == 'P':
            t1_dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t1_dict_cco[cols[1]].add(cols[4])
    t1_exp_handle.close()

   # Create dictionaries with <protein, GO terms> 
   # as <key, values> pairs from t2_exp file
    t2_dict_mfo = defaultdict(lambda:set()) # initialize t2_dict dictionaries
    t2_dict_bpo = defaultdict(lambda:set())
    t2_dict_cco = defaultdict(lambda:set())
    t2_handle = open(t2_exp, 'r') # open t2_exp file
    for lines in t2_handle: # populate t2_dict with entries from t2_exp file
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        if cols[8] == 'F':
            t2_dict_mfo[cols[1]].add(cols[4])
        elif cols[8] == 'P':
            t2_dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t2_dict_cco[cols[1]].add(cols[4])
    t2_handle.close()

    # Open files to write Limited-Knowledge(LK) benchmark entries
    outfile_LK_bpo = open(t2_exp + '.bpo_LK_bench.txt' , 'w')
    outfile_LK_cco = open(t2_exp + '.cco_LK_bench.txt' , 'w')
    outfile_LK_mfo = open(t2_exp + '.mfo_LK_bench.txt' , 'w')

    # Open files to write No-Knowledge(NK) benchmark entries
    outfile_NK_bpo = open(t2_exp + '.bpo_NK_bench.txt' , 'w')
    outfile_NK_cco = open(t2_exp + '.cco_NK_bench.txt' , 'w')
    outfile_NK_mfo = open(t2_exp + '.mfo_NK_bench.txt' , 'w')

    # Creating benchmark set ...
    t1_iea_handle = open(t1_iea, 'r')
    for lines in t1_iea_handle:
        cols = lines.strip().split('\t')
        if cols[8] == 'F':
            if cols[1] not in t1_dict_mfo and cols[1] in t2_dict_mfo:
                # Limited-Knowledge benchmarks: MFO
                for term in t2_dict_mfo[cols[1]]:
                    print >> outfile_LK_mfo, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_dict_mfo and cols[1] not in t1_dict_bpo and \
                cols[1] not in t1_dict_cco and cols[1] in t2_dict_mfo:
                # No-Knowledge benchmarks: MFO
                for term in t2_dict_mfo[cols[1]]: 
                    print >> outfile_NK_mfo, str(cols[1]) + '\t' + str(term)

        elif cols[8] == 'P':
            if cols[1] not in t1_dict_bpo and cols[1] in t2_dict_bpo:
                # Limited-Knowledge benchmarks: MFO
                for term in t2_dict_bpo[cols[1]]:
                    print >> outfile_LK_bpo, str(cols[1]) + '\t' + str(term)

            if cols[1] not in t1_dict_mfo and cols[1] not in t1_dict_bpo and \
                cols[1] not in t1_dict_cco and cols[1] in t2_dict_bpo:
                # No-Knowledge benchmarks: MFO
                for term in t2_dict_bpo[cols[1]]: 
                    print >> outfile_NK_bpo, str(cols[1]) + '\t' + str(term)

        elif cols[8] == 'C':
            if cols[1] not in t1_dict_cco and cols[1] in t2_dict_cco:
                # Limited-Knowledge benchmarks: MFO
                for term in t2_dict_cco[cols[1]]:
                    print >> outfile_LK_cco, str(cols[1]) + '\t' + str(term)

            if cols[1] not in t1_dict_mfo and cols[1] not in t1_dict_bpo and \
                cols[1] not in t1_dict_cco and cols[1] in t2_dict_cco:
                # No-Knowledge benchmarks: MFO
                for term in t2_dict_cco[cols[1]]: 
                    print >> outfile_NK_cco, str(cols[1]) + '\t' + str(term)

    # Close all open files
    t1_iea_handle.close()
    outfile_LK_mfo.close()
    outfile_LK_bpo.close()
    outfile_LK_cco.close()
    outfile_NK_mfo.close()
    outfile_NK_bpo.close()
    outfile_NK_cco.close()

    #Clear all dictionaries 
    t1_dict_mfo.clear()
    t1_dict_bpo.clear()
    t1_dict_cco.clear()
    t2_dict_mfo.clear()
    t2_dict_bpo.clear()
    t2_dict_cco.clear()

if __name__ == '__main__':
    t1_iea_file = sys.argv[1]
    t1_exp_file = sys.argv[2]
    t2_exp_file = sys.argv[3]
    create_benchmarks(t1_iea_file, t1_exp_file, t2_exp_file)
