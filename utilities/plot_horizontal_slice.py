#!/usr/bin/env python2

##
#  @file plot_horizontal_slice.py
#  @brief Plots a horizontal slice using command-line parameters.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Plots a horizontal slice given a set of command-line parameters.

from pycvm import HorizontalSlice, UCVM, VERSION, UCVM_CVMS, Point, ask_number, ask_path, ask_file, get_user_opts
import getopt, sys, os

## Prints usage of this utility.
def usage():
    print "Plots a horizontal slice given two bounding latitude and longitude co-ordinates,"
    print "the CVM to plot, and a couple of other settings."
    print "\nValid arguments:"
    print "\t-b, --bottomleft: bottom-left latitude, longitude (e.g. 34,-118)"
    print "\t-u, --upperright: upper-right latitude, longitude (e.g. 35,-117)"
    print "\t-s, --spacing: grid spacing in degrees (typically 0.01)"
    print "\t-e, --depth: depth for horizontal slice in meters (e.g. 1000)"
    print "\t-d, --datatype: either 'vs', 'vp', 'density', or 'poisson', without quotation marks"
    print "\t-c, --cvm: one of the installed velocity models"
    print "\t-z, --zrange: optional Z-range for elygtl:ely (e.g. -z 0,350)"
    print "\t-Z, --zthreshold: optional Z-threshold for svmgtl:svm (e.g. -Z 1000)"
    print "\t-a, --scale: color scale, either 's' for smooth, 'd' for discretized or 'b' for bi-color scale, without quotes"
    print "\t-g, --gate: optional gate value for bi-color scale gate"
    print "\t-f, --datafile: optional binary input data filename"
    print "\t-o, --outfile: optional png output filename"
    print "\t-t, --title: optional plot title"
    print "\t-H, --help: optional display usage information"
    print "\t-i, --installdir: optional UCVM isntall directory"
    print "\t-n, --configfile: optional UCVM configfile"
    print "UCVM %s\n" % VERSION

ret_val = get_user_opts({"b,bottomleft":"lat1,lon1", \
                         "u,upperright":"lat2,lon2", \
                         "s,spacing":"spacing", \
                         "e,depth":"depth", \
                         "d,datatype":"data_type", \
                         "c,cvm":"cvm", \
                         "z,zrange,o":"zrange1,zrange2", \
                         "Z,zthreshold,o":"zthreshold", \
                         "a,scale": "color", \
                         "g,gate,o": "gate", \
                         "f,datafile,o":"datafile",
                         "o,outfile,o":"outfile", \
                         "t,title,o":"title", \
                         "H,help,o":"", \
                         "i,installdir,o":"installdir", \
                         "n,configfile,o":"configfile" })


meta = {}

if ret_val == "bad":
    usage()
    exit(1)
elif ret_val == "help":
    usage()
    exit(0)
elif len(ret_val) > 0:
    print "Using parameters:\n"
    for key, value in ret_val.iteritems():
        print key , " = " , value
        meta[key]=value
        try:
            float(value)
            exec("%s = float(%s)" % (key, value))
        except StandardError, e:
            if value is None:
                exec("%s = %s" % (key, value))
            else:
                exec("%s = '%s'" % (key, value))
else:  
    print ""
    print "Plot Horizontal Slice - UCVM %s" % VERSION
    print ""
    print "This utility helps you plot a horizontal slice across the earth for one of the CVMs"
    print "that you installed with UCVM."
    print ""
    print "In order to create the plot, you must first specify the region."
    print ""

    lon1 = ask_number("Please enter the bottom-left longitude from which the plot should start: ")
    lat1 = ask_number("Next, enter the bottom-left latitude from which the plot should start: ")
    lon2 = ask_number("Enter the top-right longitude where the plot should end: ")
    lat2 = ask_number("Enter the top-right latitude where the plot should end: ")

    # Check to see that this is a valid box.
    if lon1 > lon2 or lat1 > lat2:
        print "Error: (%.2f, %.2f) to (%.2f, %.2f) is not a valid box. Please re-run this script" % (lon1, lat1, lon2, lat2)
        print "and specify a valid region. The first point should be the lower-left corner, the"
        print "second point should be the upper-right corner."
        exit(1)
    meta['lon1']=lon1
    meta['lon2']=lon2
    meta['lat1']=lat1
    meta['lat2']=lat2

    spacing = -1
    while spacing <= 0:
        spacing = ask_number("Which grid spacing (in decimal degree units) would you like (usually, this is 0.01): ")
    
        if spacing <= 0:
            print "Error: grid spacing must be a positive number."
    meta['spacing']=spacing

    depth = -1
    print ""
    while depth < 0:
        depth = ask_number("Please enter the depth, in meters, at which you would like this plot: ")
        if depth < 0:
            print "Error: the depth must be a positive number."
    meta['depth']=depth

    print ""
    data_type = ""
    while data_type != "vs" and data_type != "vp" and data_type != "density" and data_type != "poisson":
        data_type = raw_input("What would you like to plot (either vp, vs, density, or poisson): ")
        data_type = data_type.lower().strip()
    
        if data_type != "vs" and data_type != "vp" and data_type != "density"  and data_type != "poisson":
            print "Error: you must select either 'vp', 'vs', 'density', 'poisson' (without quotation marks)."
    meta['mproperty']=data_type

    counter = 1
    corresponding_cvm = []
    installdir = None
    configfile = None

    # Ask if a different installdir should be  used
    cwd = os.getcwd()
    installdir = ask_path("Do you want to use different UCVM install directory", cwd+"/..")
    # Ask if a different ucvm.conf should be  used
    configfile = ask_file("Do you want to use different ucvm.conf file", cwd+"/../ucvm.conf")

    # Ask which CVMs to use.
    print "\nFrom which CVM would you like this data to come:"

    # Create a new UCVM object.
    u = UCVM(install_dir=installdir, config_file=configfile)

    for cvm in u.models:
        cvmtoprint = cvm
        if cvm in UCVM_CVMS:
            cvmtoprint = UCVM_CVMS[cvm]
        corresponding_cvm.append(cvm)
        print "\t%d) %s" % (counter, cvmtoprint)
        counter += 1
    
    cvm_selected = -1
    while cvm_selected < 0 or cvm_selected > counter:
        cvm_selected = int(ask_number("\nSelect the CVM: ")) - 1
    
        if cvm_selected < 0 or cvm_selected > counter:
            print "Error: the number you selected must be between 1 and %d" % counter

    cvm_selected = corresponding_cvm[cvm_selected]
    meta['cvm']=cvm_selected

    # We will offer three color options. Discretized, smooth or bi-color. But, we'll only offer red-blue for now.
    gate = 2.5
    color = ""
    while color != "s" and color != "d":
        print ""
        color = raw_input("Finally, would you like a descritized or smooth color scale\n(enter 'd' for discrete, 's' for smooth): ")
        color = color.strip()
    
        if color != "s" and color != "d" and color !="b":
            print "Please enter 'd' (without quotation marks) for a discrete color bar and 's' (without quotation"
            print "marks) for a smooth color scale and 'b' (without quotation marks) for bi-color scale."
    meta['gate']=gate
    meta['color']=color


# Now we have all the information so we can actually plot the data.
print ""
print "Retrieving data. Please wait..."
 
###################################################################################
# Generate the horizontal slice.
h = HorizontalSlice(Point(lon1, lat2, depth), Point(lon2, lat1, depth), meta)
h.plot()
