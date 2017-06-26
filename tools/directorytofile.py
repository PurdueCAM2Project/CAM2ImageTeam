"""
This module can write the filenames inside of a directory to an output file.

*****************************
Command Line Usage: python directorycontents.py [RELATIVE DIR PATH] [OUTPUT FILE PATH]
Or python directorycontents.py [RELATIVE DIR PATH] [OUTPUT FILE PATH] [PREFIX]

******************************
    ** THE CAM2 PROJECT **
******************************
Authors: Caleb Tung,
Created: 6/26/2017
Preferred: Python3.x
"""

from __future__ import print_function # Force the use of Python3.x print()

import os
import sys



def dir_to_file(directory, output_filename, prefix=None):
    """
    Writes the filenames of all files in a directory into an output file.
    Can add a prefix to the filenames, otherwise directly lists the directory
    as the prefix.

    param: directory - The path to the directory that holds the targeted files
    param: output_filename - The path to the output file to write the targeted names
    param: prefix - OPTIONAL: The prefix to the filenames written in the output file

    return: None
    """
    try:
        output_f = open(output_filename, 'w+')

        # Iterates through all files in directory and writes names to output file
        for root, unused_dirs, files in os.walk(directory):
            for filename in files:
                if prefix is None: # Default behavior, just write root name as prefix
                    output_f.write(root + filename + '\n')
                else:
                    if prefix.endswith('/'): # Don't write in an extra '/' if user provided one
                        output_f.write(prefix + filename + '\n')
                    else:
                        output_f.write(prefix + '/' + filename + '\n')

        output_f.close()

    except OSError as os_err:
        print('Either could not open output_filename or failed to resolve directory.')
        print('ERROR MESSAGE:\n' + os_err)

    return

def main():
    """
    The main function, called if context is the main
    """
    num_args_no_prefix = 2 + 1
    num_args_with_prefix = 3 + 1

    help_message = """
    Writes the filenames in a directory to a single file, with the option to add
    a prefix if desired.\n
    Expects either 2 or 3 command line args:
    python directorycontents.py [DIRECTORY PATH] [OUTPUT FILE PATH]
    or python directorycontents.py [DIRECTORY PATH] [OUTPUT FILE PATH] [PREFIX]\n
    Note: [PREFIX] is the prefix you wish to attach to the filenames (e.g. 'somedir/')
    """

    num_args = len(sys.argv)

    if num_args == num_args_no_prefix:
        dir_to_file(sys.argv[1], sys.argv[2])
    elif num_args == num_args_with_prefix:
        dir_to_file(sys.argv[1], sys.argv[2], sys.argv[3])
    else:
        print(help_message)

    return

if __name__ == '__main__':
    main()
