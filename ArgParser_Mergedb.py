#!/usr/bin/env python

'''
    The entry point of this module is parse_args() method which calls other
    methods to collect user supplied arguments, parses and verifies them 
    and at the end returns those arguments as a dictionary. Description of 
    these methods are following:   
   
    parse_args:
       This method calls the methods below and returns the final dictionary
       containing the user supplied arguments.

    collect_args:
        This method collects the user supplied arguments and returns them 
        as an argparse.ArgumentParser object.

    extract_args: 
        This method puts the user supplied arguments into an ordered 
        dictionary which it returns at the end.

    check_args: 
        This method verifies the correctness of the user supplied arguments 
        and puts them into an ordered dictionary which it returns at the 
        end. 
'''

import os
import sys
import argparse
import re
from collections import OrderedDict


def collect_args():
    """
    This method collects the user supplied arguments and returns them 
    at the end.
    """

    parser = argparse.ArgumentParser(description='Merges UniProtKB/' + \
                    'SwissProt and UniProt-GOA files for some ' + \
                    'specific organism.')
    parser.add_argument('-I1', '--input1', help='Specifies path to ' +  \
                    'a UniProt/Swissprot file. This opton is mandatory.')
    parser.add_argument('-I2', '--input2', help='Specifies path to a ' + \
                    'UniProt-GOA file. This option is mandatory.')
    parser.add_argument('-G','--organism', help='Specifies an organism id,' + \
                    'for example, 559292 for Saccharomyces cerevisiae. ' + \
                    'This opton is mandatory.')
    parser.add_argument('-O', '--output', default='', help='Provides user ' + \
                    'an option to specify an output filename prefix. When ' + \
                    'not specified, the program will create an output ' + \
                    'file name.')
    return parser

def extract_args(args):
    """
    This method builds a dicitonary from the user supplied arguments
    and returns the constructed dictionary at the end.
    """

    args_dict = OrderedDict()
    args_dict['t1'] = args.input1
    args_dict['t2'] = args.input2
    args_dict['outfile'] = args.output
    args_dict['g'] = args.organism
    return args_dict
    
def check_args(args_dict, parser):
    """
    This method checks the user arguments for consistency. It builds a new
    dictionary from these arguments and finally returns this newly created 
    dictionary.
    """

    user_dict = OrderedDict() 
    for arg in args_dict:
        if arg == 't1':
            if args_dict[arg] == None:
                print ('Missing Uniprot-SwissProt file\n')
                print (parser.parse_args(['--help']))
            else:
                user_dict['t1'] = args_dict[arg]
        elif arg == 't2':
            if args_dict[arg] == None:
                print ('Missing Uniprot-GOA file\n')
                print (parser.parse_args(['--help']))
            else:
                user_dict['t2'] = args_dict[arg]
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
    """
    This is the entry point for the other methods in this module. It
      1. invokes collect_args to collect user arguments.
      2. invokes extract_args() method to put those arguments into 
         an ordered dictionary which it returns at the end.
      3. invokeds check_args to check the consistency of those 
         arguments and returns the dictionary of the correct arguments.
      4. returns the dictionary at the end.
    """
    # Collect user arguments:
    parser = collect_args() 
    args_dict = {}
    args, unknown = parser.parse_known_args()
    if len(unknown) > 0:
        print ('\n*********************************')
        print ("Invalid Arguments")
        print ('*********************************\n')
        print (parser.parse_args(['--help']))
    # Places the user arguments into a dictionary:
    args_dict = extract_args(args) 
    # Checks the consistency of the user args:
    user_dict = check_args(args_dict,parser) 
    return user_dict

if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print (__doc__)
    sys.exit(0)
