#!/usr/bin/env python2

import sys
import os

cmd="./plot_cross_section.py -b 35.21,-121 -u 35.21,-118 -c cca -s 0 -e 5000 -v 100 -h 1000 -g 2.5 -a b -d vs -o cross_section_cca_bi.png"
print cmd
os.system(cmd)

cmd="./plot_elevation_cross_section.py -b 35.21,-121 -u 35.21,-118 -h 1000 -v -100 -d vs -c cca -a b -s 1000 -e -4000 -g 2.5 -o cross_section_elevation_cca_b.png"
print cmd
os.system(cmd)

cmd="./plot_elevation_cross_section.py -b 35.21,-121 -u 35.21,-118 -h 1000 -v -100 -d vs -c cca -a b -s 1000 -e -4000 -g 3.0 -o cross_section_elevation_cca_b_2.png"
print cmd
os.system(cmd)

cmd="./plot_cross_section.py -c cvmh -s 0 -e 5000 -v 100 -h 1000 -g 2.5 -a b -d vs -b 35.21,-121 -u 35.21,-118 -o cross_section_cvmh_bi.png"
print cmd
os.system(cmd)

cmd="./plot_horizontal_slice.py -b 34.21,-121.0 -u 36.21,-118 -s 0.05 -e 200 -d vs -a b -c cca -o horizontal_cca_vs_bi.png"
print cmd
os.system(cmd)



