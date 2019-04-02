#!/usr/bin/env python

##
#  @file plot_cross_section_by_elevation.py
#  @brief Plots a cross section using command-line parameters.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Plots a cross section given a set of command-line parameters.

from pycvm import ElevationCrossSection, UCVM, VERSION, UCVM_CVMS, Point
import getopt, sys, os
import json
import pdb

## Prints usage statement.
def usage():
    print "Plots a cross-section given two latitude, longitude points, one or two elevations,"
    print "the CVM to plot, and a couple of other settings."
    print "\nValid arguments:"
    print "\t-s, --starting: starting elevation for cross-section (meters)"
    print "\t-e, --ending: ending elevation for cross-section (meters)"
    print "\t-h, --horizontal: horizontal spacing for cross-section (meters)"
    print "\t-v, --vertical: vertical spacing for cross-section (meters)"
    print "\t-d, --datatype: either 'vs', 'vp', 'rho', or 'poisson', without quotation marks"
    print "\t-c, --cvm: one of the installed CVMs"
    print "\t-a, --scale: color scale, either 's' for smooth, 'd' for discretized or 'b' for bi-color scale, without quotes"
    print "\t-g, --gate: optional gate value for bi-color scale gate"
    print "\t-b, --origin: origin latitude, longitude from which to start plot (e.g. 34,-118)"
    print "\t-u, --destination: destination latitude, longitude to end plot (e.g. 35,-117)"
    print "\t-f, --datafile: optional input filename"
    print "\t-o, --outfile: optional png output filename"
    print "\t-i, --installdir: optional UCVM install directory"
    print "UCVM %s\n" % VERSION

## Makes sure the response is a number.
def ask_number(question):
    temp_val = None
    
    while temp_val is None:
        temp_val = raw_input(question)
        try:
            float(temp_val)
            return float(temp_val)
        except ValueError:
            print temp_val + " is not a number. Please enter a number."
            temp_val = None
    
## Gets the options and assigns them to the correct variables.
def get_user_opts(options):
    
    short_opt_string = ""
    long_opts = []
    opts_left = []
    opts_opt = []
    ret_val = {}
    
    for key, value in options.iteritems():
        short_opt_string = short_opt_string + key.split(",")[0] + ":"
        long_opts.append(key.split(",")[1])
        opts_left.append(key.split(",")[0])

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opt_string, long_opts)
    except getopt.GetoptError as err:
        print str(err)   
        exit(1)
    
    if len(opts) == 0 :
        return {}

    for o, a in opts:
        for key, value in options.iteritems():
            if o == "-" + key.split(",")[0] or o == "--" + key.split(",")[1]:
                opts_left.remove(key.split(",")[0])
                if "," in value:
                    ret_val[value.split(",")[0]] = a.split(",")[0]
                    ret_val[value.split(",")[1]] = a.split(",")[1]
                else:
                    ret_val[value] = a

# handle optional opts
    for l in opts_left :
        if l == "o" :
          opts_opt.append(l)
          ret_val["outfile"] = None
        else :
            if l == "f" :
              opts_opt.append(l)
              ret_val["datafile"] = None
            else :
                if l == "g" :
                  opts_opt.append(l)
                  ret_val["gate"] = 2.5
                else:
                  if l == "i" :
                    opts_opt.append(l)
                    ret_val["installdir"] = None
    
    if len(opts_left) == 0 or len(opts_left) == len(opts_opt):
        return ret_val
    else:
        return "bad"

ret_val = get_user_opts({"b,origin":"lat1,lon1", \
			"u,destination":"lat2,lon2", \
                        "s,starting":"starting_elevation", \
			"e,ending":"ending_elevation", \
                        "d,datatype":"data_type", \
			"c,cvm":"cvm_selected", \
			"h,horizonatal":"horizontal_spacing", \
			"v,vertical":"vertical_spacing", \
			"a,scale": "color", \
			"g,gate": "gate", \
			"f,datafile":"datafile", \
                        "o,outfile":"outfile", \
                        "i,installdir":"installdir" })

meta = {}

if ret_val == "bad":
    usage()
    exit(1)
elif len(ret_val) > 0:
    print "Using parameters:\n"
    for key, value in ret_val.iteritems():
        print key , " = " , value
        meta[key] = value
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
    print "Plot Cross-Section - UCVM %s" % VERSION
    print ""
    print "This utility helps you plot a cross-section across the earth for one of the CVMs"
    print "that you installed with UCVM."
    print ""
    print "In order to create the plot, you must first specify the starting point."
    print ""

    lon1 = ask_number("Please enter the origin longitude from which the plot should start: ")
    lat1 = ask_number("Next, enter the origin latitude from which the plot should start: ")
    lon2 = ask_number("Enter the destination longitude where the plot should end: ")
    lat2 = ask_number("Enter the destination latitude where the plot should end: ")

    starting_elevation = 0 
    installdir = None
    print ""

    starting_elevation = ask_number("Please enter the elevation, in meters, at which you would like \n" + \
                                    "this cross-section to start: ")

    ending_elevation = 0 
    ending_elevation = ask_number("Please enter the elevation, in meters, at which you would like \n" + \
                                  "this cross-section to end: ")

    if ending_elevation >= starting_elevation:
        print "Error: the bottom, ending elevation must be less than the starting elevation."
 
    horizontal_spacing = -1
    print ""

    while horizontal_spacing < 0:
        horizontal_spacing = ask_number("Please enter the horizontal spacing, in meters, for the plot: ")
        if horizontal_spacing < 0:
            print "Error: the spacing must be a positive number."

    vertical_spacing = -1
    while vertical_spacing < 0:
        vertical_spacing = ask_number("Please enter the vertical spacing, in meters, for the plot: ")
        if vertical_spacing < 0:
            print "Error: the spacing must be a positive number."   

    print ""

    data_type = ""

    while data_type != "vs" and data_type != "vp" and data_type != "density":
        data_type = raw_input("What would you like to plot (either vp, vs, or density): ")
        data_type = data_type.lower().strip()
    
        if data_type != "vs" and data_type != "vp" and data_type != "density":
            print "Error: you must select either 'vp', 'vs', 'density' (without quotation marks)."

    # Ask which CVMs to use.
    print "\nFrom which CVM would you like this data to come:"

    counter = 1
    corresponding_cvm = []

    # Create a new UCVM object.
    u = UCVM(install_dir=installdir)

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

    # We will offer two color options. Discretized or smooth. But, we'll only offer red-blue for now.
    gate = 2.5
    color = ""

    while color != "s" and color != "d" and color != "b" and data_type != "poisson":
        print ""
        color = raw_input("Finally, would you like a descritized or smooth color scale\n(enter 'd' for discrete, 's' for smooth, 'b' for bi-color): ")
        color = color.strip()
    
        if color != "s" and color != "d" and color != "b":
            print "Please enter 'd' (without quotation marks) for a discrete color bar and 's' (without quotation"
            print "marks) for a smooth color scale and 'b' (without quotation marks) for bi-color scale."

# Now we have all the information so we can actually plot the data.
print ""
print "Retrieving data. Please wait..."

# Generate the horizontal slice.

d = ElevationCrossSection(Point(lon1, lat1, elevation=starting_elevation), Point(lon2, lat2, elevation=starting_elevation), \
                 ending_elevation, horizontal_spacing, vertical_spacing, cvm_selected)

d.plot(data_type,filename=outfile, datafile=datafile, color_scale=color,scale_gate=gate, meta=meta)
