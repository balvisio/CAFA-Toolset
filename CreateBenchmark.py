#!/usr/bin/env python
import sys
import os
import re
from collections import defaultdict

'''
   This module has two methods: create_annotation_dict and create_benchmarks.

   create_annotation_dict: 
       This method takes a GOA file with no header section. It creates 
       THREE dictionaries. A dictionary with <protein name, GO ID> pairs 
       for BPO type entries, one for CCO type entries, and the thrid one 
       for MFO type entries. Then it returns these THREE dictionaries.

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
    # Initialize THREE dictionaries:
    t1_mfo_dict = defaultdict(lambda:set())  
    t1_bpo_dict = defaultdict(lambda:set())
    t1_cco_dict = defaultdict(lambda:set())

    # Populate the dictionaries: 
    for lines in goa_exp_handle: 
        cols = lines.strip().split('\t')
        if len(cols) < 15: # Skip lines NOT in GAF 1.0 or GAF 2.0 format
            continue
        if cols[8] == 'F': # Col 8: Ontology group
            t1_mfo_dict[cols[1]].add(cols[4]) # Col 1: protein name, Col 2: GO ID
        elif cols[8] == 'P':
            t1_bpo_dict[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            t1_cco_dict[cols[1]].add(cols[4])
    return (t1_bpo_dict, t1_cco_dict, t1_mfo_dict)







def create_benchmarks(t1_iea_handle, t1_exp_handle, t2_exp_handle, 
                      bmfile_LK_bpo_handle, bmfile_LK_cco_handle, 
                      bmfile_LK_mfo_handle, bmfile_NK_bpo_handle, 
                      bmfile_NK_cco_handle, bmfile_NK_mfo_handle):
    # Create dict for (protein, GO ID) from entries with EXP evidence code at t1:
    t1_bpo_dict, t1_cco_dict, t1_mfo_dict = create_annotation_dict(t1_exp_handle)

    # Create dict for (protein, GO ID) from entries with EXP evidence code at t2:
    t2_bpo_dict, t2_cco_dict, t2_mfo_dict = create_annotation_dict(t2_exp_handle)

    # Populate benchmark files:
    print 'Creating benchmark sets ...'
    for lines in t1_iea_handle:
        cols = lines.strip().split('\t')
        if cols[8] == 'F':
            if cols[1] not in t1_mfo_dict and cols[1] in t2_mfo_dict:
                # Limited-Knowledge benchmarks: MFO
                for term in t2_mfo_dict[cols[1]]:
                    print >> bmfile_LK_mfo_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_mfo_dict and cols[1] not in t1_bpo_dict and \
                cols[1] not in t1_cco_dict and cols[1] in t2_mfo_dict:
                # No-Knowledge benchmarks: MFO
                for term in t2_mfo_dict[cols[1]]: 
                    print >> bmfile_NK_mfo_handle, str(cols[1]) + '\t' + str(term)
        elif cols[8] == 'P':
            if cols[1] not in t1_bpo_dict and cols[1] in t2_bpo_dict:
                # Limited-Knowledge benchmarks: BPO
                for term in t2_bpo_dict[cols[1]]:
                    print >> bmfile_LK_bpo_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_mfo_dict and cols[1] not in t1_bpo_dict and \
                cols[1] not in t1_cco_dict and cols[1] in t2_bpo_dict:
                # No-Knowledge benchmarks: BPO
                for term in t2_bpo_dict[cols[1]]: 
                    print >> bmfile_NK_bpo_handle, str(cols[1]) + '\t' + str(term)
        elif cols[8] == 'C':
            if cols[1] not in t1_cco_dict and cols[1] in t2_cco_dict:
                # Limited-Knowledge benchmarks: CCO
                for term in t2_cco_dict[cols[1]]:
                    print >> bmfile_LK_cco_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_mfo_dict and cols[1] not in t1_bpo_dict and \
                cols[1] not in t1_cco_dict and cols[1] in t2_cco_dict:
                # No-Knowledge benchmarks: CCO
                for term in t2_cco_dict[cols[1]]: 
                    print >> bmfile_NK_cco_handle, str(cols[1]) + '\t' + str(term)

    # Clear all dictionaries: 
    t1_bpo_dict.clear()
    t1_cco_dict.clear()
    t1_mfo_dict.clear()

    t2_bpo_dict.clear()
    t2_cco_dict.clear()
    t2_mfo_dict.clear()
    return None


def create_benchmarks_old(t1_iea_handle, t1_exp_handle, t2_exp_handle, 
                      bmfile_LK_bpo_handle, bmfile_LK_cco_handle, 
                      bmfile_LK_mfo_handle, bmfile_NK_bpo_handle, 
                      bmfile_NK_cco_handle, bmfile_NK_mfo_handle):
    # Create dict for (protein, GO ID) from entries with EXP evidence code at t1:
    t1_bpo_dict, t1_cco_dict, t1_mfo_dict = create_annotation_dict(t1_exp_handle)

    # Create dict for (protein, GO ID) from entries with EXP evidence code at t2:
    t2_bpo_dict, t2_cco_dict, t2_mfo_dict = create_annotation_dict(t2_exp_handle)

    # Populate benchmark files:
    print 'Creating benchmark sets ...'
    for lines in t1_iea_handle:
        cols = lines.strip().split('\t')
        if cols[8] == 'F':
            if cols[1] not in t1_mfo_dict and cols[1] in t2_mfo_dict:
                # Limited-Knowledge benchmarks: MFO
                for term in t2_mfo_dict[cols[1]]:
                    print >> bmfile_LK_mfo_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_mfo_dict and cols[1] not in t1_bpo_dict and \
                cols[1] not in t1_cco_dict and cols[1] in t2_mfo_dict:
                # No-Knowledge benchmarks: MFO
                for term in t2_mfo_dict[cols[1]]: 
                    print >> bmfile_NK_mfo_handle, str(cols[1]) + '\t' + str(term)
        elif cols[8] == 'P':
            if cols[1] not in t1_bpo_dict and cols[1] in t2_bpo_dict:
                # Limited-Knowledge benchmarks: BPO
                for term in t2_bpo_dict[cols[1]]:
                    print >> bmfile_LK_bpo_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_mfo_dict and cols[1] not in t1_bpo_dict and \
                cols[1] not in t1_cco_dict and cols[1] in t2_bpo_dict:
                # No-Knowledge benchmarks: BPO
                for term in t2_bpo_dict[cols[1]]: 
                    print >> bmfile_NK_bpo_handle, str(cols[1]) + '\t' + str(term)
        elif cols[8] == 'C':
            if cols[1] not in t1_cco_dict and cols[1] in t2_cco_dict:
                # Limited-Knowledge benchmarks: CCO
                for term in t2_cco_dict[cols[1]]:
                    print >> bmfile_LK_cco_handle, str(cols[1]) + '\t' + str(term)
            if cols[1] not in t1_mfo_dict and cols[1] not in t1_bpo_dict and \
                cols[1] not in t1_cco_dict and cols[1] in t2_cco_dict:
                # No-Knowledge benchmarks: CCO
                for term in t2_cco_dict[cols[1]]: 
                    print >> bmfile_NK_cco_handle, str(cols[1]) + '\t' + str(term)

    # Clear all dictionaries: 
    t1_bpo_dict.clear()
    t1_cco_dict.clear()
    t1_mfo_dict.clear()

    t2_bpo_dict.clear()
    t2_cco_dict.clear()
    t2_mfo_dict.clear()
    return None




if __name__ == '__main__':
    goa_file_handle = sys.argv[1] # a GOA file with no header section
    create_annotation_dict(goa_file_handle) # Create three dictionaries
