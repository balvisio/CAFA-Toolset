#!/usr/bin/env python

import os
import sys
from collections import defaultdict

'''
   The entry point of this module is create_benchmarks method. It has 
   the following arguments:    
            t1_iea_handle: file handle for t1_iea file 
            t1_exp_handle: file handle for t1_exp file 
            t2_exp_handle: file handle for t2_exp file 
            bmfile_LK_bpo_handle: file handle in append mode for LK-BPO type benchmark file
            bmfile_LK_cco_handle: file handle in append mode for LK-CCO type benchmark file
            bmfile_LK_mfo_handle: file handle in append mode for LK-MFO type benchmark file
            bmfile_NK_bpo_handle: file handle in append mode for LK-BPO type benchmark file
            bmfile_NK_cco_handle: file handle in append mode for LK-CCO type benchmark file
            bmfile_NK_mfo_handle: file handle in append mode for LK-MFO type benchmark file
   
       This method filters the Limited-Knowledge(LK) and No-Knowledge(NK)
       benchmark proteins as described below:
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

   This module has the following two methods to aid the benchmark creation by 
   the above method:

   create_annotation_dict: 
       This method takes a GOA file with no header section. It creates 
       THREE dictionaries. A dictionary with <protein name, GO ID> pairs 
       for BPO type entries, one for CCO type entries, and the thrid one 
       for MFO type entries. Then it returns these THREE dictionaries.

   write_benchmarks: 
      This method does the actual writing of the benchmark entries to the 
      benchmark output file. create_benchmarks repeatedly calls this method 
      to write the benchmarks to the output file.     
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

def write_benchmarks(protName,
                    t1_bpo_dict,
                    t1_cco_dict,
                    t1_mfo_dict,
                    t2_xxo_dict,
                    bmfile_LK_xxo_handle,
                    bmfile_NK_xxo_handle,
                    LKtype # Can take string BPO, CCO, or MFO
                   ):
    if LKtype.upper() == 'BPO':
        t1_xxo_dict = t1_bpo_dict
    elif LKtype.upper() == 'CCO':
        t1_xxo_dict = t1_cco_dict
    elif LKtype.upper() == 'MFO':
        t1_xxo_dict = t1_mfo_dict
    else:
        print 'Error in write_benchmarks parameter passing'
        sys.exit(1)

    if protName not in t1_xxo_dict and protName in t2_xxo_dict:
        # Limited-Knowledge benchmarks: BPO, CCO, or MFO type based on LKtype
        for term in t2_xxo_dict[protName]:
            print >> bmfile_LK_xxo_handle, str(protName) + '\t' + str(term)
    if protName not in t1_mfo_dict and protName not in t1_bpo_dict and \
       protName not in t1_cco_dict and protName in t2_xxo_dict:
        # No-Knowledge benchmarks: BPO, CCO, or MFO type based on LKtype
        for term in t2_xxo_dict[protName]:
            print >> bmfile_NK_xxo_handle, str(protName) + '\t' + str(term)
    return None

def create_benchmarks(t1_iea_handle,
                      t1_exp_handle,
                      t2_exp_handle,
                      bmfile_LK_bpo_handle,
                      bmfile_LK_cco_handle,
                      bmfile_LK_mfo_handle,
                      bmfile_NK_bpo_handle,
                      bmfile_NK_cco_handle,
                      bmfile_NK_mfo_handle):
    # Create dict for (protein, GO ID) from entries with EXP evidence code at t1:
    t1_bpo_dict, t1_cco_dict, t1_mfo_dict = create_annotation_dict(t1_exp_handle)

    # Create dict for (protein, GO ID) from entries with EXP evidence code at t2:
    t2_bpo_dict, t2_cco_dict, t2_mfo_dict = create_annotation_dict(t2_exp_handle)

    # Populate benchmark files:
    print 'Creating benchmark sets ...'
    for lines in t1_iea_handle:
        cols = lines.strip().split('\t')
        if cols[8] == 'F':
            # write out MFO type benchmarks: 
            write_benchmarks(cols[1],
                             t1_bpo_dict,
                             t1_cco_dict,
                             t1_mfo_dict,
                             t2_mfo_dict,
                             bmfile_LK_mfo_handle,
                             bmfile_NK_mfo_handle,
                             'MFO'
                            )
        elif cols[8] == 'P':
            # write out BPO type benchmarks: 
            write_benchmarks(cols[1],
                              t1_bpo_dict,
                              t1_cco_dict,
                              t1_mfo_dict,
                              t2_bpo_dict,
                              bmfile_LK_bpo_handle,
                              bmfile_NK_bpo_handle,
                              'BPO'
                            )
        elif cols[8] == 'C':
            # write out CCO type benchmarks: 
            write_benchmarks(cols[1],
                             t1_bpo_dict,
                             t1_cco_dict,
                             t1_mfo_dict,
                             t2_cco_dict,
                             bmfile_LK_cco_handle,
                             bmfile_NK_cco_handle,
                             'CCO',
                            )
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
