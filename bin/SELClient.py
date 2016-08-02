#! /usr/bin/env python

"""
Experimental Python telnet client for talking to SEL relays
"""

from __future__ import print_function, unicode_literals
from telnetlib import Telnet
import re

HOST = "192.168.217.166"
Level1Pass = "940018"
PROMPT0 = "*"
PROMPT1 = "*>"
PROMPT2 = "**>"
PromptRE = re.compile(r'\*>?>?')
PromptRE_relay = re.compile(r'\=>?>?')
PassPromptRE = re.compile(r'Password: \?')

tn = Telnet(HOST)

if False:
    tn.write("QUI\r")
    print "Send: ", repr("QUI\r")
    n, m, l = tn.expect([PromptRE], 10.0)
    print "Read: ", repr(l.strip())

    tn.write("ACC\r")
    print "Send: ", repr("ACC\r")
    n, m, l = tn.expect([PassPromptRE], 10.0)
    print "Read: ", repr(l.strip())
    tn.write(Level1Pass + "\r")
    print "Send: ", repr(Level1Pass + "\r")

    n, m, l = tn.expect([PromptRE], 10.0)
    print "Read: ", repr(l.strip())


tn.write("POR 1\r")
print "Send: ", repr("POR 1\r")

n, m, l = tn.expect([PromprRE_relay], 10.0)
print "read: ", repr(l.strip())

tn.write("ACC\r")
print "Send: ", repr("ACC\r")
n, m, l = tn.expect([PassPromptRE_relay], 10.0)
print "Read: ", repr(l.strip())
tn.write(Level1Pass + "\r")
print "Send: ", repr(Level1Pass + "\r")

tn.write("ID\r")
n, m, l = tn.expect([PassPromptRE_relay], 10.0)
n, m, l = tn.expect([PassPromptRE_relay], 10.0)
print "Read: ", repr(l.strip())
