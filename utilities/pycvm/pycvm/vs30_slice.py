##
#  @file vs30_slice.py
#  @brief Gets a slice of Vs30 values either to display or save.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Gets a horizontal slice of the Vs30 data which can be used in the exact 
#  same way, and plotted in the same way, as a
#  @link horizontal_slice.HorizontalSlice HorizontalSlice @endlink.

#  Imports
from horizontal_slice import HorizontalSlice
from common import Point, MaterialProperties, UCVM, UCVM_CVMS, \
                   math, pycvm_cmapDiscretize, cm, mcolors, basemap, np, plt

##
#  @class Vs30Slice
#  @brief Gets a horizontal slice of Vs30 data.
#
#  Retrieves a horizontal slice of Vs30 values for a given CVM.
class Vs30Slice(HorizontalSlice):
    
    ##
    #  Initializes the super class and copies the parameters over.
    #
    #  @param upperleftpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param bottomrightpoint The @link common.Point ending point @endlink at which this plot should end.
    #  @param spacing The spacing, in degrees, for this plot. 
    #  @param cvm The community velocity model from which this data should come.
    #  
    def __init__(self, upperleftpoint, bottomrightpoint, meta={}):

        #  Initializes the base class which is a horizontal slice.
        HorizontalSlice.__init__(self, upperleftpoint, bottomrightpoint, meta)
    
    ##
    #  Retrieves the values for this Vs30 slice and stores them in the class.
    def getplotvals(self, mproperty="vs"):
        
        #  How many y and x values will we need?
        
        ## The plot width - needs to be stored as property for the plot function to work.
        self.plot_width  = self.bottomrightpoint.longitude - self.upperleftpoint.longitude
        ## The plot height - needs to be stored as a property for the plot function to work.
        self.plot_height = self.upperleftpoint.latitude - self.bottomrightpoint.latitude 
        ## The number of x points we retrieved. Stored as a property for the plot function to work.
        if ( self.xsteps ):
           self.num_x = int(self.xsteps)
        else :
           self.num_x = int(math.ceil(self.plot_width / self.spacing)) + 1
        ## The number of y points we retrieved. Stored as a property for the plot function to work.
        if ( self.ysteps ) :
           self.num_y = int(self.ysteps)  
        else :
           self.num_y = int(math.ceil(self.plot_height / self.spacing)) + 1
        
        ## The 2D array of retrieved Vs30 values.
        self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in range(self.num_x)] for x in range(self.num_y)] 
        
        u = UCVM(install_dir=self.installdir, config_file=self.configfile)

        ###MEI
        if (self.datafile != None) :
            print("\nUsing --> "+self.datafile)
            # print("expecting x ",self.num_x," y ",self.num_y)
            data = u.import_binary(self.datafile, self.num_x, self.num_y)
        else:
            #  Generate a list of points to pass to UCVM.
            ucvmpoints = []
            for y in range(0, self.num_y):
                for x in range(0, self.num_x):
                    ucvmpoints.append(Point(self.upperleftpoint.longitude + x * self.spacing, \
                                            self.bottomrightpoint.latitude + y * self.spacing, \
                                            self.upperleftpoint.depth))
            data = u.vs30(ucvmpoints, self.cvm)
        
        i = 0
        j = 0
        
        for matprop in data:
            self.materialproperties[i][j].vs = matprop
            j = j + 1
            if j >= self.num_x:
                j = 0
                i = i + 1

    ##
    #  Plots the Vs30 data as a horizontal slice. This code is very similar to the
    #  HorizontalSlice routine.
    #
    #  @param filename The location to which the plot should be saved. Optional.
    #  @param title The title of the plot to use. Optional.
    #  @param color_scale The color scale to use for the plot. Optional.
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

        if 'title' not in self.meta:
            title= "%sVs30 Data For %s" % (location_text, cvmdesc)
            self.meta['title'] = title

        self.meta['mproperty']="vs"
        
        HorizontalSlice.plot(self)
