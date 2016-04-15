#!/usr/bin/env python

'''
    This module has the following two methods:

    read_config: 
        This method tries to locate the configuration file in 
        the current directory or any of the subdirectories. If 
        it does not find the configuration file, it creates one
        by invoking create_config. At the end, it returns the
        content of the configuration file as an ordered dictionary.

    create_config: 
        This method creates a configureation file which is passed 
        as an argument. This file stores the configuration:

        DEFAULT_PATH: the default workspace
        HOSTNAME: ftp.ebi.ac.uk
        CURRENT_FILE_PATH: file path for current GOA release
        OLD_FILE_PATH: file path for old GOA releases
        EXP_EVIDENCE_CODES: the set of GO annotation exeperimental 
                            evidence codes
        ONTOLOGIES: the thre ontology names
        TAXONOMOY_FILENAME: the file name for taxonomy definitions
        BASE_URL: www.uniprot.org/uniprot
        FTP_DATE: regular expression for ftp dates
        FTP_FILE_START: gene_association
'''

import os
import sys
import re
import ConfigParser as cp
from collections import OrderedDict

def create_config(config_filename):
    outfile_handle = open(config_filename, 'w')
    outfile_handle.write('[WORKDIR]\n')
    work_dir_response = raw_input('Provide a path to your working directory (If left blank, defaults  to current directory) : ')
    if work_dir_response == '':
        outfile_handle.write('DEFAULT_PATH : .\n') 
    elif work_dir_response.startswith('.') or work_dir_response.startswith('/'):
        outfile_handle.write('DEFAULT_PATH : ' + work_dir_response + '\n')
    else:
        outfile_handle.write('DEFAULT_PATH : ' + './' + work_dir_response + '\n')
        
    outfile_handle.write('\n')

    outfile_handle.write('[FTP]\n')
    outfile_handle.write('HOSTNAME : ftp.ebi.ac.uk\n')
    outfile_handle.write('CURRENT_FILE_PATH : /pub/databases/GO/goa/UNIPROT\n')
    outfile_handle.write('OLD_FILE_PATH : /pub/databases/GO/goa/old/UNIPROT\n')
    outfile_handle.write('\n')
    
    outfile_handle.write('[DEFAULTS]\n')
    outfile_handle.write('EXP_EVIDENCE_CODES : ' + str(set(['EXP','IDA','IPI','IMP','IGI','IEP'])) + '\n')
    outfile_handle.write('ONTOLOGIES : ' + str(set(['F','P','C'])) + '\n')
    outfile_handle.write('TAXONOMY_FILENAME : names.dmp\n')
    
    outfile_handle.write('\n')

    outfile_handle.write('[SEQUENCE]\n')
    outfile_handle.write('BASE_URL : www.uniprot.org/uniprot/\n')

    outfile_handle.write('\n')

    outfile_handle.write('[REGEX]\n')
    outfile_handle.write('FTP_DATE : [a-zA-Z]+\_\d+\n')
    outfile_handle.write('FTP_FILE_START : gene_association\n')

def read_config(config_filename):
    """
    This method reads the conig file supplied by config_filename and returns
    the configuration as an ordered dictionary
    If the config file is not found in the current direcotry or
    any subdirectory, it creates one by invoking create_config method
    """

    fname_ind = 0
    # Search for configuration file. 
    # current directory -> workspace -> create one 
    for root,dirs,files in os.walk('.'):
        for fname in files:
            if fname == config_filename:
                fname_ind = 1
        if fname_ind == 0:
            print 'Configuration file not found'
            print 'Creating new configuration file ...'
            print '************************************'
            create_config(config_filename) # Creates a configuration file
        break
    # Reads the config file and stores values in a dictionary
    Config_handle = cp.ConfigParser()
    Config_handle.read(config_filename)
    ConfigParam = OrderedDict()
    ConfigParam['workdir'] = Config_handle.get('WORKDIR', 'DEFAULT_PATH')
    ConfigParam['ftp_host'] = Config_handle.get('FTP', 'HOSTNAME')
    ConfigParam['ftp_curr_path'] = Config_handle.get('FTP', 'CURRENT_FILE_PATH')
    ConfigParam['ftp_old_path'] = Config_handle.get('FTP', 'OLD_FILE_PATH')
    ConfigParam['exp_eec'] = Config_handle.get('DEFAULTS', 'EXP_EVIDENCE_CODES')
    ConfigParam['ont_def'] = Config_handle.get('DEFAULTS', 'ONTOLOGIES')
    ConfigParam['tax_file'] = Config_handle.get('DEFAULTS', 'TAXONOMY_FILENAME')
    ConfigParam['uniprot_path'] = Config_handle.get('SEQUENCE', 'BASE_URL')
    ConfigParam['ftp_date'] = Config_handle.get('REGEX', 'FTP_DATE')
    ConfigParam['ftp_file_start'] = Config_handle.get('REGEX', 'FTP_FILE_START')
    return ConfigParam

if __name__ == '__main__':
    print (sys.argv[0] + ':')
    print (__doc__)
    sys.exit(0)
