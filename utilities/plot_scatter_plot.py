#!/usr/bin/env python2
#
#  plot_scatter_plot.py
#
#  create a scatter plot of vp vs density from an external
#  map_pts text file generated from ucvm_query calls
#

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import sys,getopt



def usage():
  print "Usage: ./plot_scatter_plot.py -i <inputfile> -d 100 -n Density(CCA)(x) Density(Algo)(Y)"
  print "Usage: ./plot_scatter_plot.py -i inputfile -d depth -n description"
  print "input file is a list of text file lines as returned by ucvm_query"
  print "-i inputfilename -e depth(meters) -n String describing data being plotted" 
  print "./plot_scatter_plot.py -i map_pts.txt -e 0.0 -n Density(CCA)(X) Density(Algo)(Y)"
  sys.exit(2)

#
#
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

  print "\n"
  print "Input CVM file is: ", inputfile
  print "Output Image file is: ", outputfile
  print "Slide Depth:",depth
  print "Description:",descript

  list_of_datafiles = inputfile
  list_of_colors = "blue"

  fig = plt.figure()
  ax =  fig.add_subplot(111)

  ax.set_title(descript)
  ax.set_xlabel("Vp (m/s) at depth %s"%(depth))
  ax.set_ylabel("Density (rho) (kg/m3) at depth %s"%(depth))

  ## the data
  f = open(list_of_datafiles,'r')
  dlines = f.readlines()
  f.close()
  x = []
  y = []
  parts = []

  ## Load vp in x and density in y. Extract them from
  # Columns 14 and 16 in the ucvm return lines
  for oneline in dlines:
    parts = oneline.split()
    x.append(float(parts[14]))
    y.append(float(parts[16]))

  ax.scatter(x,y,color=list_of_colors,s=5,edgecolor='none')
  ax.set_aspect(1./ax.get_data_ratio()) # make axes square
  plt.savefig(outputfile)
  #plt.show()

if __name__ == "__main__":
  main(sys.argv[1:])
