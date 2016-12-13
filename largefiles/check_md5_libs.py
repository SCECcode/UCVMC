#!/usr/bin/env python

import os
import sys

cmd = "md5sum -c euclid3-1.3.tar.md5"
os.system(cmd)
print cmd

cmd = "md5sum -c fftw-3.3.3.tar.md5"
os.system(cmd)
print cmd

cmd = "md5sum -c proj-4.8.0.tar.md5"
os.system(cmd)
print cmd
