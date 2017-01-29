#!/usr/bin/env python
import os
import sys
import subprocess
#
# Script for checking downloaded UCVM Files. This script should be run
# after the UCVM largefiles have been retrieved from their respository
# into the UCVMC/largefiles subdirectory.
#
# When both the UCVMC/largefiles and their associated md5 files
# are located in the same directory, then this script will confirm
# that the largefiles are intact.
#
# The md5 files are downloaded from git repository
# Then largefiles are downloaded from SCEC website
# This script confirms that all files have been downloaded intact.
# This script provides assurance that the downloaded largefiles
# are the files required for UCVMC to work properly
#

def check_md5file(filename,total_ok,total_errs):
  print "Checking file: %s"%(filename) 
  proc = subprocess.Popen(["md5sum", "-c", filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  out,err = proc.communicate()
  res = out.split()
  if res[1] == "OK":
    print "File: %s OK"%(filename)
    total_ok += 1
  else:
    print "Erorr: %s does not match expected value."%(filename)
    total_errs += 1
  return total_ok,total_errs

UCVM_Version = "17.1"
total_ok = 0
total_errs = 0
#
#
#
print "Checking largefiles for UCVMC version: %s"%(UCVM_Version)
#
# Check Model Files
#
total_ok, total_errs = check_md5file("cencal080.tar.gz.md5",total_ok,total_errs)

total_ok, total_errs = check_md5file("cvmh-15.1.0.tar.gz.md5",total_ok,total_errs)

total_ok, total_errs = check_md5file("cvms426.tar.gz.md5",total_ok,total_errs)

total_ok, total_errs = check_md5file("cvms4.tar.gz.md5",total_ok,total_errs)

total_ok, total_errs = check_md5file("cvms5.tar.gz.md5",total_ok,total_errs)
#
# Check Library Files
#
total_ok, total_errs = check_md5file("euclid3-1.3.tar.gz.md5",total_ok, total_errs)

total_ok, total_errs = check_md5file("fftw-3.3.3.tar.gz.md5", total_ok, total_errs)

total_ok, total_errs = check_md5file("proj-4.8.0.tar.gz.md5", total_ok, total_errs)
#
# Check etree files
# 
total_ok, total_errs = check_md5file("ucvm.e.md5", total_ok, total_errs)
#
# Check reference grids files
#
total_ok, total_errs = check_md5file("test-grid-lib-1d.ref.md5",total_ok, total_errs)
#
# All largefiles checked
#
print "Checked %d UCVM large files with: %d OK, and: %d errors"%((total_ok+total_errs),total_ok,total_errs)
sys.exit(0)
