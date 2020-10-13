#!/usr/bin/env python3
#
#  plot_density_plot.py
#
#  create a scatter plot of densities from an
#  map_pts text file generated from ucvm_query calls
#

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys,getopt
from pycvm import nafe_drake
#
#

def usage():
  print("Usage: ./plot_density_plot.py -i <inputfile> -d 100 -n Density(CCA)(x) Density(Algo)(Y)"
  print("Usage: ./plot_density_plot.py -i inputfile -d depth -n description"
  print("input file is a list of text file lines as returned by ucvm_query"
  print("-i inputfilename -e depth(meters) -n String describing data being plotted" 
  print("./plot_density_plot.py -i map_pts.txt -e 0.0 -n Density(CCA)(X) Density(Algo)(Y)"
  sys.exit(2)

def main(argv):
  inputfile = ''
  outputfile = ''
  depth = 0
  descript = ""
  try:
    opts, args = getopt.getopt(argv,"hi:o:e:n:",["ifile=","ofile="])
  except getopt.GetoptError:
    usage()

  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt in ("-e","--depth"):
      depth = float(arg)
    elif opt in ("-n","--name"):
      descript = arg
    elif opt in ("-i", "--ifile"):
      inputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg

  if (len(inputfile)<1):
    usage()

  print("\n"
  print("Input CVM file is: ", inputfile
  print("Output Image file is: ", outputfile
  print("Slice Depth:",depth
  print("Description:",descript

  list_of_datafiles = inputfile
  list_of_colors = "blue"

  fig = plt.figure()
  ax =  fig.add_subplot(111)

  ax.set_title(descript)
  ax.set_xlabel("Density (cm/kg3) at depth %s from model"%(depth))
  ax.set_ylabel("Density (rho) (cm/kg3) at depth %s from Nafe-Drake Vs to rho Scaling Relation."%(depth))

  ## the data
  f = open(list_of_datafiles,'r')
  dlines = f.readlines()
  f.close()
  x = []
  y = []
  parts = []

  ## Load rho in x and nafe_drake density in y. Extract them from
  # Columns 16 and 15 in the ucvm return lines
  for oneline in dlines:
    parts = oneline.split()
    x.append(float(parts[16]))
    vp = (float(parts[15]))
    # print("vp from model:",vp)
    rho = nafe_drake.vs_2_density(vp)
    # print("rho from vs:",rho)
    y.append(rho)

  ax.scatter(x,y,color=list_of_colors,s=5,edgecolor='none')
  ax.set_xlim([0,5000])
  ax.set_ylim([0,5000])
  #ax.set_aspect(1./ax.get_data_ratio()) # make axes square
  plt.savefig(outputfile)

if __name__ == "__main__":
  main(sys.argv[1:])
