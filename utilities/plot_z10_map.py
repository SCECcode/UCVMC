#!/usr/bin/env python

##
#  @file plot_z10_slice.py
#  @brief Plots a Z1.0 slice using command-line parameters.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Plots a Z1.0 slice given a set of command-line parameters.

from pycvm import Z10Slice, UCVM, VERSION, UCVM_CVMS, Point, ask_number, ask_path, ask_file, get_user_opts
import getopt, sys, os

## Prints usage of this utility.
def usage():
    print "Generates a Z1.0 map or text file given two bounding latitude and longitude "
    print "co-ordinates, the CVM to plot, and a couple of other settings."
    print "\nValid arguments:"
    print "\t-b, --bottomleft: bottom-left latitude, longitude (e.g. 34,-118)"
    print "\t-u, --upperright: upper-right latitude, longitude (e.g. 35,-117)"
    print "\t-s, --spacing: grid spacing in degrees (typically 0.01)"
    print "\t-z, --interval: Z-interval, in meters, for Z%.1f to be queried (lower value means more precision)"
    print "\t-c, --cvm: one of the installed CVMs"
    print "\t-a, --scale: color scale, either 's' for smooth or 'd' for discretized, without quotes"
    print "\t-f, --datafile: optional binary input data filename"
    print "\t-x, --x: optional x steps matching the datafile"
    print "\t-y, --y: optional y steps matching the datafile"
    print "\t-o, --outfile: optional png output filename"
    print "\t-t, --title: optional plot title"
    print "\t-H, --help: display usage information"
    print "\t-i, --installdir: optional UCVM install directory"
    print "\t-g, --configfile: optional UCVM configfile"
    print "UCVM %s\n" % VERSION


meta = {}

ret_val = get_user_opts({"b,bottomleft":"lat1,lon1", \
                         "u,upperright":"lat2,lon2", \
                         "s,spacing":"spacing", \
                         "c,cvm":"cvm", \
                         "f,datafile,o":"datafile", \
                         "o,outfile,o":"outfile", \
                         "x,nx,o":"nx", \
                         "y,ny,o":"ny", \
                         "a,scale": "color", \
                         "t,title,o":"title", \
                         "H,help,o":"", \
                         "i,installdir,o":"installdir", \
                         "g,configfile,o":"configfile" })

if ret_val == "bad":
    usage()
    exit(1)
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
    useMPI = "n"

else:      
    print ""
    print "Z1.0  - UCVM %s" % (VERSION)
    print ""
    print "This utility helps you either plot a Z1.0 basin depth map or save the data in a"
    print "text file that you can then later parse."
    print ""
    print "In order to create the plot, you must first specify the region."
    print ""


    lon1 = ask_number("Please enter the bottom-left longitude from which the Z1.0 values should come: ")
    lat1 = ask_number("Next, enter the bottom-left latitude from which the Z1.0 values should come: ")
    lon2 = ask_number("Enter the top-right longitude where the Z1.0 values should end: ")
    lat2 = ask_number("Enter the top-right latitude where the Z1.0 values should end: ")

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
    print "From which CVM would you like this data to come:"

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

    color = ""
    while color != "s" and color != "d" and data_type != "poisson":
        print ""
        color = raw_input("Finally, would you like a descritized or smooth color scale\n(enter 'd' for discrete, 's' for smooth): ")
        color = color.strip()

        if color != "s" and color != "d":
            print "Please enter 'd' (without quotation marks) for a discrete color bar and 's' (without quotation"
            print "marks) for a smooth color scale."
    meta['color']=color



###################################################################################
# Generate the Z10 horizontal slice.
b = Z10Slice(Point(lon1, lat2, 0), Point(lon2, lat1, 0), meta)
b.plot(meta=meta)
