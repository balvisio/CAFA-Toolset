#!/usr/bin/env python

import os
import sys
import argparse
import re
from collections import defaultdict

'''
   This script parses, verifies a bunch of user input parameters using argparse
   module. Finally creates a dictionary with all parameter values and then 
   returns it.
'''

def extract_args(args):
    # This dictionary below contains the values of all arguments available to
    # the program. If they have been passed, it will take the values passed. 
    # Else, will assume default values. If a new parameter is to be added to
    # the program, it should be added into this dictionary

    args_dict = {}
    args_dict = {'g' : args.organism,
                 'outfile' : args.output,
                 't1' : args.input1,
                 }
    print ("*************************************************")
    print ("Welcome to the Target generatin tool !!!!!")
    print ("*************************************************\n")
    print ('Following is a list of user supplied inputs :\n')
    for arg in args_dict:
        print (arg + ' : ' + str(args_dict[arg]))
    print ('*********************************************\n')
    return args_dict
    
def check_args(args_dict,parser):
    # This method checks the values for each of the arguments provided to look 
    # for inconsistent input. At the end, it creates a final dictionary of 
    # input argument values and gives it back to the main script

    user_dict = {}
    for arg in args_dict:
        if arg == 't1':
            if args_dict[arg] == None:
                print ('Missing T1 file\n')
                print (parser.parse_args(['--help']))
            else:
                user_dict['t1'] = args_dict[arg]

        elif arg == 'g': 
            if args_dict[arg] == None: 
                print('Missing organism id\n')
                print (parser.parse_args(['--help']))
            else: 
                user_dict['g'] = args_dict[arg]
  
        elif arg == 'outfile':
            user_dict[arg] = args_dict[arg]
            
        elif arg == 'Taxon_ID':
            if 'all' in args_dict[arg] or len(args_dict[arg]) == 0:
                user_dict[arg] = set([])
            else:
                args_dict[arg] = [x.capitalize() for x in args_dict[arg]]
                user_dict[arg] = set(args_dict[arg])
        else:
            if 'all' in args_dict[arg] or len(args_dict[arg]) == 0:
                user_dict[arg] = set([])
            else:
                args_dict[arg] = [x.upper() for x in args_dict[arg]]
                user_dict[arg] = set(args_dict[arg])
    return user_dict

def parse(parser, ConfigParam=defaultdict()):
    args_dict = {}
    args, unknown = parser.parse_known_args()

    if len(unknown) > 0:
        print ('\n*********************************')
        print ("Invalid Arguments")
        print ('*********************************\n')
        print (parser.parse_args(['--help']))
    args_dict = extract_args(args)
    user_dict = check_args(args_dict,parser)
    return user_dict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='bm.py',description='Creates a set of \
        benchmark proteins')
    parser.add_argument('-G','--organism', help='This option is mandatory.\
        Specifies an organism id, for example, 559292 for Saccharomyces \
        cerevisiae.')
    parser.add_argument('-I1', '--input1', nargs='*', help='This opton is \
        mandatory. Specifies path to the first input file.')
    parser.add_argument('-O', '--output', nargs='*',default=[], help='Optional \
        argument.Provides user an option to specify an output filename.')
    parse(parser, ConfigParam=defaultdict())

    
