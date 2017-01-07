#!/usr/bin/env python
# file make_manifest.py
"""
This is designed to create a simple manifest, showing all files in
the input directory

name: make_manifest.py
description: Make Manifest
This performs a recursive directory and outputs a list of all the files in the directory and 
associated sub-directories.
This is used only to help document a software distribution, but creating a list of
all distributed files. This is not used for any scientific research purposes.

Inputs:
Can be run in the src directory, and it will recursively list all files.
Can be passed a path name on the command line, and it will use that path as its
starting point.


Outputs:
Creates a file named "manifest.txt" in the current directory which contains a list of
files included in the distribution.

The ls command parameters used below include:

# R - recursive
# A - don't show . or ..
# Q - quote file names
# L - show linked file not link
# h - human format size
# l - with h shows human file sizes
# p - show directories with /
# t - sort by modificatoin time
# s - show size
# c - short by mod time
# x - horizontal
"""
import os
import sys

dir_name = ""
if (len(sys.argv) < 2):
 dir_name = "."
else:
 dir_name = sys.argv[1]
cmd = "ls -RALGShwoqptc %s > manifest.txt"%(dir_name)
print "Running cmd: %s"%(cmd)
os.system(cmd)
