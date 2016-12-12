#!/usr/bin/env python
import sys
import os
import urllib

print "Run this in the the UCVMC local git directory"
print "This script will download 5 large data files into the UCVM source directories"
print "This should be run before the UCVMC software is installed"
#
# Check to make sure the script is being run with outside a UCVM directory
#
curdir = os.getcwd()
if os.path.basename(os.path.normpath(curdir)) == "UCVMC":
    print "Running in UCVMC source tree. Will download and install ucvm.e and 4 other files."
else:
    print "Run this script in the directory that contains the UCVMC src directory."
    sys.exit(0)

print "Installing files in: %s"%(curdir)

f1_target = curdir + "/model/ucvm/ucvm.e"
f2_target = curdir + "/model/ucvm/ucvm_yong_wald.e"
f3_target = curdir + "/model/ucvm_utah/ucvm.e"
f4_target = curdir + "/test/ref/test-grid-lib-1d.ref"
f5_target = curdir + "/test/ref/test-grid-ucvm_query-1d.ref"

cmd = "md5sum -b %s %s %s %s %s > ./ucvm_large_files.md5"%(f1_target,f2_target,f3_target,f4_target,f5_target)
print "cmd: ",cmd

os.system(cmd)

print "Completed all required md5sums. To check these files type :"
print "md5sum -c ucvm_large_files.md5 sum"
sys.exit(0)
