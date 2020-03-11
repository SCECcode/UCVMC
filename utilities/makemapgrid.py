#!/usr/bin/env python2

##
#  @file makemapgrid.py
#  @brief Generate a material properties txt information base on a slice of horizontal slice using returns from ucvm_query
#  @author SCEC
#  @version 19.4.0
#
from pycvm import MapGridHorizontalSlice, UCVM, VERSION, UCVM_CVMS, Point, ask_number, ask_path, ask_file, get_user_opts
import getopt, sys, os

## Prints usage of this utility.
def usage():
    print "Plots the return values from ucvm_query for a horizontal slice given two bounding latitude and longitude co-ordinates,"
    print "the CVM to plot, and a couple of other settings."
    print "\nValid arguments:"
    print "\t-b, --bottomleft: bottom-left latitude, longitude (e.g. 34,-118)"
    print "\t-u, --upperright: upper-right latitude, longitude (e.g. 35,-117)"
    print "\t-s, --spacing: grid spacing in degrees (typically 0.01)"
    print "\t-e, --depth: depth for horizontal slice in meters (e.g. 1000)"
    print "\t-c, --cvm: one of the installed velocity models"
    print "\t-o, --outfile: output filename containing list of lines from ucvm_query"
    print "\t-H, --help: optional display usage information"
    print "\t-i, --installdir: optional UCVM install directory"
    print "\t-n, --configfile: optional UCVM configfile"
    print "UCVM %s\n" % VERSION

ret_val = get_user_opts({"b,bottomleft":"lat1,lon1", \
                         "u,upperright":"lat2,lon2", \
                         "s,spacing":"spacing", \
                         "e,depth":"depth", \
                         "c,cvm":"cvm", \
                         "o,outfile":"outfile", \
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
    print "Plot ucvm_query return values for a map grid mesh Slice - UCVM %s" % VERSION
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
    meta['lon1']=lon1
    meta['lon2']=lon2
    meta['lat1']=lat1
    meta['lat2']=lat2

    # Check to see that this is a valid box.
    if lon1 > lon2 or lat1 > lat2:
        print "Error: (%.2f, %.2f) to (%.2f, %.2f) is not a valid box. Please re-run this script" % (lon1, lat1, lon2, lat2)
        print "and specify a valid region. The first point should be the lower-left corner, the"
        print "second point should be the upper-right corner."
        exit(1)

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

    # Ask which CVMs to use.
    print "\nFrom which CVM would you like this data to come:"

    counter = 1
    corresponding_cvm = []
    installdir = None
    configfile = None

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

# Now that we have all the requisite data, we can actually make the plot now.
print "Retrieving data. Please wait..."

# Generate the horizontal slice.
h = MapGridHorizontalSlice(Point(lon1, lat2, depth), Point(lon2, lat1, depth), meta)
h.plot()
