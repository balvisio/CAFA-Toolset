#!/usr/bin/env python
from collections import defaultdict
import sys
import os.path

'''
    This script verifies the Limited-Knowledge(LK) and No-Knowledge(NK) 
    benchmark sets created by CreateBenchmark program.
'''

def create_iea_dict(iea_handle):
     # Initialize a dictionar which will later be populated with
    # <protein, GO ID> tuples from t1_iea file:
    dict_iea = defaultdict(lambda:set())
    # Populate the dictionar for t1_iea with <protein, GO terms> as
    # <key, values> pairs from the entries with NOn-Experimental Evidence
    # at time t1:
    for lines in iea_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        dict_iea[cols[1]].add(cols[4])
        # Column 1: protein name, Column 4: GO ID 
    return dict_iea

def create_exp_dict(exp_handle):
    # Initialize three dictionaries in BPO, CCO, and MFO ontology groups
    # which will later be populated with <protein, GO ID> tuples from
    # t1_exp file ontology groups: 
    dict_bpo = defaultdict(lambda:set())
    dict_cco = defaultdict(lambda:set())
    dict_mfo = defaultdict(lambda:set()) 

    # Populate the three dictionaries for t1_exp with <protein, GO terms> 
    # as <key, values> pairs from the entries with Non-Experimental Evidence 
    # at time t1:
    for lines in exp_handle:
        cols = lines.strip().split('\t')
        if len(cols) < 15:
            continue
        if cols[8] == 'F': # Column 8: Ontology group
            dict_mfo[cols[1]].add(cols[4]) 
            # Column 1: protein name, Column 4: GO ID 
        elif cols[8] == 'P':
            dict_bpo[cols[1]].add(cols[4])
        elif cols[8] == 'C':
            dict_cco[cols[1]].add(cols[4])
    return (dict_bpo, dict_cco, dict_mfo)

def verify_LK_benchmark_bpo(t1_iea_dict,
                            t1_bpo_dict,
                            t1_cco_dict,
                            t1_mfo_dict,
                            t2_bpo_dict,
                            t2_cco_dict,
                            t2_mfo_dict,
                            output_filename_LK_bpo,
                            LKcount):
    # Verify the benchmark entries in the benchmark file output_filename_LK_bpo:
    if os.path.exists(output_filename_LK_bpo) and \
       os.stat(output_filename_LK_bpo).st_size != 0:
        outfile_LK_bpo_handle = open(output_filename_LK_bpo, 'r')
        for lines in outfile_LK_bpo_handle: 
            cols = lines.strip().split('\t')
            if cols[0] not in t1_iea_dict:
                print 'Error: an undesired protein ' + cols[0] + \
                      ' got selected in ' + output_filename_LK_bpo
                break
            elif cols[0] in t1_bpo_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                       output_filename_LK_bpo + ' already had experimental \
                       evidence at t1'
                break
            elif cols[0] not in t2_bpo_dict or cols[1] not in t2_bpo_dict[cols[0]]:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_LK_bpo + ' has not gained experimental \
                      evidence at t2'
                break 
        outfile_LK_bpo_handle.close() 
        LKcount += 1
    return LKcount    

def verify_LK_benchmark_cco(t1_iea_dict,
                            t1_bpo_dict,
                            t1_cco_dict,
                            t1_mfo_dict,
                            t2_bpo_dict,
                            t2_cco_dict,
                            t2_mfo_dict,
                            output_filename_LK_cco,
                            LKcount):
    # Verify the benchmark entries in the benchmark file output_filename_LK_cco:
    if os.path.exists(output_filename_LK_cco) and \
       os.stat(output_filename_LK_cco).st_size != 0:

        outfile_LK_cco_handle = open(output_filename_LK_cco, 'r')
        for lines in outfile_LK_cco_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_iea_dict:
                print 'Error: an undesired protein ' + cols[0] + \
                      ' got selected in ' + output_filename_LK_cco
                break
            elif cols[0] in t1_cco_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_LK_cco + ' already had experimental \
                      evidence at t1'
                break
            elif cols[0] not in t2_cco_dict or \
                 cols[1] not in t2_cco_dict[cols[0]]:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_LK_cco + ' has not gained experimental \
                      evidence at t2'
                break
        outfile_LK_cco_handle.close()
        LKcount += 1
    return LKcount

def verify_LK_benchmark_mfo(t1_iea_dict,
                            t1_bpo_dict,
                            t1_cco_dict,
                            t1_mfo_dict,
                            t2_bpo_dict,
                            t2_cco_dict,
                            t2_mfo_dict,
                            output_filename_LK_mfo,
                            LKcount):
    # Verify the benchmark entries in the benchmark file output_filename_LK_mfo:
    if os.path.exists(output_filename_LK_mfo) and \
       os.stat(output_filename_LK_mfo).st_size != 0:
        outfile_LK_mfo_handle = open(output_filename_LK_mfo, 'r')
        for lines in outfile_LK_mfo_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_iea_dict:
                  print 'Error: an undesired protein ' + cols[0] + \
                        ' got selected in ' + output_filename_LK_mfo
                  break
            elif cols[0] in t1_mfo_dict:
                  print 'Error: selected protein ' + cols[0] + ' in ' + \
                        output_filename_LK_mfo + ' already had experimental \
                        evidence at t1'
                  break
            elif cols[0] not in t2_mfo_dict or \
                 cols[1] not in t2_mfo_dict[cols[0]]:
                  print 'Error: selected protein ' + cols[0] + ' in ' + \
                        output_filename_LK_mfo + ' has not gained experimental \
                        evidence at t2'
                  break
        outfile_LK_mfo_handle.close()
        LKcount += 1
    return LKcount

def verify_NK_benchmark_bpo(t1_iea_dict,
                            t1_bpo_dict,
                            t1_cco_dict,
                            t1_mfo_dict,
                            t2_bpo_dict,
                            t2_cco_dict,
                            t2_mfo_dict,
                            output_filename_NK_bpo,
                            NKcount):
    # Verify the benchmark entries in the benchmark file: output_filename_NK_bpo
    if os.path.exists(output_filename_NK_bpo) and \
       os.stat(output_filename_NK_bpo).st_size != 0:
        outfile_NK_bpo_handle = open(output_filename_NK_bpo, 'r')
        for lines in outfile_NK_bpo_handle: 
            cols = lines.strip().split('\t')
            if cols[0] not in t1_iea_dict:
                print 'Error: an undesired protein ' + cols[0] + \
                      ' got selected in ' + output_filename_NK_bpo
                break
            elif cols[0] in t1_bpo_dict or \
                 cols[0] in t1_cco_dict or \
                 cols[0] in t1_mfo_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_NK_bpo + ' already had experimental \
                      evidence at t1'
                break
            elif cols[0] not in t2_bpo_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_NK_bpo + ' has not gained experimental \
                      evidence at t2'
                break 
        outfile_NK_bpo_handle.close() 
        NKcount += 1
    return NKcount

def verify_NK_benchmark_cco(t1_iea_dict,
                            t1_bpo_dict,
                            t1_cco_dict,
                            t1_mfo_dict,
                            t2_bpo_dict,
                            t2_cco_dict,
                            t2_mfo_dict,
                            output_filename_NK_cco,
                            NKcount):
    # Verify the benchmark entries in the benchmark file: output_filename_NK_cco
    if os.path.exists(output_filename_NK_cco) and \
       os.stat(output_filename_NK_cco).st_size != 0:
        outfile_NK_cco_handle = open(output_filename_NK_cco, 'r')
        for lines in outfile_NK_cco_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_iea_dict:
                print 'Error: an undesired protein ' + cols[0] + \
                      ' got selected in ' + output_filename_NK_cco
                break
            elif cols[0] in t1_bpo_dict or \
                 cols[0] in t1_cco_dict or \
                 cols[0] in t1_mfo_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_NK_cco + ' already had experimental \
                      evidence at t1'
                break
            elif cols[0] not in t2_cco_dict:
                print 'Error: selected protein ' + cols[0] + ' in ' + \
                      output_filename_NK_cco + ' has not gained experimental \
                      evidence at t2'
                break 
        outfile_NK_cco_handle.close() 
        NKcount += 1
    return NKcount

def verify_NK_benchmark_mfo(t1_iea_dict,
                            t1_bpo_dict,
                            t1_cco_dict,
                            t1_mfo_dict,
                            t2_bpo_dict,
                            t2_cco_dict,
                            t2_mfo_dict,
                            output_filename_NK_mfo,
                            NKcount):
    # Verify the benchmark entries in the benchmark file: output_filename_NK_mfo
    if os.path.exists(output_filename_NK_mfo) and \
       os.stat(output_filename_NK_mfo).st_size != 0:
        outfile_NK_mfo_handle = open(output_filename_NK_mfo, 'r')
        for lines in outfile_NK_mfo_handle:
            cols = lines.strip().split('\t')
            if cols[0] not in t1_iea_dict:
                  print 'Error: an undesired protein ' + cols[0] + \
                        ' got selected in ' + output_filename_NK_mfo
                  break
            elif cols[0] in t1_bpo_dict or \
                 cols[0] in t1_cco_dict or \
                 cols[0] in t1_mfo_dict:
                  print 'Error: selected protein ' + cols[0] + ' in ' + \
                        output_filename_NK_mfo + ' already had experimental \
                        evidence at t1'
                  break
            elif cols[0] not in t2_mfo_dict:
                  print 'Error: selected protein ' + cols[0] + ' in ' + \
                        output_filename_NK_mfo + ' has not gained experimental \
                        evidence at t2'
                  break 
        outfile_NK_mfo_handle.close() 
        NKcount += 1
    return NKcount

def verify_LK_benchmark(t1_iea_handle,
                        t1_exp_handle,
                        t2_exp_handle,
                        output_filename_LK_bpo,
                        output_filename_LK_cco,
                        output_filename_LK_mfo):
    # Create a dictionary for the <protein, GO ID> tuples from t1_iea file:
    t1_iea_dict = create_iea_dict(t1_iea_handle)

    # Create BPO, CCO and MFO dictionaries for the 
    # <protein, GO ID> tuples from t1_exp file:
    t1_bpo_dict, t1_cco_dict, t1_mfo_dict = create_exp_dict(t1_exp_handle) 

    # Create BPO, CCO and MFO dictionaries for the 
    # <protein, GO ID> tuples from t2_exp file:
    t2_bpo_dict, t2_cco_dict, t2_mfo_dict = create_exp_dict(t2_exp_handle) 
   
    LKcount = 0
    LKcount = LKcount + verify_LK_benchmark_bpo(t1_iea_dict,
                                                t1_bpo_dict,
                                                t1_cco_dict,
                                                t1_mfo_dict,
                                                t2_bpo_dict,
                                                t2_cco_dict,
                                                t2_mfo_dict,
                                                output_filename_LK_bpo,
                                                LKcount)
    LKcount = LKcount + verify_LK_benchmark_cco(t1_iea_dict,
                                                t1_bpo_dict,
                                                t1_cco_dict,
                                                t1_mfo_dict,
                                                t2_bpo_dict,
                                                t2_cco_dict,
                                                t2_mfo_dict,
                                                output_filename_LK_cco,
                                                LKcount)
    LKcount = LKcount + verify_LK_benchmark_mfo(t1_iea_dict,
                                                t1_bpo_dict,
                                                t1_cco_dict,
                                                t1_mfo_dict,
                                                t2_bpo_dict,
                                                t2_cco_dict,
                                                t2_mfo_dict,
                                                output_filename_LK_mfo,
                                                LKcount)
    return LKcount

def verify_NK_benchmark(t1_iea_handle, 
                        t1_exp_handle, 
                        t2_exp_handle, 
                        output_filename_NK_bpo, 
                        output_filename_NK_cco, 
                        output_filename_NK_mfo):

    # Create a dictionary for the <protein, GO ID> tuples from t1_iea file:
    t1_iea_dict = create_iea_dict(t1_iea_handle)

    # Create BPO, CCO and MFO dictionaries for the 
    # <protein, GO ID> tuples from t1_exp file:
    t1_bpo_dict, t1_cco_dict, t1_mfo_dict = create_exp_dict(t1_exp_handle)

    # Create BPO, CCO and MFO dictionaries for the 
    # <protein, GO ID> tuples from t2_exp file:
    t2_bpo_dict, t2_cco_dict, t2_mfo_dict = create_exp_dict(t2_exp_handle)

    NKcount = 0
    NKcount = NKcount + verify_NK_benchmark_bpo(t1_iea_dict,
                                                t1_bpo_dict,
                                                t1_cco_dict,
                                                t1_mfo_dict,
                                                t2_bpo_dict,
                                                t2_cco_dict,
                                                t2_mfo_dict,
                                                output_filename_NK_bpo,
                                                NKcount)
    NKcount = NKcount + verify_NK_benchmark_cco(t1_iea_dict,
                                                t1_bpo_dict,
                                                t1_cco_dict,
                                                t1_mfo_dict,
                                                t2_bpo_dict,
                                                t2_cco_dict,
                                                t2_mfo_dict,
                                                output_filename_NK_cco,
                                                NKcount)
    NKcount = NKcount + verify_NK_benchmark_mfo(t1_iea_dict,
                                                t1_bpo_dict,
                                                t1_cco_dict,
                                                t1_mfo_dict,
                                                t2_bpo_dict,
                                                t2_cco_dict,
                                                t2_mfo_dict,
                                                output_filename_NK_mfo,
                                                NKcount)
    return NKcount

if __name__ == "__main__":
    print 'This script does not run independently'
    sys.exit(1)

