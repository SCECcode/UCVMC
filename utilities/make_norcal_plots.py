#!/usr/bin/env python2
import sys
import os

#
# 0 depth
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 0.0 -d vp -a s -c cencal,cca,cvmsi  -o \"norcal_vp_0_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 0.0 -d vs -a s -c cencal,cca,cvmsi  -o \"norcal_vs_0_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 0.0 -d density -a s -c cencal,cca,cvmsi  -o \"norcal_density_0_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 0.0 -d poisson -a s -c cencal,cca,cvmsi  -o \"norcal_poisson_0_map.png\""
os.system(cmd)
print cmd
##100
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 100.0 -d vp -a s -c cencal,cca,cvmsi  -o \"norcal_vp_100_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 100.0 -d vs -a s -c cencal,cca,cvmsi  -o \"norcal_vs_100_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 100.0 -d density -a s -c cencal,cca,cvmsi  -o \"norcal_density_100_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 100.0 -d poisson -a s -c cencal,cca,cvmsi  -o \"norcal_poisson_100_map.png\""
os.system(cmd)
print cmd
#1000
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 1000.0 -d vp -a s -c cencal,cca,cvmsi  -o \"norcal_vp_1000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 1000.0 -d vs -a s -c cencal,cca,cvmsi  -o \"norcal_vs_1000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 1000.0 -d density -a s -c cencal,cca,cvmsi  -o \"norcal_density_1000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 1000.0 -d poisson -a s -c cencal,cca,cvmsi  -o \"norcal_poisson_1000_map.png\""
os.system(cmd)
print cmd

#10000
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 10000.0 -d vp -a s -c cencal,cca,cvmsi  -o \"norcal_vp_10000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 10000.0 -d vs -a s -c cencal,cca,cvmsi  -o \"norcal_vs_10000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 10000.0 -d density -a s -c cencal,cca,cvmsi  -o \"norcal_density_10000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 10000.0 -d poisson -a s -c cencal,cca,cvmsi  -o \"norcal_poisson_10000_map.png\""
os.system(cmd)
print cmd

#40000
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 40000.0 -d vp -a s -c cencal,cca,cvmsi  -o \"norcal_vp_40000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 40000.0 -d vs -a s -c cencal,cca,cvmsi  -o \"norcal_vs_40000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 40000.0 -d density -a s -c cencal,cca,cvmsi  -o \"norcal_density_40000_map.png\""
os.system(cmd)
print cmd
cmd="./plot_horizontal_slice.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -e 40000.0 -d poisson -a s -c cencal,cca,cvmsi  -o \"norcal_poisson_40000_map.png\""
os.system(cmd)
print cmd

#
# Other plots

cmd="./plot_elevation_map.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -a s -c cencal,cca,cvmsi  -o \"norcal_elevation_map.png\""
os.system(cmd)
print cmd
cmd="./plot_vs30_map.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -a s -c cencal,cca,cvmsi  -o \"norcal_vs30_map.png\""
os.system(cmd)
print cmd
cmd="./plot_vs30_etree_map.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -a s -c cencal,cca,cvmsi  -o \"norcal_vs30_etree_map.png\""
os.system(cmd)
print cmd
cmd="./plot_z25_map.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -a s -c cencal,cca,cvmsi -o \"norcal_z25_map.png\""
os.system(cmd)
print cmd
cmd="./plot_z10_map.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.05 -a d -c cencal,cca,cvmsi -o \"norcal_z10_map.png\""
os.system(cmd)
print cmd

sys.exit(0)
