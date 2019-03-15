##
#  @file horizontal_slice.py
#  @brief Plots a horizontal slice either for display or saving to a file.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Allows for generation of a horizontal slice, either interactively, via
#  arguments, or through Python code in the class HorizontalSlice.

#  Imports
from mpl_toolkits import basemap
from mpl_toolkits.basemap import cm
from common import Plot, Point, MaterialProperties, UCVM, UCVM_CVMS, \
                   math, pycvm_cmapDiscretize, cm, mcolors, basemap, np, plt

import pdb
##
#  @class HorizontalSlice
#  @brief Plots a horizontal slice starting at a given @link common.Point Point @endlink
#         to another @link common.Point Point @endlink.
#
#  Generates a horizontal slice that can either be displayed to the user, saved to a file
#  or differenced with another plot.
class HorizontalSlice:
    
    ##
    #  Initializes the horizontal slice. The slice will go from the upper-left 
    #  @link common.Point Point @endlink parameter to the bottom-right 
    #  @link common.Point Point @endlink parameter, at the depth specified in the 
    #  upper-left point. 
    #
    #  @param upperleftpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param bottomrightpoint The @link common.Point ending point @endlink at which this plot should end.
    #  @param spacing The spacing, in degrees, for this plot.
    #  @param cvm The community velocity model from which this data should come.
    #  
    def __init__(self, upperleftpoint, bottomrightpoint, spacing, cvm, xsteps=None, ysteps = None):

        self.xsteps = xsteps
        self.ysteps = ysteps
        
        if not isinstance(upperleftpoint, Point):
            raise TypeError("Parameter upperleftpoint must be of type Point.")
        else:
            ## The upper-left point from which this plot should originate.
            self.upperleftpoint = upperleftpoint
            
        if not isinstance(bottomrightpoint, Point):
            raise TypeError("Parameter bottomrightpoint must be of type Point.")
        else:
            ## The bottom-right corner at which this plot should end.
            self.bottomrightpoint = bottomrightpoint
        
        #  Check that the bottom-right point is below and right of the upper-left point.
        if (self.upperleftpoint.longitude > self.bottomrightpoint.longitude) or \
           (self.upperleftpoint.latitude < self.bottomrightpoint.latitude):
            raise ValueError("The upper-left point must be higher than, and to the " + \
                             "left of, the bottom-right point.")
            
        #  Check the spacing. If it's specified in meters, convert to degrees.
        try:
            ## The spacing for the plot, defined in degrees. If meters specified, it's converted to degrees.
            self.spacing = float(spacing)
        except Exception:
            print "TODO"
        
        ## The community velocity model from which the data should be retrieved.
        self.cvm = cvm
    
    ##
    #  Retrieves the values for this horizontal slice and stores them in the class.
    def getplotvals(self, property="vs",datafile = None):
        
        #  How many y and x values will we need?
        
        ## The plot width - needs to be stored as property for the plot function to work.
        self.plot_width  = self.bottomrightpoint.longitude - self.upperleftpoint.longitude
        ## The plot height - needs to be stored as a property for the plot function to work.
        self.plot_height = self.upperleftpoint.latitude - self.bottomrightpoint.latitude 
        ## The number of x points we retrieved. Stored as a property for the plot function to work.
        if ( self.xsteps ) :
           self.num_x = int(self.xsteps)
        else :
           self.num_x = int(math.ceil(self.plot_width / self.spacing)) + 1

        ## The number of y points we retrieved. Stored as a property for the plot function to work.
        if ( self.ysteps ) :
           self.num_y = int(self.ysteps)
        else :
           self.num_y = int(math.ceil(self.plot_height / self.spacing)) + 1
        
        ## The 2D array of retrieved material properties.
        self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in xrange(self.num_x)] for x in xrange(self.num_y)] 
        
        u = UCVM()

### MEI
        if (datafile != None) :
            data = u.import_binary(datafile, self.num_x, self.num_y)
            print "\nUsing --> "+datafile 
            print "expecting x ",self.num_x," y ",self.num_y
	else: 
            #  Generate a list of points to pass to UCVM.
            ucvmpoints = []
            for y in xrange(0, self.num_y):
                for x in xrange(0, self.num_x):
                    ucvmpoints.append(Point(self.upperleftpoint.longitude + x * self.spacing, \
                                            self.bottomrightpoint.latitude + y * self.spacing, \
                                            self.upperleftpoint.depth))
            data = u.query(ucvmpoints, self.cvm)

        i = 0
        j = 0
        isfloat = 0
        if (datafile != None) :
            isfloat = 1
        for matprop in data:
            if(datafile != None) :
                matprop=matprop * 1000.0
            if isfloat:
                self.materialproperties[i][j].setProperty(property,matprop)
            else:
                self.materialproperties[i][j]=matprop
            j = j + 1
            if j >= self.num_x:
                j = 0
                i = i + 1

    ## 
    #  Plots the horizontal slice either to an image or a file name.
    # 
    #  @param property The property either as a single item array or string.
    #  @param filename The file name of the image if we're saving it. Optional.
    #  @param title The title of the plot. Optional.
    #  @param horizontal_label The horizontal label of the plot. Optional.
    #  @param color_scale The color scale for the plot (d, discretized; s, smooth). Optional.
    def plot(self, property, filename = None, title = None, horizontal_label = None, color_scale = "d", datafile = None, meta={}):

        if self.upperleftpoint.description == None:
            location_text = ""
        else:
            location_text = self.upperleftpoint.description + " "

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm

        if title == None:
            title = "%s%s Horizontal Slice at %.0fm" % (location_text, cvmdesc, self.upperleftpoint.depth)

        self.getplotvals(property,datafile)

        # Call the plot object.
        p = Plot(title, "", "", None, 10, 10)

        u = UCVM()

        BOUNDS = u.makebounds()
        TICKS = u.maketicks()
       

        m = basemap.Basemap(projection='cyl', llcrnrlat=self.bottomrightpoint.latitude, \
                            urcrnrlat=self.upperleftpoint.latitude, \
                            llcrnrlon=self.upperleftpoint.longitude, \
                            urcrnrlon=self.bottomrightpoint.longitude, \
                            resolution='f', anchor='C')
        
        lat_ticks = np.arange(self.bottomrightpoint.latitude, self.upperleftpoint.latitude + 0.1, self.plot_height / 2)
        lon_ticks = np.arange(self.upperleftpoint.longitude, self.bottomrightpoint.longitude + 0.1, self.plot_width / 2)
    
        m.drawparallels(lat_ticks, linewidth=1.0, labels=[1,0,0,0])
        m.drawmeridians(lon_ticks, linewidth=1.0, labels=[0,0,0,1])
        m.drawstates()
        m.drawcountries()
    
        alons = np.arange(self.upperleftpoint.longitude, self.bottomrightpoint.longitude, self.spacing)
        alats = np.arange(self.bottomrightpoint.latitude, self.upperleftpoint.latitude, self.spacing)
        lons = np.linspace(self.upperleftpoint.longitude, self.bottomrightpoint.longitude - self.spacing, self.num_x-1)
        lats = np.linspace(self.bottomrightpoint.latitude, self.upperleftpoint.latitude - self.spacing, self.num_y-1)
    
        # Get the properties.
        datapoints = np.arange(self.num_x * self.num_y,dtype=np.float32).reshape(self.num_y, self.num_x)

        nancnt=0
        zerocnt=0
        negcnt=0
        print ("total cnt is ",self.num_x * self.num_y)
        for i in xrange(0, self.num_y):
            for j in xrange(0, self.num_x):
                if property != "poisson":
                    if color_scale == "sd" or color_scale == "sd_r":
                        datapoints[i][j] = self.materialproperties[i][j].getProperty(property)
                        if(datapoints[i][j] == -1 ) :
                            datapoints[i][j]=np.nan
                            nancnt=nancnt+1
##to have blank background
##                        if (datapoints[i][j] == 0) :
##                            datapoints[i][j]=np.nan
##                            zerocnt=zerocnt+1
##
                    else:
                        datapoints[i][j] = self.materialproperties[i][j].getProperty(property) / 1000
                        if (datapoints[i][j] == 0) :
# KEEP 0 as 0                           datapoints[i][j]=np.nan
                           zerocnt=zerocnt+1
                        if (datapoints[i][j] < 0) :
                           negcnt=negcnt+1
                        if(datapoints[i][j] == -1 ) :
                           nancnt=nancnt+1
                elif self.materialproperties[i][j].vp == 0 or self.materialproperties[i][j].vs == 0.0:
                    datapoints[i][j] = 0.0
                else:
                    datapoints[i][j] = self.materialproperties[i][j].vp / self.materialproperties[i][j].vs

#        print (" total number of nancnt is ", nancnt)
#        print (" total number of zerocnt is ", zerocnt)
#        print (" total number of negcnt is ", negcnt)

        self.max_val=np.nanmax(datapoints)
        self.min_val=np.nanmin(datapoints)
        self.mean_val=np.mean(datapoints)

        if color_scale == "s":
            colormap = basemap.cm.GMT_seis
            norm = mcolors.Normalize(vmin=BOUNDS[0],vmax=BOUNDS[len(BOUNDS) - 1])
        elif color_scale == "s_r":
            colormap = basemap.cm.GMT_seis_r
            norm = mcolors.Normalize(vmin=BOUNDS[0],vmax=BOUNDS[len(BOUNDS) - 1])
        elif color_scale == "sd":
            BOUNDS= u.makebounds(self.min_val, self.max_val, 5, self.mean_val, substep=5)
            colormap = basemap.cm.GMT_globe
            TICKS = u.maketicks(self.min_val, self.max_val, 5)
            norm = mcolors.Normalize(vmin=self.min_val,vmax=self.max_val)
        elif color_scale == "b":
            C = []
            for bound in BOUNDS :
               if bound < scale_gate :
                  C.append("grey")
               else:
                  C.append("red")
            colormap = mcolors.ListedColormap(C)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)
        elif color_scale == "d":
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_seis, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)  
        elif color_scale == "d_r":
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_seis_r, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)  
        elif color_scale == 'dd':
            BOUNDS= u.makebounds(self.min_val, self.max_val, 5, self.mean_val, substep=5)
            TICKS = u.maketicks(self.min_val, self.max_val, 5)
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_globe, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)
        else:
            print "ERROR: unknown option for colorscale."

        if( datafile == None ):
          meta['num_x'] = self.num_x
          meta['num_y'] = self.num_y
          meta['datapoints'] = datapoints.size
          meta['max'] = np.asscalar(self.max_val)
          meta['min'] = np.asscalar(self.min_val)
          meta['mean'] = np.asscalar(self.mean_val)
          meta['lon_list']=lons.tolist()
          meta['lat_list']=lats.tolist()
          if filename:
              u.export_metadata(meta,filename)
              u.export_binary(datapoints,filename)
                    
        t = m.transform_scalar(datapoints, lons, lats, len(lons), len(lats))
        img = m.imshow(t, cmap=colormap, norm=norm)

       
#        print "MIN is ", np.nanmin(datapoints)
#        print "MAX is ", np.nanmax(datapoints)
#        img=m.scatter(xlist, ylist, c=dlist, cmap=colormap, norm=norm, s=1, edgecolor='',marker='o')      
#        img=m.scatter(xcoords, ycoords, c=datapoints, cmap=colormap, norm=norm, s=1, edgecolor='',marker='o')      
    
        m.drawcoastlines()
    
        cax = plt.axes([0.125, 0.05, 0.775, 0.02])
        cbar = plt.colorbar(img, cax=cax, orientation='horizontal',spacing='proportional',ticks=TICKS)
        if property != "poisson":
            if horizontal_label == None:
                cbar.set_label(property.title() + " (km/s)")
            else:
                cbar.set_label(horizontal_label)
        else:
            cbar.set_label("Vp/Vs")
            
        if filename:
            plt.savefig(filename)
## MEI, TODO p.savehtml("show.html")
        else:
            plt.show()
