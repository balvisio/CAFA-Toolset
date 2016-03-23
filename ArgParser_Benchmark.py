#!/usr/bin/env python

import os
import sys
import argparse
import re
from collections import OrderedDict

'''
   Th methods in this module collect user supplied arguments, parses and 
   verifies them. The entry point of these chain of actions is parse_args 
   method. Description of these methods are following:
   
   collect_args: This method collect the user supplied arguments.  
   extract_args: This method puts the user supplied arguments into an 
        ordered dictionary. 
   check_args: This method verifies the correctness of the user supplied
       arguments and puts them into an ordered dictionary and returns it. 
   parse_args: This method calls the above methods and returns the final 
      dictionary with user supplied arguments.
'''

def collect_args(prog='benchmark'):
    # Argument list:
    parser = argparse.ArgumentParser(description='Creates benchmark protein sets \
                    from two annotation files at two time points')
    parser.add_argument('-I1', '--input1', help='This opton is mandatory. \
                    Specifies path to the first input file.')
    parser.add_argument('-I2', '--input2', help='This option is mandatory. \
                    Specifies path to the second input file.')
    if prog == 'benchmark':
        parser.add_argument('-O', '--output', default='', help='Provides user an \
            option to specify an output filename.')
    elif prog == 'verify':
        parser.add_argument('-I3', '--input3', default='', help='Provides user an \
            option to specify any of the benchmark files that need to be verified.')

    parser.add_argument('-G','--organism',nargs='*', default=['all'],help='Provides \
                    user a choice to specify a set of organisms  \
                    (example:Saccharomyces cerevisiae or 7227) separated by \
                    space. Default is all.')
    parser.add_argument('-N','--ontology',nargs='*', default=['all'],help='Provides \
                    user a choice to specify a set of ontologies (F, P, C) \
                    separated by space. Default is all.')
    parser.add_argument('-V','--evidence',nargs='*', default=['all'],help='Provides \
                    user a choice to specify a set of GO experimental evidence \
                    codes (example: IPI, IDA, EXP) separated by space. Default \
                    is all.')
    parser.add_argument('-S', '--source',action='store', nargs='*',default=\
                    ['all'],help='Provides user a choice to specify sources \
                    (example: UniProt, InterPro) separated by spaces. Default \
                    is all.')
    parser.add_argument('-C', '--confidence',default='F',help='Allows user to turn \
                    on the annotation confidence filter. If turned on, GO \
                    terms assignments to proteins that are documented in few \
                    papers (4 or less by default) will not be considered part \
                    of the benchmark set. By default, it is turned off.')
    parser.add_argument('-T', '--threshold',type=int, default=4,help='Allows \
                    users to specify a threshold for the minimum number of \
                    papers to be used for having a confident annotation. If \
                    not specified, defaults to a value of 4.')
    parser.add_argument('-P', '--pubmed',default='F',help='Allows user to turn on \
                    the pubmed filter. If turned on, GO terms w/o any Pubmed \
                    references will not be considered part of the benchmark \
                    set. By default, it is turned off.')
    parser.add_argument('-B', '--blacklist', nargs='*',default=[], help='This \
                    parameter can take in a list of pubmed ids. All GO \
                    terms and proteins annotated in them will be eliminated \
                    from the benchmark set. Default is an empty list.')
    return parser

def extract_args(args, prog):
    # This dictionary bellow places the user supplied arguments to the dictionary keys.
    # If no argument is supplied by the user, the key is assigned with the default value.
    
    args_dict = OrderedDict() 
    args_dict['t1'] = args.input1
    args_dict['t2'] = args.input2
    if prog == 'benchmark':
        args_dict['outfile'] = args.output # Default: ''
    elif prog == 'verify': 
        args_dict['t3'] = args.input3
    args_dict['Taxon_ID'] = args.organism # Default: 'all'
    args_dict['Aspect'] = args.ontology # Default: 'all'
    args_dict['Evidence'] = args.evidence # Default: 'all'   
    args_dict['Assigned_By'] = args.source # Default is 'all' 
    args_dict['Confidence'] = args.confidence # Default: 'F'
    args_dict['Threshold'] = args.threshold # Default: 4
    args_dict['Pubmed'] = args.pubmed # Default: 'F' 
    args_dict['Blacklist'] = args.blacklist # Default: [] 
    return args_dict
    
def check_args(args_dict, parser):
    # This method checks the consistency of user arguments.
    # It creates a dictionary of input arguments and returns 
    # the created dictionary.
    user_dict = OrderedDict() 
    for arg in args_dict:
        if arg == 't1':
            if args_dict[arg] == None:
                print 'Missing input file at time t1\n'
                print parser.parse_args(['--help'])
            else:
                user_dict['t1'] = args_dict[arg]
        elif arg == 't2':
            if args_dict[arg] == None:
                print 'Missing input file at time t2\n'
                print parser.parse_args(['--help'])
            else:
                user_dict['t2'] = args_dict[arg]
        elif arg == 't3':
                user_dict['t3'] = args_dict[arg]
        elif arg == 'outfile':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Threshold':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Confidence':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Pubmed':
            user_dict[arg] = args_dict[arg]
        elif arg == 'Taxon_ID':
            if 'all' in args_dict[arg] or len(args_dict[arg]) == 0:
                user_dict[arg] = set([]) 
            else:
                args_dict[arg] = [x.capitalize() for x in args_dict[arg]]
                user_dict[arg] = set(args_dict[arg])
        else: # Aspect, Evidence, Assigned_By, Blacklist
            if 'all' in args_dict[arg] or len(args_dict[arg]) == 0:
                user_dict[arg] = set([])
            else:
                args_dict[arg] = [x.upper() for x in args_dict[arg]]
                user_dict[arg] = set(args_dict[arg])
    return user_dict

def parse_args(prog='benchmark'):
    parser = collect_args(prog) # Collect user supplied argument values
    args_dict = {}
    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print '\n*********************************'
        print "Invalid Arguments"
        print '*********************************\n'
        print parser.parse_args(['--help']) # Shows help messages and quits
    args_dict = extract_args(args, prog)
    user_dict = check_args(args_dict, parser)
    return user_dict

if __name__ == '__main__':
    print ('This program does not run independently.') 
    sys.exit(1) 
