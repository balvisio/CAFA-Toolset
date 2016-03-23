#!/usr/bin/env python

import os
import sys
import argparse
import re
from collections import OrderedDict

'''
   Th methods in this module collect user supplied arguments, parses and 
   verifies them. The entry point to these chain of actions is parse_args 
   method. Description of these methods are following:   
   
   collect_args: This method collect the user supplied arguments.  
   extract_args: This method puts the user supplied arguments into an 
        ordered dictionary. 
   check_args: This method verifies the correctness of the user supplied
       arguments and puts them into an ordered dictionary and returns it. 
   parse_args: This method calls the above methods and returns the final 
      dictionary with user supplied arguments.
'''

def collect_args():
    # This method collects the user supplied arguments 
    # and returns them at the end.
    parser = argparse.ArgumentParser(description='Generate a set of target \
        sequences for a specific organism by filtering them out fro a \
        UniProt-SwissProt file.')
    parser.add_argument('-I1', '--input1', help=' Specifies path to a \
        UniProt-SwissProt file. This opton is mandatory.')
    parser.add_argument('-G','--organism', help=' Specifies an organism id, \
        for example, 559292 for Saccharomyces cerevisiae. This opton is \
        mandatory.')
    parser.add_argument('-O', '--output', default='', help='Provides user an\
        option to specify an output filename prefix. When not specified, \
        the program will create an output file name.')
    return parser

def extract_args(args):
    # This method builds a dicitonary from the user supplied arguments
    # and returns the constructed dictionary at the end.
    args_dict = OrderedDict() 
    args_dict['t1'] = args.input1
    args_dict['outfile'] = args.output
    args_dict['g'] = args.organism
    return args_dict
    
def check_args(args_dict,parser):
    # This method checks the user arguments for consistency.
    # It builds a new dictionary from these arguments and 
    # finally returns this newly created dictionary 

    user_dict = OrderedDict() 
    for arg in args_dict:
        if arg == 't1':
            if args_dict[arg] == None:
                print ('Missing Uniprot-SwissProt file\n')
                print (parser.parse_args(['--help']))
            else:
                user_dict['t1'] = args_dict[arg]
        elif arg == 'outfile':
            user_dict[arg] = args_dict[arg]
        elif arg == 'g':
            if args_dict[arg] == None: 
                print('Missing organism id\n')
                print (parser.parse_args(['--help']))
            else:
                user_dict['g'] = args_dict[arg]
        elif arg == 'Taxon_ID':
            if 'all' in args_dict[arg] or len(args_dict[arg]) == 0:
                user_dict[arg] = set([])
            else:
                args_dict[arg] = [x.capitalize() for x in args_dict[arg]]
                user_dict[arg] = set(args_dict[arg])
    return user_dict

def parse_args():
    # This is the entry point for the other methods in this module:
    # 1. it invokes collect_args to collect user arguments
    # 2. it puts those arguments into a dictionary by calling extract_args method
    # 3. it checks the consistency of those arguments by invoking check_args which
    #    returns an dictionary of correct arguments
    # 4. Finally, it returns the dictionary at the end.

    parser = collect_args() # Collect user arguments
    args_dict = {}
    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print ('\n*********************************')
        print ("Invalid Arguments")
        print ('*********************************\n')
        print (parser.parse_args(['--help']))
    args_dict = extract_args(args) # Places the user arguments into a dictionary
    user_dict = check_args(args_dict,parser) # Checks the consistency of the user args
    return user_dict

if __name__ == '__main__':
    print('This program does not run independently.')
    sys.exit(1)
