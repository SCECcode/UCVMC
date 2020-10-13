##
#  @file map_grid_horizontal_slice.py
#  @brief Gets a slice of values to save.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Gets a horizontal slice which contains the complete set of
#  material properties
#  @link horizontal_slice.HorizontalSlice HorizontalSlice @endlink.

#  Imports
from horizontal_slice import HorizontalSlice
from common import Point, MaterialProperties, UCVM, UCVM_CVMS, \
                   math, pycvm_cmapDiscretize, cm, mcolors, basemap, np, plt
import pdb

##
#  @class MapGridHorizontalSlice
#  @brief Gets a horizontal slice of cvm data.
#
#  Retrieves a horizontal slice of values for a given CVM.
class MapGridHorizontalSlice(HorizontalSlice):
    
    ##
    #  Initializes the super class and copies the parameters over.
    #
    #  @param upperleftpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param bottomrightpoint The @link common.Point ending point @endlink at which this plot should end.
    #  @param meta The metadata to hold the configuration settings
    #  
    def __init__(self, upperleftpoint, bottomrightpoint, meta = {}) :
        #
        # define a list of strings that will be returned and written to file
        self.ucvm_query_results = []

        #  Initializes the base class which is a horizontal slice.
        HorizontalSlice.__init__(self, upperleftpoint, bottomrightpoint, meta)
    
    def getplotvals(self):

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
        
        ## The 2D array of retrieved material properties
        self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in range(self.num_x)] for x in range(self.num_y)] 
        
        u = UCVM(install_dir=self.installdir, config_file=self.configfile)

        #  Generate a list of points to pass to UCVM.
        ucvmpoints = []
        for y in range(0, self.num_y):
            for x in range(0, self.num_x):
                ucvmpoints.append(Point(self.upperleftpoint.longitude + x * self.spacing, \
                                        self.bottomrightpoint.latitude + y * self.spacing, \
                                        self.upperleftpoint.depth))

        self.ucvm_query_results = u.map_grid(ucvmpoints, self.cvm)
 
    ##
    #  Save the horizontal slice grid_pts into a txt file
    #
    #  @param filename The location to which the grid_pts should be saved. Optional.
    #
    def plot(self):

        self.getplotvals()
 
        if self.filename != None:
            print("Writing to output file: %s"%(self.filename)) 
            f = open(self.filename,"w")
            for line in self.ucvm_query_results:
                f.write("%s\n"%(line))
            f.close()
        else:
            print("No file created")
            pass
