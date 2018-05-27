#!/usr/bin/env python
import sys
import os

#
# 0 depth
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 1.00 -e 0.0 -c cencal,cca,cvmsi  -o norcal_map_grid_0.txt"
os.system(cmd)
print cmd
cmd="./plot_scatter_plot.py -i ./norcal_map_grid_0.txt  -e 0.0 -n \"CS18.4 Vp Density Scatter Plot 0k\" -o nocal_vp_versus_density_0km.png"
os.system(cmd)
print cmd


#
# Test the overall density vs vp
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 1.00 -e 1000.0 -c cencal,cca,cvmsi  -o norcal_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_scatter_plot.py -i ./norcal_map_grid_1000.txt  -n \"CS18.5 Vp Density Scatter Plot 1000km\" -o nocal_vp_versus_density_1000km.png"
os.system(cmd)
print cmd


#
# Test the density rule for cencal
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 1.00 -e 1000.0 -c cencal  -o cencal_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_scatter_plot.py -i ./cencal_map_grid_1000.txt  -e 1000.0 -n cencal_map_grid_1000_km -o cencal_vp_versus_density_1000km.png"
os.system(cmd)
print cmd


#
# Test the density rule for cca
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 1.00 -e 1000.0 -c cca  -o cca_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_scatter_plot.py -i ./cca_map_grid_1000.txt  -e 1000.0 -n cca_map_grid_0_km -o cca_vp_versus_density_1000km.png"
os.system(cmd)
print cmd

#
# Test the density rule for cvms5 
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 1.00 -e 1000.0 -c cvms5  -o cvms5_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_scatter_plot.py -i ./cvms5_map_grid_1000.txt  -e 1000.0 -n cvms5_map_grid_0_km -o cvms5_vp_versus_density_1000km.png"
os.system(cmd)
print cmd

#
# Test the density rule for cvmsi
cmd="./plot_map_grid.py -b 30.5,-126.0 -u 42.5,-112.5 -s 1.00 -e 1000.0 -c cvmsi  -o cvmsi_map_grid_1000.txt"
os.system(cmd)
print cmd
cmd="./plot_scatter_plot.py -i ./cvmsi_map_grid_1000.txt  -e 1000.0 -n cvmsi_map_grid_0_km -o cvmsi_vp_versus_density_1000km.png"
os.system(cmd)
print cmd

sys.exit(0)
