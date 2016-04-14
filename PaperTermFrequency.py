#!/usr/bin/python
'''
    This module has the following two methods: 

    count_freq(goa_handle, EEC=set([])):
        This method calculates two things: 
        (1) the number of annotations per paper for every paper listed in 
            the input file, and 
        (2) how many papers are associated with every protein annotation 
            pair.
        It returns these two values as tuple.

    paper_term_freq(goa_handle, ptf_handle, params):
        It populates the paper term frequency file. Then, it returns the
        dictionary containing the pair of the protein annotation
        (protein name, GO ID) and number of papers supporting it.
'''
import os
import sys
from collections import defaultdict
import re

def count_freq(goa_handle, EEC=set([])):
    paper_conf = defaultdict(lambda:defaultdict(set))
    ann_conf = defaultdict(lambda:defaultdict(set))
    for line in goa_handle:
        if line[0] == '!':
            continue
        fields = line.strip().split('\t')
        if not fields[5] == '' and re.match('^PMID', fields[5]): # Match PMID 
            pubmed_id = fields[5].split(':')[1] # Extract PubMed id
            if (not EEC) or (fields[6] in EEC):
                ann_conf[fields[1]][fields[4]].add(str(pubmed_id)) 
                    # add pubmed id as evidence to the protein, GO ID 
                    # (fields[1], fields[4]) pair
                paper_conf[pubmed_id][fields[4]] = 1
    return (ann_conf, paper_conf)

def paper_term_freq(goa_handle, ptf_handle, params):
    """
     Given an input uniprot-goa file, this method populates file 
     pointed by ptf_handle with a pair of pubmed id and the number 
     of proteins annotated by that pubmed id.
    """
    ann_conf, paper_conf = count_freq(goa_handle,
                            params['Evidence'])
    print 'Populating paper-term frequency file ...'
    if len(paper_conf) > 0:
        for pubmed_id in paper_conf:
            print >> ptf_handle, pubmed_id + '\t' + str(len(paper_conf[pubmed_id]))
    paper_conf.clear()
    return ann_conf

if __name__ == '__main__':
    if len(sys.argv) ==1:
        print(sys.argv[0] + ':')
        print(__doc__)
    else:
        goa_file = sys.argv[1] # input file in GOA format
        ptf_file = sys.argv[2] # output file for paper term frequency
        paper_term_freq(open(sys.argv[1], 'r'), 
                        open(sys.argv[2], 'w'), set())
        # Create a paper term frequency file from the input goa file
    sys.exit(0)
