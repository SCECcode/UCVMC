#!/usr/bin/env python2
import sys
import os

#
# Test the density rule for cca
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.10 -e 1000.0 -c cca  -o cca_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_density_plot.py -i ./cca_map_grid_1000.txt  -e 1000.0 -n \"CCA density(x) Density from Vs(y)\" -o cca_rho_versus_vs_density_1000km.png"
os.system(cmd)
print cmd

#
# Test the density rule for cvms5
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.10 -e 1000.0 -c cvms5  -o cvms5_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_density_plot.py -i ./cvms5_map_grid_1000.txt  -e 1000.0 -n \"CVM-S4.26 density(x) Density from Vs(y)\" -o cvms5_rho_versus_vs_density_1000km.png"
os.system(cmd)
print cmd

#
# Test the density rule for cencal
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.10 -e 1000.0 -c cencal  -o cencal_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_density_plot.py -i ./cencal_map_grid_1000.txt  -e 1000.0 -n \"Cencal density(x) versus Density from Vs(y)\" -o cencal_rho_versus_vs_density_1000km.png"
os.system(cmd)
print cmd

#
# Test the density rule for cvmh
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 0.10 -e 1000.0 -c cvmh  -o cvmh_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_density_plot.py -i ./cvmh_map_grid_1000.txt  -e 1000.0 -n \"CVM-H density(x) versus Density from Vs(y)\" -o cvmh_rho_versus_vs_density_1000km.png"
os.system(cmd)
print cmd

sys.exit(0)
