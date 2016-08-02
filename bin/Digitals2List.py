#! /usr/bin/env python

"""Digitals2List.py
USAGE:  DigitalsList.py <FILENAME>
where <FILENAME> is the file exported from AcSELerator for an SEL-4xx relay's
Report setting group (typically named SET_R1.txt).  The Event Report Digitals
Word Bits are extracted from the settings and printed to the screen as text,
one Word Bit per line.  The Word Bit list can be saved to a file by redirecting
output (using > on the command line).
"""

from __future__ import print_function, unicode_literals
import re
import sys

if len(sys.argv) == 1:
    print("ERROR:  Please include a filename when calling this program.")
    print("(Example Usage:  %s \"SET_R1.txt\")" % sys.argv[0])
    print("\nIf you passed in a filename but still received this error, \
the problem may be Windows calling the Python program without arguments.")
    sys.exit(1)

InFileName = sys.argv[1]

SettingRegEx = re.compile(r'([A-Z]+)([0-9]+),"(.*)"')

with open(InFileName) as InFile:

    # Read in lines until Event Report Digitals settings are found
    l = InFile.readline()
    if l:
        sMatch = SettingRegEx.match(l)
    else:
        sMatch = None
    while l:
        if sMatch:
            # Print only Event Report Digital points
            if sMatch.group(1) == 'ERDG' and len(sMatch.group(3)) > 0:
                print(sMatch.group(3))

        l = InFile.readline()
        if l:
            sMatch = SettingRegEx.match(l)
        else:
            sMatch = None
