#!/usr/bin/python
import sys

from util.Deploy import Deploy

call = Deploy()
call.setDest(sys.argv[1])
call.iter()
