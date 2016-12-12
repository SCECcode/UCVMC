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

print "Retrieving: ",f1_target
urllib.urlretrieve ("http://hypocenter.usc.edu/research/UCVM/ES_Paper/ucvm.e", f1_target)
print "Finished: ",f1_target

print "Retrieving: ",f2_target
urllib.urlretrieve ("http://hypocenter.usc.edu/research/UCVM/ES_Paper/ucvm_yong_wald.e", f2_target)
print "Finished: ",f2_target

print "Retrieving: ",f3_target
urllib.urlretrieve ("http://hypocenter.usc.edu/research/UCVM/ES_Paper/utah/ucvm.e", f3_target)
print "Finished: ",f3_target

print "Retrieving: ",f4_target
urllib.urlretrieve ("http://hypocenter.usc.edu/research/UCVM/ES_Paper/test-grid-lib-1d.ref", f4_target)
print "Finished: ",f4_target

print "Retrieving: ",f5_target
urllib.urlretrieve ("http://hypocenter.usc.edu/research/UCVM/ES_Paper/test-grid-ucvm_query-1d.ref", f5_target)
print "Finished: ",f5_target

print "Completed all required downloads. This computer is now ready to build and install the UCVMC programs and scripts." 
sys.exit(0)
