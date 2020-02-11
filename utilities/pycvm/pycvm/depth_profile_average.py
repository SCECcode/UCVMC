##
#  @file depth_profile_average.py
#  @brief Plots a 1D depth profile to an image or a pre-existing plot.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Allows for generation of a 1D depth profile, either interactively, via
#  arguments, or through Python code in the class DepthProfile.

#  Imports
from common import Plot, Point, MaterialProperties, UCVM, UCVM_CVMS, plt
from scipy.interpolate import spline, splprep, splev
from scipy.interpolate import Rbf, InterpolatedUnivariateSpline
import scipy.interpolate as interpolate
import numpy as np
import pdb
import json

##
#  @class DepthProfileAverage
#  @brief Plots a 1D depth profile at a given @link common.Point Point @endlink.
#
#  Generates a 1D depth profile that can either be saved as a file or displayed
#  to the user. 
class DepthProfileAverage:
    
    ##
    #  Initializes the 1D profile class.
    #
    #  @param startingpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param todepth The ending depth, in meters, where this plot should end.
    #  @param spacing The discretization interval in meters.
    #  @param cvm The CVM from which to retrieve these material properties.
    def __init__(self, startingpoint, meta={}):

        self.meta=meta

##                 @
##                 ^
##               deltaY
##                 V
##    @<-deltaX->TARGET<-deltaX->@
##                 ^
##               deltaY
##                 V
##                 @

        if 'deltax' in self.meta:
            self.deltax = int(self.meta['deltax'])
        else:
            self.deltax = 0

        if 'deltay' in self.meta:
            self.deltay = int(self.meta['deltay'])
        else
            self.deltay=0

        if 'installdir' in self.meta:
            self.installdir = self.meta['installdir']
        else:
            self.installdir = None

        if 'configfile' in self.meta:
            self.configfile = self.meta['configfile']
        else:
            self.configfile = None

        self.metadata = None
        if 'metadata' in self.meta :
            f = self.meta['metadata']
            u = UCVM(install_dir=self.installdir, config_file=self.configfile)
            self.metadata = u.import_metadata(f)

        if not isinstance(startingpoint, Point):
            raise TypeError("The starting point must be an instance of Point.")
        else:
            ## Defines the @link common.Point starting point @endlink for the depth profile.
            self.startingpoint = startingpoint

        ## The discretization of the plot, in meters.
        if self.metadata != None and "vertical_spacing" in self.metadata:
            self.spacing = float(self.metadata['vertical_spacing'])
        elif 'vertical_spacing' in self.meta :
            self.spacing = float(self.meta['vertical_spacing'])
        else:
            self.spacing = -1

        if self.metadata != None and 'ending_depth' in self.metadata :
            self.todepth = float(self.metadata['ending_depth'])
        elif 'ending_depth' in self.meta :
            self.todepth = float(self.meta['ending_depth'])
        else:
            self.todepth = 50000

        if (self.todepth - self.startingpoint.depth) % self.spacing != 0:
            raise ValueError("%s\n%s\n%s" % ("The spacing value does not divide evenly into the requested depth. ", \
                          "Please make sure that the depth (%.2f - %.2f) divided by the spacing " % (todepth, startingpoint.depth), \
                          "%.2f has no remainder" % (spacing)))
        else:
            if self.metadata != None and "starting_depth" in self.metadata:
                self.startingdepth = float(self.metadata['starting_depth'])
            ## Defines the depth to which the plot should go in meters.
            else:
                self.startingdepth = self.startingpoint.depth

        self.z_range = None
        if 'zrange1' in self.meta and 'zrange2' in self.meta :
            self.z_range=self.meta['zrange1']+","+self.meta['zrange2']

        ## The CVM to use (must be installed with UCVM).
        if 'cvm' in self.meta :
            self.cvm = self.meta['cvm']

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

        ## Private holding place for depth data.
        self.depthlist = []

        ## Default threshold in simplified units
        if 'vs_threshold' in self.meta :
            self.threshold = self.meta['vs_threshold']
        else:
            self.threshold = None

## 
#  Generates the depth profile in a format that is ready to plot.
    def getplotvals(self):

## setup the depth list
        self.meta['depth'] = []
        for i in np.arange(self.startingpoint.depth, self.todepth + 1, self.spacing):
            self.meta['depth'].append(i)

## setup local vplist[], vslist[] and rholist[]
        idx=0
        vp_sum=[]
        vs_sum=[]
        rho_sum=[]

## coming in from external file,  just 1 set
        if (self.datafile != None) :
            print "ERROR: TODO"
                exit(1)
        else:

## get the latlons
        latlons_list=[]
        latlons_list.append({'lat':self.startingpoint.latitude,'lon':self.startingpoint.longitude})
##XXX
        dlen=len(self.meta['depth'])
        blob_list=[]
        idx=0
        xmax=(2* self.deltax)+1
        ymax=(2* self.deltay)+1
        for y in xrange(0, ymax) :
            for x in xrange(0, xmax) :
##XXX                  lalons=latlons_list[idx]
                lalons=latlons_list[0]
                vplist=[]
                vslist=[]
                rholist=[]
                b=getplotvals_one(idx, self.meta['depth'], latlons['lat'], latlons['lon'], vplist, vslist, rholist)
                idx=idx+1
                blob_list.append(b)
## accumulate it
                for z in xrange(0, dlen):
                    vs_sum[z]=vs_sum[z]+vslist[z]
                    vp_sum[z]=vp_sum[z]+vplist[z]
                    rho_sum[z]=rho_sum[z]+rholist[z]

### average and extract the vp,vs,rho 
        averageplotdata(idx, dlen, vs_sum, vp_sum, rho_sum);

    def averageplotvals(self, counts,dlen, vssum, vpsum, rhosum ):
        for i xrange(0, dlen) :
            vplist.append(vpsum[i]/counts)
            vslist.append(vssum[i]/counts)
            rholist.append(rhosum[i]/counts)

    def getplotvals_one(self, idx, depth_list, lat, lon, vplist, vslist, rholist):
        # Generate the list of points.
        point_list = []
        for depth in depth_list :
            point_list.append(Point(lon, lat, depth))
            
        u = UCVM(install_dir=self.installdir, config_file=self.configfile, z_range=self.z_range)

        data = u.query(point_list, self.cvm)
        
        tmp = []
        for matprop in data:
            vplist.append(matprop.vp)
            vslist.append(matprop.vs)
            rholist.append(matprop.density)
## create the blob
            if(self.datafile == None) : ## save an external copy of matprops 
                b= { 'vp':float(matprop.vp), 'vs':float(matprop.vs), 'density':float(matprop.density) }
                tmp.append(b)
    
        blob = { 'idx': idx, 'lon':lon, 'lat':lat, 'matprops' : tmp }
        return blob
           
    ##
    #  Adds the depth profile to a pre-existing plot.
    #
    #  @param plot The @link common.Plot Plot @endlink object to which we're plotting.
    #  @param colors The colors that the properties should be plotted as. Optional.
    #  @param customlabels An associated array of labels to put for the legend. Optional.
    def addtoplot(self, plot, colors = None, customlabels = None):
        
        # Check that plot is a Plot
        if not isinstance(plot, Plot):
            raise TypeError("Plot must be an instance of the class Plot.")
        
        # Get the material properties.
        self.getplotvals()
        
        max_x = 0
        yvals = []

        ### determining the depth interval --
        if self.metadata == None :
            for i in xrange(int(self.startingdepth), int(self.todepth + 1), int(self.spacing)):  
                yvals.append(i)       
        else: ## pick up from the the meta data file
            yvals = self.metadata['depth']
      
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

        self.depthlist=yvals

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

        plt.axis([0, max_x, int(self.todepth), int(self.startingdepth)])
    
    ##
    #  Plots a new depth profile using all the default plotting options.
    #
    #  @param properties An array of material properties. Can be one or more of vp, vs, and/or density.
    #  @param filename If this is set, the plot will not be shown but rather saved to this location.
    def plot(self):

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
            title = "%s%s Depth Profile From %sm To %sm at (%.6f,%.6f)" % (location_text, cvmdesc, self.startingpoint.depth, self.todepth, self.startingpoint.longitude, self.startingpoint.latitude)

        # Call the plot object.
        p = Plot(title, "Units (see legend)", "Depth (m)", None, 7, 10)

        # Add to plot.
        self.addtoplot(p)
                
        if self.filename == None:
            plt.show()
        else:
            plt.savefig(self.filename)
