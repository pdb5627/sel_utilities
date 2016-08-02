#! /usr/bin/env python

"""List2Digitals.py
USAGE:  List2Digitals.py <FILENAME>
where <FILENAME> is a list of Event Report Digitals Word Bits.  Each Word Bit
should be on its own line.  The list is converted to settings in a format
suitable for import into AcSELerator.  The output is printed to the screen
but can be saved to a file by redirecting output (using > on the command line).
"""

from __future__ import print_function, unicode_literals
import sys

if len(sys.argv) == 1:
    print "ERROR:  Please include a filename when calling this program."
    print "(Example Usage:  %s \"WBList.txt\")" % sys.argv[0]
    print "\nIf you passed in a filename but still received this error, \
the problem may be Windows calling the Python program without arguments."
    sys.exit(1)

InFileName = sys.argv[1]

nERDG = 1
print("[R1]")
with open(InFileName) as InFile:

    WordBit = InFile.readline().strip()
    while WordBit:
        if len(WordBit) > 0:
            print('ERDG%d,"%s"' % (nERDG, WordBit))
            nERDG += 1

        WordBit = InFile.readline().strip()

ERDGMax = 800

while nERDG <= ERDGMax:
    print('ERDG%d,""' % nERDG)
    nERDG += 1
