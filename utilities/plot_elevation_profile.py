#!/usr/bin/env python

##
#  @file plot_elevation_profile.py
#  @brief Plots a elevation profile using command-line parameters.
#  @author 
#  @version 
#
#  Plots a elevation profile given a set of command-line parameters.

from pycvm import ElevationProfile, UCVM, VERSION, UCVM_CVMS, Point
import getopt, sys, os

## Prints usage statement.
def usage():
    print "Plots a elevation profile given a latitude, longitude, a elevation,"
    print "the CVM to plot, and a couple of other settings."
    print "\nValid arguments:"
    print "\t-s, --startingpoint: latitude, longitude (e.g. 34,-118)"
    print "\t-b, --startingelevation: starting elevation for elevation profile (meters)"
    print "\t-e, --endingelevation: ending elevation for elevation profile (meters)"
    print "\t-d, --datatype: one or more 'vs', 'vp' and/or 'density'(e.g. vs,vp,density)"
    print "\t-v, --vertical: vertical spacing for elevation interval (meters)"
    print "\t-c, --cvm: one of the installed CVMs"
    print "\t-g, --threshold: optional  Vs threshold to display as gating"
    print "\t-o, --outfile: optional png output filename"
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
            if l == "g" :
              opts_opt.append(l)
              ret_val["vs_threshold"] = None

    if len(opts_left) == 0 or len(opts_left) == len(opts_opt):
        return ret_val
    else:
        return "bad"

starting_elevation = 0

ret_val = get_user_opts({ "s,startingpoint":"lat1,lon1", \
			"b,startingelevation":"starting_elevation", \
			"e,endingelevation":"ending_elevation", \
			"c,cvm":"cvm_selected", \
			"d,datatype":"data_type", \
			"v,vertical":"vertical_spacing", \
			"g,gating":"vs_threshold", \
			"o,outfile":"outfile"})

# Create a new UCVM object.
u = UCVM()

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
    print "Plot Elevation-Profile - UCVM %s" % VERSION
    print ""
    print "This utility helps you plot a elevation-profile for one of the CVMs"
    print "that you installed with UCVM."
    print ""
    print "In order to create the plot, you must first specify the grid point."
    print ""

    lon1 = ask_number("Please enter the longitude: ")
    lat1 = ask_number("Next, enter the latitude: ")

    starting_elevation = 0  ## default, 0
    starting_elevation = ask_number("Please enter the elevation, in meters, at which you would like \n" + \
                                  "this plot to start: ")

    ending_elevation = -150000  ## max, -15000
    ending_elevation = ask_number("Please enter the elevation, in meters, at which you would like \n" + \
                                  "this plot to end: ")

    if ending_elevation >= starting_elevation:
        print "Error: the bottom, ending elevation must be less than the starting elevation."
 
    print ""
    vertical_spacing = -1
    while vertical_spacing < 0:
        vertical_spacing = ask_number("Please enter the vertical spacing, in meters, for the plot: ")
        if vertical_spacing < 0:
            print "Error: the spacing must be a positive number."   

    print ""

    data_type = [] 
    while True:
        dtype = raw_input("What would you like to plot (either vp, vs, or density): ")
        if dtype == "":
            break;

        dtype = data_type.lower().strip()
    
        if dtype != "vs" and dtype != "vp" and dtype != "density":
            print "Error: you must select either 'vp', 'vs', 'density' (without quotation marks)."
        else:
            data_type.append(dtype)	    

    # Ask which CVMs to use.
    print "\nFrom which CVM would you like this data to come:"

    counter = 1
    corresponding_cvm = []

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

# Now we have all the information so we can actually plot the data.
print ""
print "Retrieving data. Please wait..."

# Generate the elevation profile

d = ElevationProfile(Point(lon1, lat1, elevation=starting_elevation),
         ending_elevation, vertical_spacing, cvm_selected, threshold=vs_threshold)

d.plot(data_type, filename=outfile, meta=meta)

