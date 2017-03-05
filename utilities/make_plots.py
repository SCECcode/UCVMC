#!/usr/bin/env python
import sys
import os

#
# Make Cross Section Plots
#
cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvmh"
print cmd
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvms"
print cmd
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvmsi"
print cmd
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvms5"
print cmd
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c 1d"
print cmd
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c bbp1d"
print cmd
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cencal"
print cmd
os.system(cmd)

#
# Make Horizontal Slice Plots
#
cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvmh"
print cmd
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvms"
print cmd
os.system(cmd)

cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvmsi"
print cmd
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvms5"
print cmd
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c 1d"
print cmd
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c bbp1d"
print cmd
os.system(cmd)

cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cencal"
print cmd
os.system(cmd)

sys.exit(0)
