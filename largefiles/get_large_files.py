#!/usr/bin/env python
import sys
import os
from urllib2 import urlopen

ucvmc_largefile_dir = "http://hypocenter.usc.edu/research/ucvmc"

def download_urlfile(url,fname):
  try:
    response = urlopen(url)
    CHUNK = 16 * 1024
    with open(fname, 'wb') as f:
      while True:
        chunk = response.read(CHUNK)
        if not chunk:
          break
        f.write(chunk)
  except:
    e = sys.exc_info()[0]
    print "Exception retrieving and saving largefile:",e
    raise
  return True

#
# Check to make sure the script is being run with outside a UCVM directory
#
curdir = os.getcwd()
if os.path.basename(os.path.normpath(curdir)) == "largefiles":
  print "Running in UCVMC/largefiles source directory. "
  print "This script will download and install ucvm.e and several other files."
  print "Due to the size of the files, this download could take minutes to hours to complete."
else:
  print "Run this script in the directory that contains the UCVMC/largefiles src directory."
  print "This script will download and install ucvm.e and several other files."
  print "Due to the size of the files, this download could take minutes to hours to complete."
  sys.exit(0)

print "Retrieving files from: %s"%(ucvmc_largefile_dir)
print "Installing files in: %s"%(curdir)


large_lib_list = ["proj-4.8.0.tar.gz",
                  "fftw-3.3.3.tar.gz",
                  "euclid3-1.3.tar.gz"]

large_model_list = ["cvms5.tar.gz",
                    "cvms4.tar.gz",
                    "cvms426.tar.gz",
                    "cvmh-15.1.0.tar.gz",
                    "cencal080.tar.gz"]

large_etree_list = ["ucvm.e"]

large_ref_list = ["test-grid-lib-1d.ref"]


#
# First, download the required library files
#
for m in large_lib_list:
  print "Retrieving: ",m
  outfilename = "./%s"%(m)
  scec_url = "%s/%s"%(ucvmc_largefile_dir,m)
  #
  # First check if file exists. If so, don't re-download.
  # Tell user that old files must be deleted from UCVMC/largefiles to download new version
  #
  if not os.path.exists(outfilename):
    try:
      download_urlfile(scec_url,outfilename)
    except:
      print "Error downloading (%s), or writing file (%s)" % (scec_url,outfilename)
      break
    print "Finished downloading: ",m
  else:
    print "Required largefile already exists in UCVMC/largefile directory",outfilename
    print "If new version is required, delete current local copy (%s) and re-run this script"%(outfilename)

#
# Second download the CVM model files
#
for m in large_model_list:
  print "Retrieving: ",m
  outfilename = "./%s"%(m)
  scec_url = "%s/%s"%(ucvmc_largefile_dir,m)
  #
  # First check if file exists. If so, don't re-download.
  # Tell user that old files must be deleted from UCVMC/largefiles to download new version
  #
  if not os.path.exists(outfilename):
    try:
      download_urlfile(scec_url,outfilename)
    except:
      print "Error downloading (%s), or writing file (%s)" % (scec_url,outfilename)
      break
    print "Finished downloading: ",m
  else:
    print "Required largefile already exists in UCVMC/largefile directory",outfilename
    print "If new version is required, delete current local copy (%s) and re-run this script"%(outfilename)

#
# Next download the topography and vs30 etree files
#

for m in large_etree_list:
  print "Retrieving: ",m
  outfilename = "./%s"%(m)
  scec_url = "%s/%s"%(ucvmc_largefile_dir,m)
  #
  # First check if file exists. If so, don't re-download.
  # Tell user that old files must be deleted from UCVMC/largefiles to download new version
  #
  if not os.path.exists(outfilename):
    try:
      download_urlfile(scec_url,outfilename)
    except:
      print "Error downloading (%s), or writing file (%s)" % (scec_url,outfilename)
      break
    print "Finished downloading: ",m
  else:
    print "Required largefile already exists in UCVMC/largefile directory",outfilename
    print "If new version is required, delete current local copy (%s) and re-run this script"%(outfilename)

#
# Download the large reference result file
#
for m in large_ref_list:
  print "Retrieving: ",m
  outfilename = "./%s"%(m)
  scec_url = "%s/%s"%(ucvmc_largefile_dir,m)
  #
  # First check if file exists. If so, don't re-download.
  # Tell user that old files must be deleted from UCVMC/largefiles to download new version
  #
  if not os.path.exists(outfilename):
    try:
      download_urlfile(scec_url,outfilename)
    except:
      print "Error downloading (%s), or writing file (%s)" % (scec_url,outfilename)
      break
    print "Finished downloading: ",m
  else:
    print "Required largefile already exists in UCVMC/largefile directory",outfilename
    print "If new version is required, delete current local copy (%s) and re-run this script"%(outfilename)

print "Completed all required downloads. This computer is now ready to build and install the UCVMC programs and scripts."
sys.exit(0)
