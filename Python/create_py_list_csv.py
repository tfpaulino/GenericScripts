#!/usr/bin/env python
# -*- Mode: Python; indent-tabs-mode: nil; tab-width: 4 -*-
# Date: 2017.07.03
# Author: Luis Cardoso
# Description: Create a list using the header information of all scripts and
#              export to a CSV file.
# Modified by: Luis Cardoso
# Version: 0.1

import os
import sys
import time
import csv

################################################################################
# Global Constants
################################################################################

TIME_DAY_IN_SECONDS = 24*60*60  # 1d => 24h
TIME_HOUR_IN_SECONDS = 60*60    # 1h => 60m
TIME_MINUTE_IN_SECONDS = 60     # 1m => 60s

################################################################################
# Definitions
################################################################################

def printMessage(title='Dummy Title', message='Dummy message!', error_status=0):
    """Print general messages to console, and if used as error parser, this will
    terminate after printing."""
    print '\n%s:' % title.title()
    print message
    # Check error status and exit if the error is greater than 0
    # Obs.: 0 means success
    if error_status > 0:
        sys.exit(error_status)
    print 80*'-'

def convertSeconds2Time(seconds=0):
    """Convert a value in seconds to a tuple with values for days, hours,
    minutes and seconds. This can be used to write the time spent on some task,
    without the need to make extra manual calculation."""
    seconds = int(seconds)
    processed = 0

    days = (seconds - processed) / TIME_DAY_IN_SECONDS
    processed = days * TIME_DAY_IN_SECONDS

    hours = (seconds - processed) / TIME_HOUR_IN_SECONDS
    processed += hours * TIME_HOUR_IN_SECONDS

    minutes = (seconds - processed) / TIME_MINUTE_IN_SECONDS
    processed += minutes * TIME_MINUTE_IN_SECONDS

    seconds = seconds - processed

    return (days, hours, minutes, seconds)

def main():
    """Collect the data from the list of files and stores on CSV file."""
    result_row = []
    argv_len = len(sys.argv)
    main_csv_path = ""
    main_start_time = time.time()
    main_start_time_tuple = time.localtime(main_start_time)
    main_start_time_string = time.strftime("%Y-%m-%d_%H-%M-%S", main_start_time_tuple)
    main_stop_time = 0

    if argv_len > 0:
        # Grab the absolute path from this file
        main_csv_path = os.path.abspath(sys.argv[0])
        # Filter the absolute to retain only the directory path
        main_csv_path = os.path.dirname(main_csv_path)
        # Join the CSV filename to the previous directory path
        # Note: The filename will have the date and time.
        main_csv_path = os.path.join(main_csv_path, "py_list_%s.csv" % main_start_time_string)
        print "The results will be present in:\n\"%s\"" % main_csv_path

        # Try to open the CSV file in Write Binary format
        try:
            csvfile = open(main_csv_path, 'wb')
        except:
            e = sys.exc_info()
            printMessage('File IO', '\n'.join(e), 0x11)

        # Create an handler with the specified properties
        main_csv_writer = csv.writer(csvfile, delimiter = ',', quotechar = '"')

        # Write the first row as a header for the values bellow
        #result_row = ['Scenario', 'Auteur', 'Description', 'Modified by', 'Version', 'Requirement', 'Table']
        result_row = ['Scenario', 'Auteur', 'Description', 'Modified by', 'Version', 'Path']
        main_csv_writer.writerow(result_row)

        # Verifica os ficheiros como argumento a este script
        for argv_param in range(1, argv_len):
            filename = sys.argv[argv_param]
            commentaire_id = 0
            # Grab the absolute path from this file
            filename_absolute = os.path.abspath(filename)
            path_absolute = filename_absolute
            # If the given path point to a file, filter its directory path
            if os.path.isfile(filename_absolute):
                path_absolute = os.path.dirname(filename_absolute)

            # Setting the patterns to be used to detect the appropriate files
            f_pattern_1 = 'scenario_'
            f_pat_len_1 = len(f_pattern_1)
            f_pattern_2 = '.py'
            f_pat_len_2 = len(f_pattern_2)

            # Recursively walk every directory and collect all files to be used
            # as module, in order to get the required information
            for rl, dl, fl in os.walk(path_absolute):
                # Add the actual path as Python Lib path, in order to be able to
                # import the Python file as module
                sys.path.append(rl)
                for f in fl:
                    f_len = 0
                    f_pos_1 = 0
                    f_pos_2 = 0
                    f_len = len(f)
                    # Check if the file has the required patterns, storing the
                    # position found (remember, -1 means not found)
                    f_pos_1 = f.lower().find(f_pattern_1)
                    f_pos_2 = f.lower().find(f_pattern_2)

                    # Check if the positions found are in the required positions
                    if f_pos_1 == 0 and f_pos_2 > 0 and (f_len - f_pat_len_2 == f_pos_2):
                        # Grab the filename without the extension
                        f_module = f[0:f_pos_2]
                        
                        # Import the module and grab the required constants and
                        # stores the data as a new row on CSV file
                        #_temp = __import__(f_module, globals(), locals(), ['Auteur', 'Description', 'Modifiedby', 'Version', 'Requirement', 'Table'])
                        #result_row = [f_module, _temp.Auteur, _temp.Description, _temp.Modifiedby, _temp.Version, _temp.Requirement, _temp.Table]
                        _temp = __import__(f_module, globals(), locals(), ['Auteur', 'Description', 'Modifiedby', 'Version'])
                        result_row = [f_module, _temp.Auteur, _temp.Description, _temp.Modifiedby, _temp.Version, rl]
                        main_csv_writer.writerow(result_row)
        # Close the file and checks if it is really closed
        csvfile.close()
        if not csvfile.closed:
            printMessage('File IO', 'I can\'t close "%s".' % main_csv_path, 0x12)

    main_stop_time = time.time()                  
    print 80*'#'
    print "# Total time spent: %dd %dh %dm %ds" % (convertSeconds2Time(main_stop_time - main_start_time))
    print 80*'#'

if __name__ == '__main__':
    main()
