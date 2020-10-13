##
#  @file elevation_profile.py
#  @brief Plots a 1D elevation profile to an image or a pre-existing plot.
#  @author 
#  @version 14.7.0
#
#  Allows for generation of a 1D elevation profile, either interactively, via
#  arguments, or through Python code in the class ElevationProfile.

#  Imports
from common import Plot, Point, MaterialProperties, UCVM, UCVM_CVMS, plt
from scipy.interpolate import spline, splprep, splev
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline
import scipy.interpolate as interpolate
import numpy as np
import pdb
import json

##
#  @class ElevationProfile
#  @brief Plots a 1D elevation profile at a given @link common.Point Point @endlink.
#
#  Generates a 1D elevation profile that can either be saved as a file or displayed
#  to the user. 
class ElevationProfile:
    
    ##
    #  Initializes the 1D profile class.
    #
    #  @param startingpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param toend The ending elevation, in meters, where this plot should end.
    #  @param spacing The discretization interval in meters.
    #  @param cvm The CVM from which to retrieve these material properties.
    def __init__(self, startingpoint, meta={}) :

        self.meta = meta

        if not isinstance(startingpoint, Point):
            raise TypeError("The starting point must be an instance of Point.")
        else:
            ## Defines the @link common.Point starting point @endlink for the elevation profile.
            self.startingpoint = startingpoint

        ## The discretization of the plot, in meters.
        if 'vertical_spacing' in self.meta :
            self.spacing = float(self.meta['vertical_spacing'])
        else:
            self.spacing = -1
        
        if 'ending_elevation' in self.meta :
            self.toelevation = float(self.meta['ending_elevation'])
        else:
            self.toelevation = -15000  ## max, -15000

        if (self.toelevation - self.startingpoint.elevation) % self.spacing != 0:
            raise ValueError("%s\n%s\n%s" % ("The spacing value does not divide evenly into the requested elevation. ", \
                          "Please make sure that the elevation (%.2f - %.2f) divided by the spacing " % (self.toelevation, self.startingpoint.elevation), \
                          "%.2f has no remainder" % (spacing)))
        else:
            ## Defines the elevation to which the plot should go in meters.
            self.startelevation = self.startingpoint.elevation

        self.z_range = None
        if 'zrange1' in self.meta and 'zrange2' in self.meta :
            self.z_range=self.meta['zrange1']+","+self.meta['zrange2']

        ## The CVM to use (must be installed with UCVM).
        if 'cvm' in self.meta :
            self.cvm = self.meta['cvm']

        if 'installdir' in self.meta:
            self.installdir = self.meta['installdir']
        else:
            self.installdir = None

        if 'configfile' in self.meta:
            self.configfile = self.meta['configfile']
        else:
            self.configfile = None

        self.datafile = None
        if 'datafile' in self.meta :
            self.datafile = self.meta['datafile']

        self.filename = None
        if 'outfile' in self.meta :
           self.filename = self.meta['outfile']

        self.properties="vs"
        if 'data_type' in self.meta :
           self.properties = self.meta['data_type']


        ## Private holding place for returned Vp data.        
        self.vplist = []
        ## Private holding place for returned Vs data.
        self.vslist = []
        ## Private holding place for returned density data.
        self.rholist = []

        ## Private holding place for elevation data.
        self.elevationlist = []

        ## Default threshold in simplified units
        if 'vs_threshold' in self.meta :
            self.threshold = self.meta['vs_threshold']
        else:
            self.threshold = None
    
    ## 
    #  Generates the elevation profile in a format that is ready to plot.
    def getplotvals(self) :
        
        point_list = []
        # Generate the list of points.
 
        toto=self.toelevation
        if(toto <=0 ):
          toto = toto-1
        else:
          toto = toto+1

        self.meta['elevation'] = []
        for i in np.arange(self.startelevation, toto, self.spacing):
            point_list.append(Point(self.startingpoint.longitude, self.startingpoint.latitude, elevation=i))
            self.meta['elevation'].append(i)
            
        u = UCVM(install_dir=self.installdir, config_file=self.configfile, z_range=self.z_range)

###MEI
        if (self.datafile != None) :
            print("\nUsing --> "+self.datafile)
            data = u.import_matprops(self.datafile)
            if len(data) == 0 :
                print("ERROR: no matprops plot data.")
                exit(1)
        else:
            data = u.query(point_list, self.cvm, elevation=1)
        
        tmp = []
        for matprop in data:
            self.vplist.append(matprop.vp)
            self.vslist.append(matprop.vs)
            self.rholist.append(matprop.density)
## create the blob
            if(self.datafile == None) : ## save an external copy of matprops 
              b= { 'vp':float(matprop.vp), 'vs':float(matprop.vs), 'density':float(matprop.density) }
              tmp.append(b)

        if(self.datafile == None) :
              blob = { 'matprops' : tmp }
              u.export_matprops(blob,self.filename)
              u.export_metadata(self.meta,self.filename)
    
    ##
    #  Adds the elevation profile to a pre-existing plot.
    #
    #  @param plot The @link common.Plot Plot @endlink object to which we're plotting.
    #  @param colors The colors that the properties should be plotted as. Optional.
    #  @param customlabels An associated array of labels to put for the legend. Optional.
    def addtoplot(self, plot, colors=None, customlabels=None) :
# defaults:
# colors={"vs":"b","vp":"y","density":"g"}
# customlabels={"vs":"Vs (km/s)","vp":"Vp (km/s)","density":"Density (g/cm^3)"}
        
        # Check that plot is a Plot
        if not isinstance(plot, Plot):
            raise TypeError("Plot must be an instance of the class Plot.")
        
        # Get the material properties.
        self.getplotvals()
        
        max_x = 0
        yvals = []

        toto=self.toelevation
        if(toto <= 0):
          toto=toto-1
        else:
          toto=toto+1

        for i in np.arange(self.startelevation, toto, self.spacing):
            yvals.append(i)       
        
        if customlabels != None and "vp" in self.properties: 
            vplabel = customlabels["vp"]
        else:
            vplabel = "Vp (km/s)" 
        
        if customlabels != None and "vs" in self.properties: 
            vslabel = customlabels["vs"]
        else:
            vslabel = "Vs (km/s)"  
        
        if customlabels != None and "density" in self.properties: 
            densitylabel = customlabels["density"]
        else:
            densitylabel = "Density (g/cm^3)"  

        if colors != None and "vp" in self.properties: 
            vpcolor = colors["vp"]
        else:
            vpcolor = "r" 
        
        if colors != None and "vs" in self.properties: 
            vscolor = colors["vs"]
        else:
            vscolor = "b"  
        
        if colors != None and "density" in self.properties: 
            densitycolor = colors["density"]
        else:
            densitycolor = "g"                
        
        if "vp" in self.properties:
            myInt=1000
            newvplist=np.array(self.vplist)/myInt
            max_x = max(max_x, max(newvplist))
            plot.addsubplot().plot(newvplist, yvals, "-", color=vpcolor, label=vplabel)

        if "vs" in self.properties:
            myInt=1000
            newvslist=np.array(self.vslist)/myInt
            max_x = max(max_x, max(newvslist))
            plot.addsubplot().plot(newvslist, yvals, "-", color=vscolor, label=vslabel)

## attempted to draw a smoothed line, not good
##            xs=np.array(self.vslist)
##            ys=np.array(yvals)
##            # spline parameters
##            s=3.0 # smoothness parameter
##            k=2 # spline order
##            nest=-1 # estimate of number of knots needed (-1 = maximal)
##            # find the knot points
##            tckp,u = splprep([xs,ys],s=s,k=k,nest=nest)
##            # evaluate spline, including interpolated points
##            newx,newy = splev(np.linspace(0,1,500),tckp)
##            plot.addsubplot().plot(newx, newy, "b-", label="smoothed"+vslabel)
            ## add a vline if there is a vs threshold
            if self.threshold != None : 
                plot.addsubplot().axvline(self.threshold/1000, color='k', linestyle='dashed')

        self.elevationlist=yvals

        if "density" in self.properties:
            myInt=1000
            newrholist=np.array(self.rholist)/myInt
            max_x = max(max_x, max(newrholist))
            plot.addsubplot().plot(newrholist, yvals, "-", color=densitycolor, label=densitylabel) 
        
        plt.legend(loc="lower left")
                
        if plt.ylim()[0] < plt.ylim()[1]:
            plt.gca().invert_yaxis() 
        
        if max_x > plt.xlim()[1]:
            plt.xlim(0, math.ceil(max_x / 0.5) * 0.5)

        plt.axis([0, max_x, int(self.toelevation), int(self.startelevation)])
    
    ##
    #  Plots a new elevation profile using all the default plotting options.
    #
    def plot(self) :

        if self.startingpoint.description == None:
            location_text = ""
        else:
            location_text = self.startingpoint.description + " "

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm

        if 'title' in self.meta:
            title = self.meta['title']
        else:
            title = "%s%s Elevation Profile From %sm To %sm at (%.2f,%.2f)" % (location_text, cvmdesc, self.startelevation, self.toelevation, self.startingpoint.longitude, self.startingpoint.latitude)

        # Call the plot object.
        p = Plot(title, "Units (see legend)", "Elevation (m)", None, 7, 10)

        # Add to plot.
        self.addtoplot(p)

        if self.filename == None:
            plt.show()
        else:
            plt.savefig(self.filename)
