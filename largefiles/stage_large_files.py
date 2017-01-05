#!/usr/bin/env python
#
# This script moves large files from current directory to the target directory so that they
# are ready for processing with the ucvm_setup.py script
#
import os
import sys
from shutil import copyfile

curpath = "/home/scec-00/maechlin/icvm/test1/UCVMC"

if len(sys.argv) < 2:
  print "Using default as UCVMC install directory"
  print "Override default using the command line"
  print "%stage_large_files.py /home/scec-00/maechlin/icvm/b1/UCVMC"
  src_dir = curpath
else:
  src_dir = str(sys.argv[1])

print src_dir

large_model_list = ["cvms5.tar.gz",
                    "cvms4.tar.gz",
                    "cvms426.tar.gz",
                    "cvmh-15.1.0.tar.gz",
                    "cencal080.tar.gz"]

large_lib_list = ["proj-4.8.0.tar.gz",
                  "fftw-3.3.3.tar.gz",
                  "euclid3-1.3.tar.gz"]

model_dir = src_dir + "/work/model"
print model_dir
lib_dir = src_dir + "/work/lib"
print lib_dir


for l in large_lib_list:
  local_file = "./" + l 
  target_file = lib_dir + "/" + l
  if not os.path.exists(target_file):
    print "ready to move lib:",local_file
    copyfile(local_file,target_file)
    # 
    # remove existing tar file so gzip doesn't ask for permisson
    #
    tarfile = os.path.splitext(os.path.basename(l))[0]
    tarfilepath = lib_dir + "/" + tarfile
    if os.path.exists(tarfilepath):
      print "Removing existing lib tar file",tarfilepath
      os.remove(tarfilepath)
  else:
    print "Target lib file already exists",target_file

for m in large_model_list:
  local_file = "./" + m
  target_file = model_dir + "/" + m
  if not os.path.exists(target_file):
    print "ready to move model:",local_file
    copyfile(local_file,target_file)
    # 
    # remove existing tar file so gzip doesn't ask for permisson
    #
    tarfile = os.path.splitext(os.path.basename(m))[0]
    tarfilepath = model_dir + "/" + tarfile
    if os.path.exists(tarfilepath):
      print "Removing existing model tar file",tarfilepath
      os.remove(tarfilepath)
  else:
    print "Target model file already exists",target_file

print "All required library and model files staged in ucvmc work directories"
sys.exit(0)
