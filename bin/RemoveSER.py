#! /usr/bin/env python

"""RemoveSER.py
USAGE:  RemoveSER.py <FILENAME>  <SER Word Bit> [<SER Word Bit> ...]
where <FILENAME> is the file exported from AcSELerator for an SEL-4xx relay's
Report setting group (typically named SET_R1.txt).  The filename should be
followed by the name of one or more relay Word Bits to be removed from the
relay's settings.  The requested settings are removed and other settings are
moved up accordingly.
"""

from __future__ import print_function, unicode_literals
import re
import sys

#FileName = r'C:\Users\pdbrown\Desktop\Shell Creek Setting Verification.txt'
if len(sys.argv) == 1:
    print "ERROR:  Please include a filename when calling this program."
    print "(Example Usage:  %s \"Setting Verification.txt\" 32QR 32QF)" % sys.argv[0]
    print "\nIf you passed in a filename but still received this error, \
            the problem may be Windows calling the Python program without arguments."
    sys.exit(1)
elif len(sys.argv) < 3:
    print "ERROR:  Please include a list of word bits to remove."
    print "(Example Usage:  %s \"Setting Verification.txt\" 32QR 32QF)" % sys.argv[0]
    sys.exit(1)

serDelSet = set(sys.argv[2:])

InFileName = sys.argv[1]
fnMatch = re.match(r'(.*)\.(.+)', sys.argv[1])
OutFileName = fnMatch.group(1) + r' (edited).' + fnMatch.group(2)

print "Reading settings from ", InFileName
print "Removing SER Points ", serDelSet
print "Saving settings to ", OutFileName

SettingRegEx = re.compile(r'([A-Z]+)([0-9]+),"(.*)"')


nSER = 1

with open(InFileName) as InFile:
    with open(OutFileName, 'w') as OutFile:

        # Read in lines until SER settings are found
        l = InFile.readline()
        if l:
            sMatch = SettingRegEx.match(l)
        else:
            sMatch = None
        while l:
            if sMatch:
                # Modify only SER points
                if sMatch.group(1) == 'SITM':
                    # Check for point to be deleted
                    if sMatch.group(3) in serDelSet:
                        # Read in next four lines and throw them away
                        for n in xrange(4):
                            InFile.readline()
                    else:
                        OutFile.write('%s%d,"%s"\n' % (sMatch.group(1), nSER, sMatch.group(3))) # SITM
                        # Repeat for next four lines of SER setting group
                        for n in xrange(4):
                            sMatch = SettingRegEx.match(InFile.readline())
                            OutFile.write('%s%d,"%s"\n' % (sMatch.group(1), nSER, sMatch.group(3)))
                        nSER += 1
                else:
                    OutFile.write(l)
            else:
                OutFile.write(l)

            l = InFile.readline()
            if l:
                sMatch = SettingRegEx.match(l)
            else:
                sMatch = None

