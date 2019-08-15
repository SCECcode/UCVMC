##
#  @file common.py
#  @brief Common definitions and functions for all the UCVM plotting scripts.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Provides common definitions and functions that are shared amongst all UCVM
#  plotting scripts. Facilitates easier multi-processing as well.

#  Imports
from subprocess import call, Popen, PIPE, STDOUT
import sys
import os
import multiprocessing
import math
import struct
import getopt
import pdb
import json

#  Numpy is required.
try:
    import numpy as np
except StandardError, e:
    print "ERROR: NumPy must be installed on your system in order to generate these plots."
    exit(1)
    
#  Matplotlib is required.
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
    import matplotlib.cm as cm
except StandardError, e:
    print "ERROR: Matplotlib must be installed on your system in order to generate these plots."
    exit(1)    

#  Basemap is required.
try:
    from mpl_toolkits import basemap
except StandardError, e:
    print "ERROR: Basemap Toolkit must be installed on your system in order to generate these plots."
    exit(1)

#  Constants

## Known CVMs that can be installed with UCVM.
UCVM_CVMS = {"1d":"1D(1d)", \
             "1dgtl":"1D w/ Vs30 GTL(1dgtl)", \
             "bbp1d":"Broadband Northridge Region 1D Model(bbp1d)", \
             "cvms":"CVM-S4(cvms)", \
             "cvms5":"CVM-S4.26(cvms5)", \
             "cvms426":"CVM-S4.26.M01(cvmsi)", \
             "cca":"CCA 06(cca)", \
             "cs173":"CyperShake 17.3(cs173)", \
             "cs173h":"CyperShake 17.3 with San Joaquin and Santa Maria Basins data(cs173h)", \
             "cvmh1511":"CVM-H 15.1.1(cvmh)", \
             "cencal":"USGS Bay Area Model(cencal)"}

## Constant for all material properties.
ALL_PROPERTIES = ["vp", "vs", "density"]
## Constant for just Vs.
VS = ["vs"]
## Constant for just Vp.
VP = ["vp"]
## Constant for just density.
DENSITY = ["density"]

## Version string.
VERSION = "19.4.0"

#  Class Definitions

## Common Access Functions

global ask_number
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

    
global ask_path
## get optional answer
def ask_path(question,target):
    temp_val = raw_input(question + target+", Enter different path or blank :")

    if temp_val.strip() == "":
        temp_val = target
        return temp_val

    while temp_val is not "":
    # Check to see that that path exists
        if os.exists(temp_val) and os.isdir(tmp_val) :
            return temp_val
        else :
            print "\n" + temp_val + " does not exist or not a directory"
            temp_val= raw_input("Please enter a different path or blank to use the default path: ")
    return target

global ask_file
## get optional answer
def ask_file(question,target):
    temp_val = raw_input(question + target+", Enter different file or blank :")

    if temp_val.strip() == "":
        temp_val = target
        return temp_val

    while temp_val is not "":
    # Check to see that that file exists
        if os.exists(temp_val) and os.isfile(tmp_val) :
            return temp_val
        else :
            print "\n" + temp_val + " does not exist or not a file"
            temp_val= raw_input("Please enter a different file or blank to use the default file: ")
    return target


## Gets the options and assigns them to the correct variables.
#
#"option short-form, optionlong-form, optional": "meta variable"
#{"b,bottomleft":"lat1,lon1", \
# "u,upperright":"lat2,lon2", \
# ...
# "t,title,o":"title", \
# "H,help,o":"" })
#
global get_user_opts
def get_user_opts(options):
        
    short_opt_string = ""
    long_opts = []
    opts_left = []
    opts_opt = []
    optional_opts = []
    ret_val = {}

    for key, value in options.iteritems():
        items=key.split(",")
        short_opt_string = short_opt_string + items[0] 
        if value != "" :
            short_opt_string = short_opt_string + ":"
        long_opts.append(items[1])
        opts_left.append(items[0])
        if len(items) > 2 and items[2] != None  and items[2] =='o' :
            optional_opts.append(key.split(",")[0])

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opt_string, long_opts)
    except getopt.GetoptError as err:
        print str(err)   
        exit(1)

    if len(opts) == 0 :
        return {}

    for o, a in opts:
## special case
        if o == "-H" or o == "--help" :
            return "help"
## regular case
        for key, value in options.iteritems():
            if o == "-" + key.split(",")[0] or o == "--" + key.split(",")[1]:
                opts_left.remove(key.split(",")[0])
                if "," in value:
                    ret_val[value.split(",")[0]] = a.split(",")[0]
                    ret_val[value.split(",")[1]] = a.split(",")[1]
                else:
                    ret_val[value] = a
                break

    for l in opts_left :
        if l in optional_opts :
          opts_opt.append(l)

    if len(opts_left) == 0 or len(opts_left) == len(opts_opt):
        return ret_val
    else: 
        return "bad"


#  Class Definitions

##
#  @class Plot
#  @brief Returns a basic plot given a set of parameters.
#
#  This forms the basis for generating a plot using this suite of tools.
#  It returns a Matplotlib plot with certain parameters already set up.
class Plot:
    
    ##
    #  Initializes the Plot with a set of basic parameters. Use the
    #  addsubplot() method to add a sub-plot to the plot.
    #
    #  @param title The title for the plot.
    #  @param xlabel The label to be displayed on the x-axis.
    #  @param ylabel The label for the y-axis.
    #  @param legend A legend to be displayed on the lower left of the plot.
    #  @param width The width of the plot in inches (dpi = 100).
    #  @param height The height of the plot in inches (dpi = 100).
    def __init__(self, title = None, xlabel = None, ylabel = None, legend = None, width = 10, height = 10):
        ## Defines the figure object to which we can add subplots.
        self.figure = plt.figure(figsize=(width, height), dpi=100)
        
        if ylabel != None:
            plt.ylabel(ylabel, fontsize=14)
        
        if xlabel != None:
            plt.xlabel(xlabel, fontsize=14)  
        
        if title != None:
            plt.title(title)
        
        if legend != None:
            plt.legend(legend, loc='lower left')
            
        ## Internal counter for how many subplots we have.
        self.subplotcounter = 1
            
    ##
    #  Adds a subplot to the figure and returns it.
    # 
    #  @return The subplot that has been added to the already generated plot.
    def addsubplot(self):
        retval = self.figure.add_subplot(1, 1, 1)
        self.subplotcounter += 1;
        return retval
    
    ## 
    #  Shows the plot.
    def show(self):
        plt.show()
        
    ##
    #  Saves the figure to disk.
    #
    #  @param filename The name fo the file to save.
    def savefig(self, filename):
        plt.savefig(filename)

## MEI ToDO
    def savehtml(self, filename):
        import mpld3
#        mpld3.save_html(self.figure,filename)
#        mpld3.save_json(self.figure, filename)
        mpld3.fig_to_dict(self.figure)

##
#  @class Point
#  @brief Defines a point in WGS84 latitude, longitude projection.
#
#  Allows for a point to be defined within the 3D earth structure.
#  It has a longitude, latitude, and depth/elevation as minimum parameters,
#  but you can specify a type, e.g. "LA Basin", and a description, 
#  e.g. "New point of interest".
class Point:
    
    ##
    #  Initializes a new point. Checks that the parameters are all valid and
    #  raises an error if they are not.
    # 
    #  @param longitude Longitude provided as a float.
    #  @param latitude Latitude provided as a float.
    #  @param depth The depth in meters with the surface being 0.
    #  @param elevation The elevation in meters.
    #  @param type The type or classification of this location. Not required.
    #  @param code A short code for the site (unique identifier). Not required.
    #  @param description A longer description of what this point represents. Not required.
    def __init__(self, longitude, latitude, depth = 0, elevation = None, type = None, code = None, description = None):
        if pycvm_is_num(longitude):
            ## Longitude as a float in WGS84 projection.
            self.longitude = longitude
        else:
            raise TypeError("Longitude must be a number")
        
        if pycvm_is_num(latitude):
            ## Latitude as a float in WGS84 projection.
            self.latitude = latitude
        else:
            raise TypeError("Latitude must be a number")

        self.elevation = None;
        if elevation != None :
            self.elevation = elevation
        
        if pycvm_is_num(depth):
            if depth >= 0:
                ## Depth in meters below the surface. Must be greater than or equal to 0.
                self.depth = depth
            else:
                raise ValueError("Depth must be positive.")
        else:
            raise TypeError("Depth must be a number.")
        
        ## A classification or short description of what this point represents. Optional.
        self.type = type
        ## A short, unique code identifying the site. Optional.
        self.code = code
        ## A longer description of what this point represents. Optional.
        self.description = description
    
    ##
    #  String representation of the point.    
    def __str__(self):
        if(self.elevation) :
            return "(%.4f, %.4f, %.4f)" % (float(self.longitude), float(self.latitude), float(self.elevation))
        else:
            return "(%.4f, %.4f, %.4f)" % (float(self.longitude), float(self.latitude), float(self.depth))

##
#  @class MaterialProperties
#  @brief Defines the possible material properties that @link UCVM UCVM @endlink can return.
#
#  Provides a class for defining the three current material properties that
#  UCVM returns and also has placeholders for Qp and Qs.
class MaterialProperties:
    
    ## 
    #  Initializes the MaterialProperties class.
    #  
    #  @param vp P-wave velocity in m/s. Must be a float.
    #  @param vs S-wave velocity in m/s. Must be a float.
    #  @param density Density in g/cm^3. Must be a float.
    #  @param poisson Poisson as a calculated float. Optional.
    #  @param qp Qp as a float. Optional.
    #  @param qs Qs as a float. Optional.
    def __init__(self, vp, vs, density, poisson = None, qp = None, qs = None):
       if pycvm_is_num(vp):
           ## P-wave velocity in m/s
           self.vp = float(vp)
       else:
           raise TypeError("Vp must be a number.")
       
       if pycvm_is_num(vs):
           ## S-wave velocity in m/s
           self.vs = float(vs)
       else:
           raise TypeError("Vs must be a number.")
       
       if pycvm_is_num(density):
           ## Density in g/cm^3
           self.density = float(density)
       else:
           raise TypeError("Density must be a number.")

       if poisson != None:
           self.poisson = float(poisson)
       else:
           self.poisson = -1
       
       if qp != None:
           ## Qp
           self.qp = float(qp)
       else:
           self.qp = -1
           
       if qs != None:
           ## Qs
           self.qs = float(qs)
       else:
           self.qs = -1
       
    ##
    #  Defines subtraction of two MaterialProperties classes.
    #
    #  @param own This MaterialProperties class.
    #  @param other The other MaterialProperties class.
    #  @return The subtracted properties.
    def __sub__(own, other):
        return MaterialProperties(own.vp - other.vp, own.vs - other.vs, own.density - other.density, \
                                  own.poisson - other.poisson, own.qp - other.qp, own.qs - other.qs)

    ##
    #  Initializes the class from a UCVM output string line.
    #
    #  @param cls Not used. Call as MaterialProperties.fromUCVMOutput(line).
    #  @param line The line containing the material properties as generated by ucvm_query.
    #  @return A constructed MaterialProperties class.
    @classmethod
    def fromUCVMOutput(cls, line):
        new_line = line.split()
        return cls(new_line[14], new_line[15], new_line[16])

    ##
    #  Initializes the class from a JSON  output string line.
    #
    #  @param cls Not used. Call as MaterialProperties.fromJSONOutput(jdict).
    #  @param jdict The jdict line containing the material properties as imported from file
    #  @return A constructed MaterialProperties class.
    @classmethod
    def fromJSONOutput(cls, jdict):
        vp=jdict['vp']
        vs=jdict['vs']
        density=jdict['density']
        return cls(vp, vs, density)

    ##
    #  Create a JSON output string line
    #
    #  @param depth The depth from surface.
    #  @return A JSON string
    def toJSON(self, depth):
        return "{ 'depth':%2f, 'vp':%.5f, 'vs':%.5f, 'density':%.5f }" % (depth, self.vp, self.vs, self.density)
    
    ##
    #  Retrieves the corresponding property given the property as a string.
    # 
    #  @param property The property name as a string ("vs", "vp", "density", "poisson", "qp", or "qs").
    #  @return The property value.
    def getProperty(self, property):               
        if property.lower() == "vs":
            return self.vs
        elif property.lower() == "vp":
            return self.vp
        elif property.lower() == "density":
            return self.density
        elif property.lower() == "poisson":
            return self.poisson
        elif property.lower() == "qp":
            return self.qp
        elif property.lower() == "qs":
            return self.qs
        else:
            raise ValueError("Parameter property must be a valid material property unit.")
    ##
    #  Set the corresponding property given the property as a string.
    # 
    #  @param property The property name as a string ("vs", "vp", "density", "qp", or "qs").
    #  @param val The property value.
    def setProperty(self, property, val):               
        if property.lower() == "vs":
            self.vs=val
        elif property.lower() == "vp":
            self.vp=val
        elif property.lower() == "density":
            self.density=val
        elif property.lower() == "poisson":
            self.poisson=val
        elif property.lower() == "qp":
            self.qp=val
        elif property.lower() == "qs":
            self.qs=val
        else:
            raise ValueError("Parameter property must be a valid material property unit.")
        
    ##
    #  String representation of the material properties.
    def __str__(self):
        return "Vp: %.2fm/s, Vs: %.2fm/s, Density: %.2fg/cm^3" % (self.vp, self.vs, self.density)
 
##
#  @class UCVM
#  @brief Python functions to interact with the underlying C code.
#
#  Provides a Python mechanism for calling the underlying C programs and
#  getting their output in a format that is readily and easily interpreted
#  by other classes.
class UCVM:
    
    ##
    #  Initializes the UCVM class and reads in all the available models that have
    #  been installed.
    #  
    #  @param install_dir The base installation directory of UCVM.
    #  @param config_file The location of the UCVM configuration file.
    def __init__(self, install_dir = None, config_file = None, z_range = None):
        if install_dir != None:
            ## Location of the UCVM binary directory.
            self.binary_dir = install_dir + "/bin"
        else:
            self.binary_dir = "../bin"
        
        if config_file != None:
            ## Location of the UCVM configuration file.
            self.config = config_file
        else:
            if install_dir != None:
               self.config = install_dir + "/conf/ucvm.conf"
            else:
               self.config = "../conf/ucvm.conf"

        if z_range != None:
            self.z_range = z_range
        else:
            self.z_range= None
        
        if install_dir != None:
            ## List of all the installed CVMs.
            self.models = [x for x in os.listdir(install_dir + "/model")]
        else:
            self.models = [x for x in os.listdir("../model")]
            
        self.models.remove("ucvm")

    ##
    #  Given raw UCVM result
    #   this function will throw an an error: missing model or invalid data etc
    #   by checking if first 'item' is float or not
    #
    #  @param raw An array of output material properties
    def checkUCVMoutput(self,idx,rawoutput):
        output = rawoutput.split("\n")[idx:-1]
        if len(output) > 1:
            line = output[0]
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo" in line):
                return output
            p=line.split()[0]
            try :
                f=float(p)
            except :
                print "ERROR: ", line
                exit(1)
           
        return output

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def query(self, point_list, cvm, elevation = None):
        
        shared_object = "../model/" + cvm + "/lib/lib" + cvm + ".so"
        properties = []
        
        # Can we load this library dynamically and bypass the C code entirely?
        if os.path.isfile(shared_object):
            import ctypes
            #obj = ctypes.cdll.LoadLibrary(shared_object)
            #print obj
        
#        print "CVM", cvm
        if( elevation ) :
            if self.z_range != None :
#                print "RANGE", self.z_range
#                print "CVM", cvm 
                proc = Popen([self.binary_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "ge", "-z", self.z_range], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            else :
                proc = Popen([self.binary_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "ge"], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        else :
            if self.z_range != None :
#                print "RANGE", self.z_range
#                print "CVM", cvm 
                proc = Popen([self.binary_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "gd", "-z", self.z_range], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
            else:
                proc = Popen([self.binary_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm, "-c", "gd" ], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            if( elevation ) :
              text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.elevation)
            else:
              text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)

        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
# it is material properties.. line
            try :
              mp = MaterialProperties.fromUCVMOutput(line)
              properties.append(mp)
            except :
              pass


        if len(properties) == 1:
            return properties[0]

        return properties

    ##
    #  Gets the Poisson value for a given set of Vs, Vp pair
    #  @param vs 
    #  @param vp
    #  @return poisson value
    def poisson(self, vs, vp) :
       if vs == 0 :
          return 0.0

       if vp == 0 :
          return 0.0

       return vp/vs

    ##
    #  Gets the Poisson value for a given set of Vs, Vp pair base on
    #  https://www.glossary.oilfield.slb.com/en/Terms/p/poissons_ratio.aspx
    #  @param vs 
    #  @param vp
    #  @return poisson value
    def poissonComplex(self, vs, vp) :
       if vs == 0 :
          return 0.5

       b=(vp * vp) - (vs * vs)
       t=((vp * vp) - 2*(vs * vs))/2

       if(b == 0) :
          return 0.0

       val = t/b
       return val

    ##
    #  Gets the Vs30 values for a given set of points and a CVM to query. If
    #  the CVM does not exist, this function will throw an error. The set of
    #  points is an array of @link Point Points @endlink. The function returns
    #  the Vs30 values as floats.
    #
    #  @param point_list An array of @link Point Points @endlink to query.
    #  @param cvm The CVM from which the Vs30 data should be retrieved.
    #  @return An array of floats which correspond to the points provided.
    def vs30(self, point_list, cvm):
        
        proc = Popen([self.binary_dir + "/vs30_query", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        text_points = ""
        floats = []
        
        if isinstance(point_list, Point):
            point_list = [point_list]
        
        for point in point_list:
            text_points += "%.5f %.5f\n" % (point.longitude, point.latitude)
            
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(0,output)
        
        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                 print "skipping text",line
            else:
                 try :
                     p=float(line.split()[2])
                 except :
                     print "ERROR: should be a float."
                     exit(1)
                 floats.append(p)
        
        if len(floats) == 1:
            return floats[0]
            
        return floats


    ##
    #  Gets the basin depths for a given set of points, CVM, and desired Vs.
    #  If the CVM does not exist, an error is given. The set of points is an
    #  array of @link Point Points @endlink. The function returns the depths
    #  as floats.
    # 
    #  @param point_list An array of @link Point Points @endlink to query.
    #  @param cvm The CVM from which the depths should come.
    #  @param vs_threshold The Vs threshold to check for (e.g. Z1.0 = 1000).
    #  @return An array of floats which correspond to the depths.
    def basin_depth(self, point_list, cvm, vs_threshold):

        proc = Popen([self.binary_dir + "/basin_query", "-f", self.config, "-m", \
                      cvm, "-v", "%.0f" % vs_threshold], stdout=PIPE, stdin=PIPE, stderr=STDOUT)

        text_points = ""
        floats = []

        if isinstance(point_list, Point):
            point_list = [point_list]

        for point in point_list:
            text_points += "%.5f %.5f\n" % (point.longitude, point.latitude)

        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(0,output)

        for line in output:
            try :
                p=float(line.split()[2])
            except :
                print "ERROR: should be a float."
                exit(1)
            floats.append(p)

        if len(floats) == 1:
            return floats[0]

        return floats

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def elevation_etree(self, point_list, cvm):
        
        shared_object = "../model/" + cvm + "/lib/lib" + cvm + ".so"
        properties = []
        
        # Can we load this library dynamically and bypass the C code entirely?
        if os.path.isfile(shared_object):
            import ctypes
            #obj = ctypes.cdll.LoadLibrary(shared_object)
            #print obj
        
        proc = Popen([self.binary_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)
            # print "%.5f %.5f %.5f" % (point.longitude, point.latitude, point.depth)
        
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                print "skipping text",line
            else:
                # Position 3 returned by ucvm_query is a elevation in the etree. Return this value
                try:
                    p=float(line.split()[3])
                except:
                    print "ERROR: should be a float value."
                    exit(1)
                properties.append(p)

        if len(properties) == 1:
            return properties[0]
        
        return properties

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def map_grid(self, point_list, cvm):
        
        shared_object = "../model/" + cvm + "/lib/lib" + cvm + ".so"
        properties = []
        
        # Can we load this library dynamically and bypass the C code entirely?
        if os.path.isfile(shared_object):
            import ctypes
            #obj = ctypes.cdll.LoadLibrary(shared_object)
            #print obj
        
        proc = Popen([self.binary_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)
            #  print "%.5f %.5f %.5f" % (point.longitude, point.latitude, point.depth)
        
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                print "skipping text",line
            else:
                # print "line:",line
                # return the whole line which will be printed to file
                properties.append(line)

        if len(properties) == 1:
            return properties[0]
        
        return properties

    ##
    #  Queries UCVM given a set of points and a CVM to query. If the CVM does not exist,
    #  this function will throw an error. The set of points must be an array of the 
    #  @link Point Point @endlink class. This function returns an array of @link MaterialProperties
    #  MaterialProperties @endlink.
    #
    #  @param point_list An array of @link Point Points @endlink for which UCVM should query.
    #  @param cvm The CVM from which this data should be retrieved.
    #  @return An array of @link MaterialProperties @endlink.
    def vs30_etree(self, point_list, cvm):
        
        shared_object = "../model/" + cvm + "/lib/lib" + cvm + ".so"
        properties = []
        
        # Can we load this library dynamically and bypass the C code entirely?
        if os.path.isfile(shared_object):
            import ctypes
            #obj = ctypes.cdll.LoadLibrary(shared_object)
            #print obj
        
        proc = Popen([self.binary_dir + "/run_ucvm_query.sh", "-f", self.config, "-m", cvm], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        
        text_points = ""
        
        if isinstance(point_list, Point):
            point_list = [point_list]
         
        for point in point_list:
            text_points += "%.5f %.5f %.5f\n" % (point.longitude, point.latitude, point.depth)
            # print "%.5f %.5f %.5f" % (point.longitude, point.latitude, point.depth)
        
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(1,output)

        for line in output:
            if ("WARNING" in line) or ("slow performance" in line) or ("Using Geo Depth coordinates as default mode" in line):
                print "skipping text",line
            else:
                #print "line:",line
                # return position 4 from ucvm_query is the etree vs30 value. return that
                try :
                   p=float(line.split()[4])
                except :
                   print "ERROR: should be a float."
                   exit(1)
                properties.append(p)

        if len(properties) == 1:
            return properties[0]
        
        return properties

    
    ##
    #  Gets the basin depths for a given set of points, CVM, and desired Vs.
    #  If the CVM does not exist, an error is given. The set of points is an
    #  array of @link Point Points @endlink. The function returns the depths
        if isinstance(point_list, Point):
            point_list = [point_list]
        
        for point in point_list:
            text_points += "%.5f %.5f\n" % (point.longitude, point.latitude)
            
        output = proc.communicate(input=text_points)[0]
        output = self.checkUCVMoutput(0,output)
        
        for line in output:
            if ("WARNING" in line) or ("slow performance" in line):
                 print "skipping text",line
            else:
                 try :
                     p=float(line.split()[2])
                 except :
                     print "ERROR: should be a float."
                     exit(1)
                 floats.append(p)
        
        if len(floats) == 1:
            return floats[0]
        
        return floats

#  import meta data as a json blob
#
    def import_json(self, fname):
        rawfile=fname
        k = rawfile.rfind(".json")
        if( k == -1) : 
            print "Supplied ",fname," did not have .json suffix\n"
        try :
	    fh = open(rawfile, 'r') 
        except :
            print "ERROR: json meta data does not exist."
            exit(1)

	data = json.load(fh)
	fh.close()
	return data

#  import raw floats data from the external file 
#
#  if filename is image.png, look for a matching
#  image_data.bin
#
    def import_binary(self, fname, num_x, num_y):
        rawfile=fname
        k = rawfile.rfind(".png")
        if( k != -1) : 
            rawfile = rawfile[:k] + "_data.bin"
        try :
            fh = open(rawfile, 'r') 
        except:
            print "ERROR: binary data does not exist."
            exit(1)
            
        floats = np.fromfile(fh, dtype=np.float32)

## special case, when floats are written out as float64 instead of float32
        if len(floats) == 2 * (num_x * num_y) :
          fh.seek(0,0)
          floats = np.fromfile(fh, dtype=np.float)

        print "TOTAL number of binary data read:",len(floats),"\n"

        # sanity check,  
        if len(floats) != (num_x * num_y) :
            print "import_binary(), wrong size !!!", len(floats), " expecting ", (num_x * num_y)
            exit(1)

        fh.close()

        if len(floats) == 1:
            return floats[0]
        
        return floats

#  export raw floats nxy ndarray  to an external file 
    def export_binary(self, floats, fname):
        rawfile = fname
        if rawfile is None :
            rawfile="data.bin"
        k = rawfile.rfind(".png")
        if( k != -1) : 
            rawfile = rawfile[:k] + "_data.bin"
        try :
            fh = open(rawfile, 'w+') 
        except:
            print "ERROR: can not write out binary data."
            exit(1)
        floats.tofile(fh)

        print "export_binary(), size=",floats.size

        fh.close()

#  { 'num_x' : xval, 'num_y' : yval, 'total' : total }
#  import ascii meta jsoin data from an external file 
    def import_metadata(self, fname):
        metafile=fname
        k = metafile.rfind(".png")
        if( k != -1) : 
            metafile = metafile[:k] + "_meta.json"
        try :
            fh = open(metafile, 'r') 
        except:
            print "ERROR: can not find the meata data."
            exit(1)
        meta = json.load(fh)
        fh.close()
        return meta

#  export ascii meta data to an external file 
    def export_metadata(self,meta,fname):
        metafile=fname
        if metafile is None:
          metafile = "meta.json"
        k = metafile.rfind(".png")
        if( k != -1) : 
            metafile = metafile[:k] + "_meta.json"
        try :
            fh = open(metafile, 'w+') 
        except:
            print "ERROR: can not write the meta data."
            exit(1)
        json.dump(meta, fh, indent=2, sort_keys=False)
        fh.close()

#  import material properties in JSON form from an external file 
#  { matprops: [ 
#          { 'vp': pval, 'vs': sval, 'density': dval },
#          ...
#          { 'vp': pval, 'vs': sval, 'density': dval } ] }
    def import_matprops(self, fname):
        properties=[]
        jblob=self.import_json(fname)
        mlist= jblob["matprops"]
        for item in mlist :
           mp=MaterialProperties.fromJSONOutput(item)
           properties.append(mp)
        return properties

#  export material properties in JSON form to an external file 
    def export_matprops(self,blob,fname):
        matpropsfile=fname
        if matpropsfile is None :
            matpropsfile="matprops.json"
        k = matpropsfile.rfind(".png")
        if( k != -1) : 
            matpropsfile = matpropsfile[:k] + "_matprops.json"
        try :
            fh = open(matpropsfile, 'w+') 
        except:
            print "ERROR: can not write the material property data."
            exit(1)
        json.dump(blob, fh, indent=2, sort_keys=False)
        fh.close()



#  export material properties in JSON form to an external file 
    def export_velocity(self,filename,vslist,vplist,rholist):
        k = filename.rfind(".png")
        rawfile=filename
        if( k != -1) :
            rawfile= filename[:k] + "_data.json"
        try :
            fh = open(rawfile, 'w+')
        except:
            print "ERROR: can not write the material property data."
            exit(1)
        raw={"vs":vslist, "vp":vplist, "rho":rholist};
        json.dump(raw, fh, indent=2, sort_keys=False)
        fh.close()

    #  make the proper bounds for colormap
    #  when all is True, then need to substep all the range
    def makebounds(self,minval=0.0,maxval=5.0,nstep=0,meanval=None, substep=5,all=True) :
        bounds=[]
        if(nstep == 0) :
          bounds = [0, 0.2, 0.4, 0.6, 0.8, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
          return bounds

        step=float(maxval - minval)/nstep

        l=0
        nsubstep=substep
        nnstep=float(step)/nsubstep
        if(meanval != None) :
          l =(meanval-minval) //step

        for i in range(0,nstep) :
          s= step*i+minval
          if (i == l or all == True) :
            for j in range(nsubstep) :
              bound= round(s+(j * nnstep),4)
              bounds.append(bound)
          
          else:
            bounds.append(round(s,4))

        bounds.append(round((step * nstep + minval),4))
#        print "bounds", bounds
        return bounds

    ## 
    #  make the proper ticks for subplot
    def maketicks(self,minval=None,maxval=None,nstep=0) :
        ticks=[]

        if(nstep == 0) :
          ticks = [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
          return ticks

        step=(maxval - minval)/nstep
        for i in range(nstep) :
            tick= round((step * i) + minval,4)
            ticks.append(tick)

        ticks.append(round((step * nstep + minval),4))
#        print "ticks ", ticks
        return ticks


#  Function Definitions

##
#  Displays an error message and exits the program.
#  @param message The error message to be displayed.
def pycvm_display_error(message):
    print "An error has occurred while executing this script. The error was:\n"
    print message
    print "\nPlease contact software@scec.org and describe both the error and a bit"
    print "about the computer you are running CVM-S5 on (Linux, Mac, etc.)."
    exit(0)
    
##
#  Returns true if value is a number. False otherwise.
#
#  @param value The value to test if numeric or not.
#  @return True if it is a number, false if not.
def pycvm_is_num(value):
    try:
        float(value)
        return True
    except Exception:
        return False
    
##
#  Returns the discrete colormap.
#
#  @param cmap The colormap to use.
#  @param N The number of discretized intervals.
def pycvm_cmapDiscretize(cmap, N):
    cdict = cmap._segmentdata.copy()
    # N colors
    colors_i = np.linspace(0,1.,N)
    # N+1 indices
    indices = np.linspace(0,1.,N+1)
    for key in ('red','green','blue'):
        # Find the N colors
        D = np.array(cdict[key])
        colors = np.interp(colors_i, D[:,0], D[:,1])
        #I = sp.interpolate.interp1d(D[:,0], D[:,1])
        #colors = I(colors_i)
        # Place these colors at the correct indices.
        A = np.zeros((N+1,3), float)
        A[:,0] = indices
        A[1:,1] = colors
        A[:-1,2] = colors
        # Create a tuple for the dictionary.
        L = []
        for l in A:
            L.append(tuple(l))
        cdict[key] = tuple(L)
    # Return colormap object.
    return mcolors.LinearSegmentedColormap('colormap',cdict,1024)
