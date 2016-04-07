#!/usr/bin/env python

'''
   The entry point of this script is parse_args() method which calls
   other methods to collect user supplied arguments, parses and
   verifies them, and at the end returns those arguments as a dictionary.
   Description of these methods are the following:
   
   collect_args: 
       This method collects the user supplied arguments.

   extract_args:
       This method puts the user supplied arguments into an ordered
       dictionary which it returns at the end.

   check_args:
       This method verifies the correctness of the user supplied
       arguments and puts them into an ordered dictionary and returns at 
       the end. 

   parse_args:
      This method calls the above methods and returns the final dictionary
      containing the user supplied arguments.
'''

import os
import sys
import argparse
import re
from collections import OrderedDict

def collect_args():
    """ 
    This method collects the user supplied arguments and returns 
    them at the end.
    """
    parser = argparse.ArgumentParser(description='Runs the Filter program ' + \
             'on a set of UniProtKB/SwissProt annotation files.')
    parser.add_argument('-I', '--input1', help='Specifies path to a ' + \
             'file listing UniProtKB/SwissProt file names. This ' + \
             'option is mandatory.')
    parser.add_argument('-O', '--output1', help='Specifies path to a ' + \
             'file to write messages from running the Filter program. ' + \
             'This option is mandatory.')
    return parser

def extract_args(args):
    """
    This method builds a dicitonary from the user supplied arguments
    and returns the constructed dictionary at the end.
    """
    args_dict = OrderedDict()
    args_dict['input1'] = args.input1
    args_dict['output1'] = args.output1
    return args_dict
    
def check_args(args_dict, parser):
    """ 
    This method checks the consistency of user arguments. It builds a new
    dictionary of the input arguments and returns the created dictionary
    at the end.
    """
    user_dict = OrderedDict()
    for arg in args_dict:
        if arg == 'input1':
            if args_dict[arg] == None:
                print 'Missing file listing data sets\n'
                print parser.parse_args(['--help'])
            else:
                user_dict['input1'] = args_dict[arg]
        elif arg == 'output1':
            if args_dict[arg] == None:
                print 'Missing file to write messages\n'
                print parser.parse_args(['--help'])
            else:
                user_dict['output1'] = args_dict[arg]
    return user_dict

def parse_args():
    """ 
    This is the entry point for the other methods in this module:
       1. it invokes collect_args to collect user arguments
       2. it puts those arguments into a dictionary by calling extract_args method
       3. it checks the consistency of those arguments by invoking check_args which
          returns an dictionary of correct arguments
       4. Finally, it returns the dictionary at the end.
    """
    parser = collect_args() # Collect user arguments
    args_dict = {}
    args, unknown = parser.parse_known_args()

    if len(unknown) > 0:
        print '\n*********************************'
        print "Invalid Arguments"
        print '*********************************\n'
        print parser.parse_args(['--help']) # Shows help messages and quits
    args_dict = extract_args(args)
    user_dict = check_args(args_dict, parser)
    return user_dict

if __name__ == '__main__':
    print (sys.argv[0] + ' docstring:')
    print (__doc__)
    sys.exit(0) 
