#! /usr/bin/env python

"""List2SER.py
USAGE:  List2SEr.py <FILENAME>
where <FILENAME> is a list of SER Word Bits.  Each Word Bit should be on its own
line.  The list is converted to settings in a format suitable for import into
AcSELerator.  The output is printed to the screen but can be saved to a file
by redirecting output (using > on the command line).
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

nSER = 1
print("[R1]")
with open(InFileName) as InFile:

    WordBit = InFile.readline().strip()
    while WordBit:
        if len(WordBit) > 0:
            print('SITM%d,"%s"' % (nSER, WordBit))
            print('SNAME%d,"%s"' % (nSER, WordBit))
            print('SSET%d,"ASSERTED"' % nSER)
            print('SCLR%d,"DEASSERTED"' % nSER)
            print('SHMI%d,"N"' % nSER)
            nSER += 1

        WordBit = InFile.readline().strip()

SERMax = 250

while nSER <= SERMax:
    print('SITM%d,""' % nSER)
    print('SNAME%d,""' % nSER)
    print('SSET%d,""' % nSER)
    print('SCLR%d,""' % nSER)
    print('SHMI%d,""' % nSER)
    nSER += 1
