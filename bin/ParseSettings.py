#! /usr/bin/env python

"""ParseSettings.py
USAGE:
ParseSettings.py <FILENAME>
where <FILENAME> is the name of a file that contains the a communication log that
includes relay settings to be parsed.

This program will read in a log of communications with a relay, parse out the
relay settings, and then write them to a collection of files suitable for import
into AcSELerator.  The intent is to avoid having to interrupt SCADA polling of
the relay by accessing direct communications and the file transfer protocol.

Output files for import into AcSELerator are saved on the current user's desktop
in a folder called "ParseSettings".  Each relay's settings will be exported to
files in a sub-folder under the "ParseSettings" folder.  A file will be exported
for each time that a SHO command is detected.  If the export file for that setting
group is detected to already exist, a new filename will be chosen with an
incrementing number in parentheses added.


The program depends on having an ID command run prior to SHO commands to know
what relay the settings are for and how to parse the SHO output.  The RelayID
reported by the ID command is used to name the relay setting folders for exported
settings.

The program will handle backspaces properly but may choke on settings if the
SHO output is terminated early (with Ctl-X or a comm error) or if characters
are missing from the relay output (comm errors).

The program is intended to work generally for SEL-4xx and SEL-3xx relays (and
possibly others), but it has been tested primarily with SEL-421 relays.
"""

from __future__ import print_function, unicode_literals
import re
import os
import errno
import sys

#FileName = r'C:\Users\pdbrown\Desktop\Shell Creek Setting Verification.txt'
if len(sys.argv) == 1:
    print "ERROR:  Please include a filename when calling this program."
    print "(Example:  %s \"Setting Verification.txt\")" % os.path.basename(sys.argv[0])
    sys.exit(1)
elif len(sys.argv) > 2:
    print "ERROR:  Too many input parameters.  Please include one filename when calling this program."
    print "(Example:  %s \"Setting Verification.txt\")" % os.path.basename(sys.argv[0])
    sys.exit(1)

FileName = sys.argv[1]
SavePath = os.path.expanduser('~') + r'\Desktop\ParseSettings'
print "Extracted settings will be saved to directories under %s" % SavePath

# Some constants for saving the "context" for reading in multiline settings
class mlConst(object):
    notML = 0
    SER = 1
    SPAnalogs = 2
    ERAnalogs = 3
    ERDigitals = 4
    Protection = 5
    Automation = 6

# Number of points to fill up to for multiline settings
mlNmax = { mlConst.SER: 250,
           mlConst.SPAnalogs: 20,
           mlConst.ERAnalogs: 20,
           mlConst.ERDigitals: 800,
           mlConst.Protection: 100,
           mlConst.Automation: 100}

findBackspace = re.compile("[^\x08]\x08")
def pbsp(s):
    return re.sub('\x08', r'\x08', s)

def getCmd(l):
    c = re.compile(r'=>?>? *(.+)', re.IGNORECASE)
    m = c.match(l)
    if m:
        ##print "cmd: ", pbsp(m.group(1))
        return m.group(1)
    else:
        return None

"""
Return a list of sanitized line (backspaces and line continuations applied)
"""
def sanitizeLines(lines):
    newLines = []
    i = iter(lines)
    for l in i:
    # Check for line continuation as indicated by backslash and read
    # following line(s) as needed
        while len(l.strip())>0 and l.strip()[-1]=="\\":
            l = l.strip()[0:-1] + i.next().strip()
        # Check for and apply any backspaces and add to sanitized list
        while findBackspace.search(l):
            l = findBackspace.sub('', l)
        newLines.append(l)
    return newLines

"""
Utility class to be able to iterate forward and backward over a list.
"""
class bidirectionalList(object):
    def __init__(self, l=[]):
        self.l = list(l)
        self.pos = 0
        # Keep track of whether the list was accessed yet so that the first item
        # is returned whether cur() is called first or next() is called first.
        self.accessed = False
    def next(self):
        if self.accessed:
            self.pos += 1
        if self.pos > len(self.l)-1:
            raise StopIteration
        self.accessed = True
        return self.l[self.pos]
    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            raise StopIteration
        return self.l[self.pos]
    def cur(self):
        self.accessed = True
        return self.l[self.pos]
    def peekNext(self):
        try:
            return self.l[self.pos+1]
        except IndexError:
            return ""

def getID(f):
    l = f.next()
    getIDRegex = re.compile(r'"(\w+)=(.+)",".+"')
    idMatch = getIDRegex.match(l)
    idData = []
    while idMatch:
        idData.append(idMatch.groups())
        l = f.next()
        idMatch = getIDRegex.match(l)
    f.prev()
    return dict(idData)

def getSettings(f, FID, group):
    settings = []

    l = f.next()

    # Some attempt is made to get parsing that works for the SEL-4xx series
    # and other relays.  Not all relay types are tested, but it should work
    # at least for SEl-421 and SEL-351 relays.

    # SEL-4xx relays use := as the setting name and value separator
    # Other relays just use =.
    if re.match('SEL-4', FID):
        setSep = r':='
    else:
        setSep = r'='

    setRegExStrSimple = r' *(\w+) *' + setSep + r'(.+)' # Have to multiply by number of settings
    setRegExMultiline = re.compile(r'([0-9]+): (.+)')
    setRegExSER = re.compile(r'(\w+),"(.+)","(.+)","(.+)",?(\w)?')
    SERSetList = ["SITM", "SNAME", "SSET", "SCLR", "SHMI"]

    setRegExSimpleTest = re.compile(setRegExStrSimple)
    setRegExMultilineTest = setRegExMultiline

    setRegExSERTest = re.compile(r'^SER Points')
    setRegExDigitalsTest = re.compile(r'^Event Reporting Digital')
    setRegExAnalogsTest = re.compile(r'^Event Reporting Analog')
    setRegExAutomationTest = re.compile(r'^Automation')
    setRegExProtectionTest = re.compile(r'^Protection')
    setRegExSPAnalogsTest = re.compile(r'^Signal Profile')
    context = None
    while not getCmd(l):
        # Multiline settings
        if setRegExMultilineTest.match(l):
            setMatch = setRegExMultiline.match(l)
            if mlContext == mlConst.SER:
                SERPtList = setRegExSER.match(setMatch.group(2)).groups()
                setList = [s + setMatch.group(1) for s in SERSetList]
                settings.extend(zip(setList, SERPtList))
                # Peek ahead to see if we are at the end of the list
                if not setRegExMultiline.match(f.peekNext()):
                    # Figure out where to start counting
                    nStart = int(setMatch.group(1)) + 1
                    # Add blank points to fill up to the specified number of points
                    for n in xrange(nStart,mlNmax[mlConst.SER]+1):
                        setList = [s + "%d"%n for s in SERSetList]
                        SERPtList = [""]*len(setList)
                        settings.extend(zip(setList, SERPtList))

            else:
                if mlContext == mlConst.ERDigitals:
                    mlPrefix = 'ERDG'
                elif mlContext == mlConst.Protection:
                    mlPrefix = 'PROTSEL'
                elif mlContext == mlConst.Automation:
                    mlPrefix = 'AUTO_'
                elif mlContext == mlConst.SPAnalogs:
                    mlPrefix = 'SPAQ'
                elif mlContext == mlConst.ERAnalogs:
                    mlPrefix = 'ERAQ'
                setName = mlPrefix + setMatch.group(1)
                setValue = setMatch.group(2).strip()
                settings.append((setName, setValue))
                # Peek ahead to see if we are at the end of the list
                if not setRegExMultiline.match(f.peekNext()):
                    # Figure out where to start counting
                    nStart = int(setMatch.group(1)) + 1
                    # Add blank points to fill up to the specified number of points
                    setList = [ mlPrefix + "%d"%n for n in xrange(nStart, mlNmax[mlContext]+1)]
                    settings.extend(zip(setList, [""]*len(setList)))


        # Simple Settings (multiple settings per line)
        elif setRegExSimpleTest.match(l):
            mlContext = mlConst.notML
            nSettings = len(re.findall(setSep, l))
            setMatchList = re.match(r'\s+'.join([setRegExStrSimple] * nSettings), l)
            setNameList = [n.strip() for n in setMatchList.groups()[0::2]]
            setValueList = [n.strip().strip('"') for n in setMatchList.groups()[1::2]]
            settings.extend(zip(setNameList, setValueList))

        # Check for context in case a multiline setting shows up next
        elif setRegExSERTest.match(l):
            mlContext = mlConst.SER
        elif setRegExDigitalsTest.match(l):
            mlContext = mlConst.ERDigitals
        elif setRegExAnalogsTest.match(l):
            mlContext = mlConst.ERAnalogs
        elif setRegExProtectionTest.match(l):
            mlContext = mlConst.Protection
        elif setRegExAutomationTest.match(l):
            mlContext = mlConst.Automation
        elif setRegExSPAnalogsTest.match(l):
            mlContext = mlConst.SPAnalogs

        l = f.next()

    # Put unused line back
    f.prev()
    return settings

idRegex = re.compile(r'^ID.*', re.IGNORECASE)
shoRegex = re.compile(r'^SHOW? +(\w+) *$', re.IGNORECASE)

cmd = None
settingList = []
relayID = None

# Read in all settings
with open(FileName) as rawf:
    # Since it is hard to back up in the file read, we will read all the lines
    # into a queue, that way if a function gets a line it doesn't process it
    # can put it back on the queue.
    f = bidirectionalList(sanitizeLines(rawf.readlines()))
    l = f.next()
    cmd = getCmd(l)
    while True:
        try:
            # Read down to next command
            while not cmd:
                l = f.next()
                cmd = getCmd(l)

            # Check if an ID command was issued
            if idRegex.match(cmd):
                relayID = getID(f)
                print "Found relay %s" % relayID["DEVID"]
                cmd = None
                continue

            # Check if a SHO command was issued
            shoMatch = shoRegex.match(cmd)
            ##print "Command: ", pbsp(cmd), shoMatch
            if shoMatch:
                groupTxt = shoMatch.group(1)
                group = list(re.match("(\w) *(\w)?", groupTxt).groups())
                # Massage the group identifier to the format used by AcSELerator
                # SEL-4xx relays are different from others
                if re.match('SEL-4', relayID["FID"]):
                    if re.match(r'[1-6]', group[0]):
                        group[1] = group[0]
                        group[0] = 'S'
                    if not group[1]:
                        group[0] = group[0].upper()
                        group[1] = "1"
                if group[1]:
                    group = ''.join(group)
                else:
                    group = group[0]
                print "Found setting group %s" % group
                settings = getSettings(f, relayID["FID"], group)
                cmd = None
                # Save settings to list with relayID
                settingList.append({"relayID": relayID, "group": group, "settings": settings})
                continue

            # In case we fall through the above checks, reset cmd
            cmd = None
        except StopIteration:
            break

unsafeChars = re.compile('[^A-Za-z0-9 _-]')

# Write out settings to file(s)
for s in settingList:
    relayID = s["relayID"]
    group = s["group"]
    settings = s["settings"]

    # Determine directory to save settings in
    # The path will be relative to the current working directory
    if relayID:
        SaveDir = SavePath + '\\' + unsafeChars.sub('_', relayID["DEVID"])
    else:
        SaveDir = SavePath + r'\NODEVID'

    # Create directory if needed
    try:
        os.makedirs(SaveDir)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

    # Determine desired filename
    SaveFile = SaveDir + '\\' + "Set_" + group + ".txt"
    if os.path.isfile(SaveFile):
        ctr = 1
        SaveFile = SaveDir + '\\' + "Set_" + group + " (%d).txt" % ctr
        while os.path.isfile(SaveFile):
            ctr += 1
            SaveFile = SaveDir + '\\' + "Set_" + group + " (%d).txt" % ctr

    # Write data to file
    print "Saving relay %s group %s in file\n    %s" % (relayID["DEVID"], group, SaveFile)
    with open(SaveFile, 'w') as f:
        # First write INFO header
        f.write("[INFO]\n")
        f.write("RELAYTYPE=%s\n" % re.match(r'(SEL-[0-9A-Z]+(-[0-9])?)-R', relayID["FID"]).group(1))
        f.write("FID=%s\n" % relayID["FID"])
        f.write("BFID=%s\n" % relayID["BFID"])
        f.write("PARTNO=%s\n" % relayID["PARTNO"])
        f.write("[%s]\n" % group)
        for s in settings:
            f.write('%s,"%s"\n' % s)

os.system('pause')
