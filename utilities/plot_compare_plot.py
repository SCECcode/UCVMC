#!/usr/bin/env python

##
#  @file plot_compare_plot.py
#  @brief Plot a scatter plot to compare two binary data files 
#  @author SCEC <mei@usc.edu>
#  @version 18.5.0
#
#  Plots a scatter plot that compares two binary datasets
#  for similarity using matplotlib/numpy

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np
import sys,getopt

def usage():
  print "\nPlot a scatter plot to compare two binary data files"
  print "Valid arguments:"
  print "\t-x, --xfile: file to use for x axis"
  print "\t-y, --yfile: file to use for y axis"
  print "\t-o, --ofile: png filename to use for resulting plot"
  print "./plot_compare_plot.py -x x.bin -y y.bin [-o o.png]"
  sys.exit(2)

## need to figure out how to distinguish them
## the data can be in np.float or np.float32 

def main(argv):
  xinputfile = ''
  yinputfile = ''
  outputfile = 'out.png'
  try:
    opts, args = getopt.getopt(argv,"hx:y:o:",["xfile=","yfile=","ofile="])
  except getopt.GetoptError:
    usage()

  for opt, arg in opts:
    if opt == '-h':
      usage()
    elif opt in ("-x", "--xfile"):
      xinputfile = arg
    elif opt in ("-y", "--yfile"):
      yinputfile = arg
    elif opt in ("-o", "--ofile"):
      outputfile = arg

  if (len(xinputfile)<1 or len(yinputfile)<1):
    usage()

  print "\nInput CVM files are: ", xinputfile, " ", yinputfile
  print "Output Image file is: ", outputfile

  list_of_colors = "blue"

  fig = plt.figure()
  ax =  fig.add_subplot(111)

  ax.set_title("scatter comparison")
  ax.set_xlabel("%s"%(xinputfile))
  ax.set_ylabel("%s"%(yinputfile))

  ## the data

  fh = open(xinputfile,'r')
  x = np.fromfile(fh, dtype=np.float32)
  print "extracted ",len(x)," data points from ", xinputfile
  fh.close()
  fh = open(yinputfile,'r')
  y = np.fromfile(fh, dtype=np.float32)
  print "extracted ",len(y)," data points from ", yinputfile
  fh.close()

  ax.scatter(x,y,color=list_of_colors,s=5,edgecolor='none')
  ax.set_aspect(1./ax.get_data_ratio()) # make axes square
  plt.savefig(outputfile)
  #plt.show()

if __name__ == "__main__":
  main(sys.argv[1:])
