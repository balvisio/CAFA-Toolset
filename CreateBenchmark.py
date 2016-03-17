#!/usr/bin/env python
import sys
import os
import re
from collections import defaultdict

'''
   This module has two methods - create_annotation_dict and create_benchmarks:

   create_annotation_dict: 
       This method takes a GOA file with entries only with experimental 
       evidence code and creates three dictionaries: A dictionary with 
       <protein name, GO ID> pairs for BPO type entries, one for CCO 
       type entries, and another for MFO type entries. Then it returns 
       the THREE dictionaries.        

   create_benchmarks: 
       This script filters the Limited-Knowledge(LK) and No-Knowledge(NK)
       benchmark proteins.
             For LK-benchmarks: it extracts the proteins whose annotation 
       did not have experimental evidence in a particular ontology at time 
       t1 but gained experimental evidence for that ontology at time t2. It 
       creates three LK-benchmark files - one for each ontology. 
             For NK-benchmarks: it extracts the proteins that did not have 
       experimental evidence in any of the three ontologies at time t1 but 
       gained experimental evidence at some ontology at time t2. This option 
       creates three NK-benchmark files - one for each ontology.
            The filtered proteins are saved in SIX 2-column tab delimited 
       files - one file for each ontology - for both LK and NK types. Thus, 
       create_benchmark() populate total SIX files.
'''

def create_annotation_dict(goa_exp_handle):
    # Create dictionaries with <protein, GO terms> 
    # as <key, values> pairs from t1_exp file
    t1_dict_mfo = defaultdict(lambda:set()) # initialize dictionaries 
    t1_dict_bpo = defaultdict(lambda:set())
    t1_dict_cco = defaultdict(lambda:set())
    for lines in goa_exp_handle: # populate t1_dict with entries from t1_exp
        cols = lines.strip().split('\t')
        if len(cols) < 15: # skip the lines in the header section
            continue  
        if cols[8] == 'F': # column 8: Ontology group
            t1_dict_mfo[cols[1]].add(cols[4])#col 1: protein name, col 2: GO ID
        elif cols[8] == 'P':
            t1_dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t1_dict_cco[cols[1]].add(cols[4])
    return (t1_dict_bpo, t1_dict_cco, t1_dict_mfo)

def create_benchmarks(t1_iea_handle, t1_exp_handle, t2_exp_handle, 
                      bmfile_LK_bpo_handle, bmfile_LK_cco_handle, 
                      bmfile_LK_mfo_handle, bmfile_NK_bpo_handle, 
                      bmfile_NK_cco_handle, bmfile_NK_mfo_handle):
    
    # Create dict with (protein, GO ID) from entries with exp evidence at t1:  
    t1_dict_bpo, t1_dict_cco, t1_dict_mfo = create_annotation_dict(t1_exp_handle)

    # Create dict with (protein, GO ID) from entries with exp evidence at t2:  
    t2_dict_bpo, t2_dict_cco, t2_dict_mfo = create_annotation_dict(t2_exp_handle)

    # Populate benchmark files:
    print 'Creating benchmark sets ...'
    for lines in t1_iea_handle:
        cols = lines.strip().split('\t')
        if cols[8] == 'F':
            if cols[1] not in t1_dict_mfo and cols[1] in t2_dict_mfo:
                # Limited-Knowledge benchmarks: MFO
                for term in t2_dict_mfo[cols[1]]:
                    print >> bmfile_LK_mfo_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_dict_mfo and cols[1] not in t1_dict_bpo and \
                cols[1] not in t1_dict_cco and cols[1] in t2_dict_mfo:
                # No-Knowledge benchmarks: MFO
                for term in t2_dict_mfo[cols[1]]: 
                    print >> bmfile_NK_mfo_handle, str(cols[1]) + '\t' + str(term)
        elif cols[8] == 'P':
            if cols[1] not in t1_dict_bpo and cols[1] in t2_dict_bpo:
                # Limited-Knowledge benchmarks: BPO
                for term in t2_dict_bpo[cols[1]]:
                    print >> bmfile_LK_bpo_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_dict_mfo and cols[1] not in t1_dict_bpo and \
                cols[1] not in t1_dict_cco and cols[1] in t2_dict_bpo:
                # No-Knowledge benchmarks: BPO
                for term in t2_dict_bpo[cols[1]]: 
                    print >> bmfile_NK_bpo_handle, str(cols[1]) + '\t' + str(term)
        elif cols[8] == 'C':
            if cols[1] not in t1_dict_cco and cols[1] in t2_dict_cco:
                # Limited-Knowledge benchmarks: CCO
                for term in t2_dict_cco[cols[1]]:
                    print >> bmfile_LK_cco_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_dict_mfo and cols[1] not in t1_dict_bpo and \
                cols[1] not in t1_dict_cco and cols[1] in t2_dict_cco:
                # No-Knowledge benchmarks: CCO
                for term in t2_dict_cco[cols[1]]: 
                    print >> bmfile_NK_cco_handle, str(cols[1]) + '\t' + str(term)

    # Clear all dictionaries: 
    t1_dict_bpo.clear()
    t1_dict_cco.clear()
    t1_dict_mfo.clear()

    t2_dict_bpo.clear()
    t2_dict_cco.clear()
    t2_dict_mfo.clear()

if __name__ == '__main__':
    t_exp_file = sys.argv[1]
    create_annotation_dict(t_exp_handle)

