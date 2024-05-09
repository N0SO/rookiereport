#!/usr/bin/env python3
import os.path
import sys

whereami = os.path.split( os.path.realpath(__file__) )
pathsplit = os.path.split(whereami[0])
#print("here I am :", whereami, pathsplit)

DEVMODPATH = [pathsplit[0],
              '/home/pi/Projects', 
              '/home/pi/Projects/moqputils',
              '/home/pi/Projects/cabrillolog']
#print('Using DEVMODPATH=',DEVMODPATH)
#os.chdir(pathsplit[0])

for mypath in DEVMODPATH:
        if ( os.path.exists(mypath) and \
          (os.path.isfile(mypath) == False) ):
            sys.path.insert(0, mypath)

import argparse
from reverselog.__init__ import VERSION

USAGE = \
"""
mqprookie
"""

DESCRIPTION = \
"""
Extract a summary of ROOKIE activity from the database. The submitted
log must have 'ROOKIE' in the log header CATEGORY-OVERLAY: field.
"""

EPILOG = \
"""
That is all!
"""

def parseMyArgs():
    parser = argparse.ArgumentParser(\
                    description = DESCRIPTION, usage = USAGE)
    parser.add_argument('-v', '--version', 
                        action='version', 
                        version = VERSION)
    
    parser.add_argument('-l', '--location',
                                   choices = ['all','mo','non-mo'],
                                   default='all',
            help="""Filter results: all - All rookies, 
                                    mo  - Missouri rookies,
                                    non-mo - Non-Missouri rookies
                    Default is all rookies.""")

    parser.add_argument('-t', '--reportType',
                                   choices = ['csv', 'html'],
                                   default = 'csv',
            help="""Set report type for output. Options are: 
                         csv (Comma Separated Variables) or 
                         html for web page use. 
                    Default value is cab""")


    args = parser.parse_args()
    return args
    
    
if __name__ == '__main__':
    args = parseMyArgs()
    if args.location:
        from rookiereport.rookiereport import rookieReport
        app = rookieReport(args)

