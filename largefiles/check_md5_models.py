#!/usr/bin/env python

import os
import sys

cmd = "md5sum -c cencal080.tar.gz.md5"
print cmd
os.system(cmd)

cmd = "md5sum -c cvmh-15.1.0.tar.gz.md5"
print cmd
os.system(cmd)

cmd = "md5sum -c cvms426.tar.gz.md5"
print cmd
os.system(cmd)

cmd = "md5sum -c cvms4.tar.gz.md5"
print cmd
os.system(cmd)

cmd = "md5sum -c cvms5.tar.gz.md5"
print cmd
os.system(cmd)
