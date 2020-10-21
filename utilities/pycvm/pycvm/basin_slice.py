##
#
#  @file basin_slice.py
#  @brief Gets the Z1.0, Z2.5, or other thresholds from a specified velocity model.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Retrieves a horizontal slice of the Z thresholds from one of the
#  community velocity models that UCVM supports. For reference, a
#  Z1.0 map is the first depth at which Vs > 1000m/s. This class
#  inherits from @link horizontal_slice.HorizontalSlice @endlink.

#  Imports
from horizontal_slice import HorizontalSlice
from common import Point, MaterialProperties, UCVM, UCVM_CVMS, \
                   math, pycvm_cmapDiscretize, cm, mcolors, np, plt
import pdb

##
#  @class BasinSlice
#  @brief Gets a horizontal slice of the basin data.
#
#  Retrieves a horizontal slice of the depths to a certain Vs threshold.
class BasinSlice(HorizontalSlice):
    
    ##
    #  Initializes the super class and copies the parameters over.
    #
    #  @param upperleftpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param bottomrightpoint The @link common.Point ending point @endlink at which this plot should end.
    #  @param spacing The spacing, in degrees by default, or meters (if "m" appended), for this plot. 
    #                 To specify meters, give this parameter like "100m" instead of "0.01" degrees.
    #  @param cvm The community velocity model from which this data should come.
    #  @param vs_threshold The Vs value to check for at each depth.
    def __init__(self, upperleftpoint, bottomrightpoint, vs_threshold, meta):
        ## The Vs value to check for.
        self.vs_threshold = vs_threshold

        #  Initializes the base class which is a horizontal slice.
        HorizontalSlice.__init__(self, upperleftpoint, bottomrightpoint, meta)
    ##
    #  Retrieves the values for this basin slice and stores them in the class.
    def getplotvals(self, mproperty="vs"):
        
        #  How many y and x values will we need?
        
        ## The plot width - needs to be stored as property for the plot function to work.
        self.plot_width  = self.bottomrightpoint.longitude - self.upperleftpoint.longitude
        ## The plot height - needs to be stored as a property for the plot function to work.
        self.plot_height = self.upperleftpoint.latitude - self.bottomrightpoint.latitude 
        ## The number of x points we retrieved. Stored as a property for the plot function to work.
        if( self.xsteps != None ) :
           self.num_x = int(self.xsteps)
        else:
           self.num_x = int(math.ceil(self.plot_width / self.spacing)) + 1
        ## The number of y points we retrieved. Stored as a property for the plot function to work.
        if( self.ysteps != None ) :
           self.num_y = int(self.ysteps)
        else:
           self.num_y = int(math.ceil(self.plot_height / self.spacing)) + 1
        
        ## Maximum depth encountered.
        self.max_val = 0
        ## Minimum depth (always 0).
        self.min_val = 0

        ## The 2D array of retrieved Vs30 values.
        self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in range(self.num_x)] for x in range(self.num_y)] 
        
        u = UCVM(install_dir=self.installdir, config_file=self.configfile)
### MEI
        if (self.datafile != None) :
#            print("\nUsing --> "+datafile)
            data = u.import_binary(self.datafile, self.num_x, self.num_y)
#            print("Total points imported is ", len(data), "for ", self.num_x, " and ", self.num_y)
        else:
            #  Generate a list of points to pass to UCVM.
            ucvmpoints = []
            for y in range(0, self.num_y):
                for x in range(0, self.num_x):
                    ucvmpoints.append(Point(self.upperleftpoint.longitude + x * self.spacing, \
                                            self.bottomrightpoint.latitude + y * self.spacing, \
                                            self.upperleftpoint.depth))
#            print("Total points extracted is ", len(ucvmpoints), "for ", self.num_x, " and ", self.num_y)
            data = u.basin_depth(ucvmpoints, self.cvm, self.vs_threshold)

        i = 0
        j = 0

        for matprop in data:
            self.materialproperties[i][j].vs = matprop

            if matprop > self.max_val:
                self.max_val = matprop

            j = j + 1
            if j >= self.num_x:
                j = 0
                i = i + 1

    ##
    #  Plots the basin depth data as a horizontal slice. This code is very similar to the
    #  HorizontalSlice routine.
    #
    #  @param horizontal_label The horizontal label of the plot. Optional.
    def plot(self, horizontal_label = "Depth (km)") :

        if self.upperleftpoint.description == None:
            location_text = ""
        else:
            location_text = self.upperleftpoint.description + " "

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm

        if 'title' not in self.meta:
            self.title = "%sBasin Depth Map For %s" % (location_text, cvmdesc)
            self.meta['title'] = self.title;
 
        self.meta['mproperty']="vs"

        HorizontalSlice.plot(self, horizontal_label)
        
##
#  @class Z10Slice
#  @brief Gets a Z1.0 data map.
#
#  Retrieves a horizontal slice of the depths for Z1.0.
class Z10Slice(BasinSlice):
    
    ##
    #  Initializes the super class and copies the parameters over.
    #
    #  @param upperleftpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param bottomrightpoint The @link common.Point ending point @endlink at which this plot should end.
    #  @param spacing The spacing, in degrees by default, or meters (if "m" appended), for this plot. 
    #                 To specify meters, give this parameter like "100m" instead of "0.01" degrees.
    #  @param cvm The community velocity model from which this data should come.
    def __init__(self, upperleftpoint, bottomrightpoint, meta={}) :

        #  Initializes the base class which is a horizontal slice.
        BasinSlice.__init__(self, upperleftpoint, bottomrightpoint, 1000, meta)
    
    ##
    #  Gets the depths for the plot in meters.
    def getplotvals(self, mproperty):
        BasinSlice.getplotvals(self, mproperty)
    
    ##
    #  Plots the Z1.0 slice.
    #
    def plot(self) :

        if self.upperleftpoint.description == None:
            location_text = ""
        else:
            location_text = self.upperleftpoint.description + " "

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm
        
        if 'title' in self.meta :
            self.title = self.meta['title']
        else:
            self.title = "%sZ1.0 Map For %s" % (location_text, cvmdesc)
            self.meta['title'] = self.title
  
        BasinSlice.plot(self)
        
##
#  @class Z25Slice
#  @brief Gets a Z2.5 data map.
#
#  Retrieves a horizontal slice of the depths for Z2.5.
class Z25Slice(BasinSlice):
    
    ##
    #  Initializes the super class and copies the parameters over.
    #
    #  @param upperleftpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param bottomrightpoint The @link common.Point ending point @endlink at which this plot should end.
    #  @param spacing The spacing, in degrees by default, or meters (if "m" appended), for this plot. 
    #                 To specify meters, give this parameter like "100m" instead of "0.01" degrees.
    #  @param cvm The community velocity model from which this data should come.
    def __init__(self, upperleftpoint, bottomrightpoint, meta={}):

        #  Initializes the base class which is a horizontal slice.
        BasinSlice.__init__(self, upperleftpoint, bottomrightpoint, 2500, meta)
    
    ##
    #  Gets the depths for the plot in meters.
    def getplotvals(self, mproperty):
        BasinSlice.getplotvals(self, mproperty)
    
    ##
    #  Generates the Z2.5 slice plot.
    #
    #  @param title The title for the plot. Optional.
    #  @param filename The file to which the plot should be saved. Optional.
    def plot(self):

        if self.upperleftpoint.description == None:
            location_text = ""
        else:
            location_text = self.upperleftpoint.description + " "

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm
        
        if 'title' not in self.meta :
            title = "%sZ2.5 Map For %s" % (location_text, cvmdesc)
            self.meta['title'] = title
  
        BasinSlice.plot(self)
     
