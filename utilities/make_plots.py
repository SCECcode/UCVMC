#!/usr/bin/env python3

import sys
import os

#
#
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 0.0 -d poisson -a s -c cs173h -o cs173h_poisson_map.png"
os.system(cmd)

#
# Make Cross Section Plots
#
cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvmh -o cross-cvmh.png"
print(cmd)
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvms -o cross-cvms.png"
print(cmd)
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvmsi -o cross-cvmsi.png"
print(cmd)
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cvms5 -o cross-cvms5.png"
print(cmd)
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c 1d -o cross-1d.png"
print(cmd)
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c bbp1d -o cross-bbp1d.png"
print(cmd)
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cencal -o cross-cencal.png"
print(cmd)
os.system(cmd)

cmd="./plot_cross_section.py -b 34.0,-122.00 -u 34.0,-117.5 -s 0 -e 2000 -h 500 -v 10 -d vs -a d -c cca -o cross-cca.png"
print(cmd)
os.system(cmd)

#
# Make Horizontal Slice Plots
#
cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvmh -o horizontal-cvmh.png"
print(cmd)
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvms -o horizontal-cvms.png"
print(cmd)
os.system(cmd)

cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvmsi -o horizontal-cvmsi.png"
print(cmd)
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cvms5 -o horizontal-cvms5.png"
print(cmd)
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c 1d -o horizontal-1d.png"
print(cmd)
os.system(cmd)


cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c bbp1d -o horizontal-bbp1d.png"
print(cmd)
os.system(cmd)

cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cencal -o horizontal-cencal.png"
print(cmd)
os.system(cmd)

cmd="./plot_horizontal_slice.py -b 33.5,-118.75 -u 34.5,-117.5 -s 0.1 -e 500 -d vs -a d -c cca -o horizontal-cca.png"
print(cmd)

os.system(cmd)
sys.exit(0)
