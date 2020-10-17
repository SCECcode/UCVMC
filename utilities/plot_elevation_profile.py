#!/usr/bin/env python3

##
#  @file plot_elevation_profile.py
#  @brief Plots a elevation profile using command-line parameters.
#  @author 
#  @version 
#
#  Plots a elevation profile given a set of command-line parameters.

from pycvm import ElevationProfile, UCVM, VERSION, UCVM_CVMS, Point, ask_number, ask_path, ask_file, get_user_opts
import getopt, sys, os

## Prints usage statement.
def usage():
    print("Plots a elevation profile given a latitude, longitude, a elevation,")
    print("the CVM to plot, and a couple of other settings.")
    print("\nValid arguments:")
    print("\t-s, --startingpoint: latitude, longitude (e.g. 34,-118)")
    print("\t-b, --startingelevation: starting elevation for elevation profile (meters)")
    print("\t-e, --endingelevation: ending elevation for elevation profile (meters)")
    print("\t-d, --datatype: one or more 'vs', 'vp' and/or 'density'(e.g. vs,vp,density)")
    print("\t-v, --vertical: vertical spacing for elevation interval (meters)")
    print("\t-c, --cvm: one of the installed CVMs")
    print("\t-z, --zrange: optional Z-range for elygtl:ely (e.g. -z 0,350)")
    print("\t-g, --threshold: optional  Vs threshold to display as gating")
    print("\t-f, --datafile: optional binary input data filename")
    print("\t-o, --outfile: optional png output filename")
    print("\t-t, --title: optional plot title")
    print("\t-H, --help: optional display usage information")
    print("\t-i, --installdir: optional UCVM isntall directory")
    print("\t-n, --configfile: optional UCVM configfile")
    print("UCVM %s\n" % VERSION)

ret_val = get_user_opts({"s,startingpoint":"lat1,lon1", \
			 "b,startingelevation":"starting_elevation", \
			 "e,endingelevation":"ending_elevation", \
			 "c,cvm":"cvm", \
			 "d,datatype":"data_type", \
			 "v,vertical":"vertical_spacing", \
                         "z,zrange,o":"zrange1,zrange2", \
			 "g,gating,o":"vs_threshold", \
                         "f,datafile,o":"datafile", \
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
    print("Using parameters:\n")
    for key, value in ret_val.iteritems():
        print(key , " = " , value)
        meta[key] = value
        try:
            float(value)
            exec("%s = float(%s)" % (key, value))
        except Exception:
            if value is None:
                exec("%s = %s" % (key, value))
            else:
                exec("%s = '%s'" % (key, value))
else: 
    print("")
    print("Plot Elevation-Profile - UCVM %s" % VERSION)
    print("")
    print("This utility helps you plot a elevation-profile for one of the CVMs")
    print("that you installed with UCVM.")
    print("")
    print("In order to create the plot, you must first specify the grid point.")
    print("")

    lon1 = ask_number("Please enter the longitude: ")
    lat1 = ask_number("Next, enter the latitude: ")

    meta['lon1']=lon1
    meta['lat1']=lat1

    starting_elevation = 0  ## default, 0
    starting_elevation = ask_number("Please enter the elevation, in meters, at which you would like \n" + \
                                  "this plot to start: ")
    meta['starting_elevation']=staring_elevation

    ending_elevation = -15000  ## max, -15000
    ending_elevation = ask_number("Please enter the elevation, in meters, at which you would like \n" + \
                                  "this plot to end: ")

    if ending_elevation >= starting_elevation:
        print("Error: the bottom, ending elevation must be less than the starting elevation.")
    meta['ending_elevation']=ending_elevation
 
    print("")
    vertical_spacing = -1
    while vertical_spacing < 0:
        vertical_spacing = ask_number("Please enter the vertical spacing, in meters, for the plot: ")
        if vertical_spacing < 0:
            print("Error: the spacing must be a positive number.")   
    meta['vertical_spacing']=vertical_spacing

    print("")

    data_type = [] 
    while True:
        dtype = raw_input("What would you like to plot (either vp, vs, or density): ")
        if dtype == "":
            break;

        dtype = data_type.lower().strip()
    
        if dtype != "vs" and dtype != "vp" and dtype != "density":
            print("Error: you must select either 'vp', 'vs', 'density' (without quotation marks).")
        else:
            data_type.append(dtype)	    
    meta['mproperty']=data_type


    # Ask if a different installdir should be  used
    cwd = os.getcwd()
    installdir = ask_path("Do you want to use different UCVM install directory", cwd+"/..")
    # Ask if a different ucvm.conf should be  used
    configfile = ask_file("Do you want to use different ucvm.conf file", cwd+"/../ucvm.conf")

    # Ask which CVMs to use.
    print("From which CVM would you like this data to come:")

    # Create a new UCVM object.
    u = UCVM(install_dir=installdir, config_file=configfile)

    for cvm in u.models:
        cvmtoprint = cvm
        if cvm in UCVM_CVMS:
            cvmtoprint = UCVM_CVMS[cvm]
        corresponding_cvm.append(cvm)
        print("\t%d) %s" % (counter, cvmtoprint))
        counter += 1
    
    cvm_selected = -1
    while cvm_selected < 0 or cvm_selected > counter:
        cvm_selected = int(ask_number("\nSelect the CVM: ")) - 1
    
        if cvm_selected < 0 or cvm_selected > counter:
            print("Error: the number you selected must be between 1 and %d" % counter)

    cvm_selected = corresponding_cvm[cvm_selected]
    meta['cvm']=cvm_selected

# Now we have all the information so we can actually plot the data.
print("")
print("Retrieving data. Please wait...")

###################################################################################
# Generate the elevation profile
d = ElevationProfile(Point(lon1, lat1, elevation=starting_elevation), meta)
d.plot()

