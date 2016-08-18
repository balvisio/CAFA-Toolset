#!/usr/bin/env python
'''
    This module is an extension to the GOAParser module.
    It has the following methods to facilitate the file handling
    needs specific to Benchmark program.

    parse_tax_file(tax_filename):
        This method acepts a taxonomy file, downloaded from NCBI
        and produces a mapping between taxonomy ids and taxonomy 
        names. At the end, it returns this mapping. 

    record_has_forBenchmark(inupgrec, 
                            ann_freq,
                            allowed,
                            tax_name_id_mapping,
                            EEC_default,
                            GAFFIELDS):
        This method accepts a gaf record, a dictionary of allowed field
        values and other user specified parameters.

        If any field in the record does not have an allowed value, the
        function stops search and returns false. Otherwise, the function
        returns true.

    t1_filter(t1_iter, 
              t1_iea_name, 
              t1_exp_name, 
              t2_exp_name, 
              GAFFIELDS,
              EXP_default=set([])):
        This method accepts 2 uniprot-goa files and checks to see for all
        proteins present in t2 files, if the evidence code of the proteins
        in t1 file is electronic or experimental. Accordingly, splits them
        into 2 different files and writes out the files
'''
import os
import sys
import GOAParser
from os.path import basename
from collections import defaultdict

def parse_tax_file(tax_filename):
    '''
    This method acepts a taxonomy file, downloaded from NCBI
    and produces a mapping between tax ids and tax names.
    '''
    tax_id_name_mapping = {}
    tax_file = open(tax_filename,'r')
    for tax_lines in tax_file:
        cols = tax_lines.strip().split('|')
        cols[0] = cols[0].rstrip()
        cols[1] = cols[1].lstrip()
        cols[2] = cols[2].lstrip()
        cols[3] = cols[3].lstrip()
        if cols[3].rstrip() == 'scientific name':
            tax_id_name_mapping[cols[0].rstrip()] = cols[1].rstrip()
    return tax_id_name_mapping

def record_has_forBenchmark(inupgrec, 
                            ann_freq,
                            allowed,
                            tax_name_id_mapping,
                            EEC_default,
                            GAFFIELDS):
    """
    Accepts a gaf record, a dictionary of allowed field values and other
    user specified parameters.                                                                                         
    If any field in the record does not have an allowed value, the function
    stops search and returns false. Otherwise, the function returns true.
    """
#    print allowed
#    print allowed.keys()
#    print '\n'
#    print inupgrec
#    print inupgrec.keys()
#    raise SystemExit
    retval=True
    organism = ''
    for field in allowed:
        if inupgrec['Evidence'] not in EEC_default:
            retval=False  # No EXP validation. retval set to FALSE
            break
        if field not in inupgrec: # if field is not a member of inupgrec.keys()
            if field == 'Pubmed':
                rec_set = set([])
                if type(inupgrec['DB:Reference']) is type(''):
                    rec_set = set([inupgrec['DB:Reference'].split(':')[1]])
                else:
                    for x in inupgrec['DB:Reference']:
                        if x.startswith('PMID'):
                            x = x.split(':')[1]
                            rec_set.add(x)
                if allowed[field] == 'T' and '' in rec_set:
                    retval=False
                    break
            elif field == 'Confidence':
                db_id = inupgrec['DB_Object_ID']
                go_id = inupgrec['GO_ID']
                if allowed[field] == 'T' and len(ann_freq[db_id][go_id]) < allowed['Threshold']:
#                    print 'field: ' + field
#                    print 'allowed[field]: ' + str(allowed[field])
#                    print 'db_id: ' + db_id
#                    print 'go_id: ' + go_id
#                    print "ann_freq[db_id][go_id]: " + str(ann_freq[db_id][go_id])
#                    print "allowed['Threshold']: " + str(allowed['Threshold'])
#                    print "allowed['Pubmed']: " + str(allowed['Pubmed'])
#                    print "allowed['Blacklist']: " + str (allowed['Blacklist'])
#                    raise SystemExit
                    retval=False
                    break
            elif field == 'Blacklist':
                rec_set = set([])
                if type(inupgrec['DB:Reference']) is type(''):
                    rec_set = set([inupgrec['DB:Reference'].split(':')[1]])
                else:
                    for x in inupgrec['DB:Reference']:
                        if x.startswith('PMID'):
                            x = x.split(':')[1]
                            rec_set.add(x)
                if len(rec_set & allowed[field]) > 0: # What exactly happening here?????????????????? 
                     retval=False
                     break
            else:
                continue

            continue

        if len(allowed[field]) == 0: # Checks whether field is an empty string or empty list
            continue

        if field == 'Taxon_ID': #  
            if type(inupgrec[field]) is type(''): # only one taxon id
                rec_set =set([inupgrec[field]]) # assign an empty set
            else: # a list of taxon ids
                rec_set = set(inupgrec[field]) # assing a set with the list of taxon ids
            for rec in rec_set:
                if rec.split(':')[1] in tax_name_id_mapping: # taxon id is in the tax_name_id_mapping?
                    organism = tax_name_id_mapping[rec.split(':')[1]] # get the organism id from the mapping
                if organism in allowed[field] or rec.split(':')[1] in allowed[field]: # checking by organism id or organism name
                    retval=True
                    break
                else:
                    retval=False
            if not retval:
                break
        else: #  
            if inupgrec[field] not in allowed[field]:
                retval=False
                break        
    return retval  

def t1_filter(t1_iter, 
              t1_iea_name, 
              t1_exp_name, 
              t2_exp_name, 
              GAFFIELDS,
              EXP_default=set([])):
    '''
    This method accepts 2 uniprot-goa files and checks to see for all
    proteins present in t2 files, if the evidence code of the proteins
    in t1 file is electronic or experimental. Accordingly, splits them
    into 2 different files and writes out the files
    '''
    t2_exp_handle = open(t2_exp_name, 'r')
    
    exp_pid_dict = defaultdict(lambda:defaultdict())

    for inline in t2_exp_handle:
        inrec = inline.strip('\n').split('\t')
        if len(inrec) < 15:
            continue
        exp_pid_dict[inrec[1]][inrec[8]] = 1
    t2_exp_handle.close()

    t1_iea_handle = open(t1_iea_name, "w")
    t1_exp_handle = open(t1_exp_name, "w")

    for rec in t1_iter:
        if exp_pid_dict.has_key(rec['DB_Object_ID']):
            if exp_pid_dict[rec['DB_Object_ID']].has_key(rec['Aspect']):
                if not rec['Evidence'] in EXP_default:
                    GOAParser.writerec(rec, t1_iea_handle,GAFFIELDS)
                elif rec['Evidence'] in EXP_default:
                    GOAParser.writerec(rec, t1_exp_handle, GAFFIELDS)
    t1_iea_handle.close()
    t1_exp_handle.close()
    exp_pid_dict.clear()

if __name__ == '__main__': 
    print (sys.argv[0] + ':')
    print(__doc__)
    sys.exit(0)

