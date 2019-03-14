#!/usr/bin/env python

import sys
import random

filepath = sys.argv[1]
filelength= 2063344

with open(filepath, 'w') as outf:
    for i in range(filelength):
        outf.write(str(random.random()) + '\n')
