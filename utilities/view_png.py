#!/usr/bin/env python

##
#  @file view_png.py
#  @brief view a png file as a plot
#  @author - SCEC <>
#  @version 18.5.0
#
#  View a png file

import getopt, sys, os

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

## Prints usage of this utility.
def usage():
    print("Generates an image given a png file ")
    print("\t-f, --datafile: plot.png")

## Gets the options and assigns them to the correct variables.
def get_user_opts(options):
    
    short_opt_string = ""
    long_opts = []
    opts_left = []
    opts_opt = []
    ret_val = {}
    
    for key, value in options.items():
        short_opt_string = short_opt_string + key.split(",")[0] + ":"
        long_opts.append(key.split(",")[1])
        opts_left.append(key.split(",")[0])

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opt_string, long_opts)
    except getopt.GetoptError as err:
        print(str(err))   
        exit(1)
    
    for o, a in opts:
        for key, value in options.items():
            if o == "-" + key.split(",")[0] or o == "--" + key.split(",")[1]:
                opts_left.remove(key.split(",")[0])
                if "," in value:
                    ret_val[value.split(",")[0]] = a.split(",")[0]
                    ret_val[value.split(",")[1]] = a.split(",")[1]
                else:
                    ret_val[value] = a

# handle optional opts
    if len(opts_left) == 0 or len(opts_left) == len(opts_opt):
        return ret_val
    else:
        return "bad"

ret_val = get_user_opts({ "f,datafile":"datafile"}) 
if ret_val == "bad":
    usage()
    exit(1)
elif len(ret_val) > 0:
    print("Using parameters:\n")
    for key, value in ret_val.items():
        print(key , " = " , value)
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
    print("view_png  - UCVM %s" % VERSION)
    print("")
    print("This utility helps you display any image in png format")
    print("")

fig = plt.figure(figsize=(5, 5), dpi=100)
view=fig.add_subplot(1,1,1)
rawim=plt.imread(datafile)
view.imshow(rawim,cmap='gray')
plt.show()

