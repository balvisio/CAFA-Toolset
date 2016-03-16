#!/usr/bin/python

import os
import sys
from collections import defaultdict
import re

'''
   Given an input file and a bunch of parameters, this module calculates
   2 things: the number of annotations per paper for every paper listed
   in the input file and the other is, calculate how many papers are
   associated with every protein annotation pair. The first helps to filter
   out high throughput papers (if required) and the second helps to identify 
   confident annotations. The assumption is annotations in more papers are
   considered confident over others.

    count_freq: This method calculates two things: (1) the number of 
    annotations per paper for every paper listed in the input file, and 
    (2) how many papers are associated with every protein annotation pair.
    It returns these two values as tuple of two dictionaries.

    paper_term_freq: It populates the paper term frequency file. Then, it 
    returns the  
'''

def count_freq(goa_handle, EEC=set([])):
#    print 'EEC: ' + str(EEC)
    paper_conf = defaultdict(lambda:defaultdict(set))
    ann_conf = defaultdict(lambda:defaultdict(set))
    for line in goa_handle:
        if line[0] == '!':
            continue
        fields = line.strip().split('\t')
        if not fields[5] == '' and re.match('^PMID', fields[5]): # Match PMID 
            paper_id = fields[5].split(':')[1] # Extract PubMed id
            if (not EEC) or (fields[6] in EEC):
                ann_conf[fields[1]][fields[4]].add(str(paper_id)) 
                    # add pubmed id as evidence to the protein, GO ID 
                    # (fields[1], fields[4]) pair
                paper_conf[paper_id][fields[4]] = 1
    return (ann_conf, paper_conf)

def paper_term_freq(params, goa_handle, ptf_handle):
    # Given an input uniprot-goa file, this method computes the number of 
    # proteins annotated in every pubmed id mentioned in the file

    ann_conf, paper_conf = count_freq(goa_handle,
                            params['Evidence'])
    print 'Populating paper-term frequency file ...'
    if len(paper_conf) > 0:
        for pubmed_id in paper_conf:
            print >> ptf_handle, pubmed_id + '\t' + str(len(paper_conf[pubmed_id]))
    paper_conf.clear()
    return ann_conf

if __name__ == '__main__':
    infile = sys.argv[1]
    paper_term = count(infile, EEC)
