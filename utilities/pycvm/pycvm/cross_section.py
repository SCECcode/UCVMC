##
#  @file cross_section.py
#  @brief Plots a cross section to an image or a pre-existing plot.
#  @author David Gill - SCEC <davidgil@usc.edu>
#  @version 14.7.0
#
#  Allows for generation of a cross section between two points.

#  Imports
from mpl_toolkits import basemap
from mpl_toolkits.basemap import cm
from common import Plot, Point, MaterialProperties, UCVM, UCVM_CVMS, \
                   math, pycvm_cmapDiscretize, cm, mcolors, basemap, np, plt

import pdb
import random
import string

try:
    import pyproj
except StandardError, e:
    print "ERROR: PyProj must be installed for this script to work."
    exit(1)

##
#  @class CrossSection
#  @brief Plots a cross section between two @link common.Point Points @endlink.
#
#  Generates a cross section that can either be saved as a file or displayed
#  to the user. 
class CrossSection:
    
    ##
    #  Initializes the cross section class.
    #
    #  @param startingpoint The @link common.Point starting point @endlink from which this plot should start.
    #  @param endingpoint The @link common.Point ending point @endlink at which this plot will end.
    #  @param todepth The ending depth, in meters, where this plot should end.
    #  @param hspacing The discretization interval in meters, horizontally.
    #  @param vspacing The discretization interval in meters, vertically.
    #  @param cvm The CVM from which to retrieve these material properties.
    def __init__(self, startingpoint, endingpoint, todepth, hspacing, vspacing, cvm):
        if not isinstance(startingpoint, Point):
            raise TypeError("The starting point must be an instance of Point.")
        else:
            ## Defines the @link common.Point starting point @endlink for the cross section.
            self.startingpoint = startingpoint
            
        if not isinstance(endingpoint, Point):
            raise TypeError("The ending point must be an instance of Point.")
        else:
            ## Defines the @link common.Point ending point @endlink for the cross section.
            self.endingpoint = endingpoint
        
        if (todepth - self.startingpoint.depth) % vspacing != 0:
            raise ValueError("%s\n%s\n%s" % ("The spacing value does not divide evenly into the requested depth. ", \
                          "Please make sure that the depth (%.2f - %.2f) divided by the spacing " % (todepth, startingpoint.depth), \
                          "%.2f has no remainder" % (vspacing)))
        else:
            ## Defines the depth to which the plot should go in meters.
            self.todepth = todepth
            
        ## The vertical discretization of the plot, in meters.
        self.vspacing = vspacing
        
        ## The horizontal discretization of the plot, in meters.
        self.hspacing = hspacing
        
        ## The CVM to use (must be installed with UCVM).
        self.cvm = cvm

    ## 
    #  Generates the depth profile in a format that is ready to plot.
    def getplotvals(self, property='vs', datafile = None):

        point_list = []
        lon_list = []
        lat_list = []
        depth_list = []

        proj = pyproj.Proj(proj='utm', zone=11, ellps='WGS84')

        x1, y1 = proj(self.startingpoint.longitude, self.startingpoint.latitude)
        x2, y2 = proj(self.endingpoint.longitude, self.endingpoint.latitude)

        num_prof = int(math.sqrt((x2-x1)*(x2-x1) + \
                                 (y2-y1)*(y2-y1))/self.hspacing)
        
#        cnt=0
        jstart = self.startingpoint.depth
        for j in xrange(int(self.startingpoint.depth), int(self.todepth) + 1, int(self.vspacing)):
            depth_list.append( round(j,3))
            for i in xrange(0, num_prof + 1):
                x = x1 + i*(x2-x1)/float(num_prof)
                y = y1 + i*(y2-y1)/float(num_prof)
                lon, lat = proj(x, y, inverse=True)
                point_list.append(Point(lon, lat, j))
                if ( j == jstart) :
                  lon_list.append( round(lon,5))
                  lat_list.append( round(lat,5))
#                if(cnt < 10) :
#                   print("point.. lon ",lon, " lat ",lat," j ",j)
#                   cnt += 1
                
        self.lon_list=lon_list
        self.lat_list=lat_list
        self.depth_list=depth_list
#        print("total points generated..", len(point_list))
#        print("total lon..", len(lon_list))
#        print("total lat..", len(lat_list))
#        print("total lat..", len(depth_list))

        u = UCVM()

### MEI -- TODO, need to have separate routine that generates cross section datafile
        if (datafile != None) :
            ## Private number of x points.
            self.num_x = num_prof +1
            ## Private number of y points.
            self.num_y = (int(self.todepth) - int(self.startingpoint.depth)) / int(self.vspacing) +1
            print "\nUsing -->"+datafile
            print "expecting x ",self.num_x," y ",self.num_y
            data = u.import_binary(datafile, self.num_x, self.num_y)
## this set of data is only for --datatype: either 'vs', 'vp', 'rho', or 'poisson'
        ## The 2D array of retrieved material properties.
            self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in xrange(self.num_x)] for x in xrange(self.num_y)] 
            datapoints = data.reshape(self.num_y, self.num_x)

            for y in xrange(0, self.num_y):
                for x in xrange(0, self.num_x):   
                    tmp=datapoints[y][x] *1000
                    if(property == 'vp'):
                      self.materialproperties[y][x].setProperty('Vp',tmp)
                    if(property == 'rho'):
                      self.materialproperties[y][x].setProperty('Rho',tmp)
                    if(property == 'poisson'):
                      self.materialproperties[y][x].setProperty('Poisson',tmp)
                    if(property == 'vs'):
                      self.materialproperties[y][x].setProperty('Vs',tmp)
        else:
            data = u.query(point_list, self.cvm)


            ## Private number of x points.
            self.num_x = num_prof + 1
            ## Private number of y points.
            self.num_y = (int(self.todepth) - int(self.startingpoint.depth)) / int(self.vspacing) + 1
        
        ## The 2D array of retrieved material properties.
            self.materialproperties = [[MaterialProperties(-1, -1, -1) for x in xrange(self.num_x)] for x in xrange(self.num_y)] 

        
            for y in xrange(0, self.num_y):
                for x in xrange(0, self.num_x):   
                    self.materialproperties[y][x] = data[y * self.num_x + x]     
    ## 
    #  Plots the horizontal slice either to an image or a file name.
    # 
    #  @param property The property either as a single item array or string.
    #  @param filename The file name of the image if we're saving it. Optional.
    #  @param title The title for the plot. Optional.
    #  @param color_scale The color scale to use. Optional.
    #  @param scale_gate The gate to use to create customized listed colormap. Optional.
    #  @param meta The meta data used to create the cross plot 
    def plot(self, property, filename = None, title = None, color_scale = "d", scale_gate=2.5, datafile = None, meta = {}):
        
        if self.startingpoint.description == None:
            location_text = ""
        else:
            location_text = self.startingpoint.description + " "

        # Gets the better CVM description if it exists.
        try:
            cvmdesc = UCVM_CVMS[self.cvm]
        except: 
            cvmdesc = self.cvm

        if title == None:
            title = "%s%s Cross Section from (%.2f, %.2f) to (%.2f, %.2f)" % (location_text, cvmdesc, self.startingpoint.longitude, \
                        self.startingpoint.latitude, self.endingpoint.longitude, self.endingpoint.latitude)
            
        self.getplotvals(property=property, datafile = datafile)
        
        # Call the plot object.
        p = Plot(None, None, None, None, 10, 10)

        plt.axes([0.1,0.7,0.8,0.25])
    
        # Figure out which is upper-right and bottom-left.
        ur_lat = self.startingpoint.latitude if self.startingpoint.latitude > self.endingpoint.latitude else self.endingpoint.latitude
        ur_lon = self.startingpoint.longitude if self.startingpoint.longitude > self.endingpoint.longitude else self.endingpoint.longitude
        ll_lat = self.startingpoint.latitude if self.startingpoint.latitude < self.endingpoint.latitude else self.endingpoint.latitude
        ll_lon = self.startingpoint.longitude if self.startingpoint.longitude < self.endingpoint.longitude else self.endingpoint.longitude
    
        # Add 1% to each for good measure.
        ur_lat = ur_lat + 0.03 * ur_lat
        ur_lon = ur_lon - 0.015 * ur_lon
        ll_lat = ll_lat - 0.03 * ll_lat
        ll_lon = ll_lon + 0.015 * ll_lon
    
        # Plot map up top.
        m = basemap.Basemap(projection='cyl', llcrnrlat=ll_lat, urcrnrlat=ur_lat, \
                            llcrnrlon=ll_lon, urcrnrlon=ur_lon, \
                            resolution='f', anchor='C')
    
        lat_ticks = np.arange(ll_lat, ur_lat + 0.1, (ur_lat - ll_lat))
        lon_ticks = np.arange(ll_lon, ur_lon + 0.1, (ur_lon - ll_lon))
    
        m.drawparallels(lat_ticks, linewidth=1.0, labels=[1,0,0,0])
        m.drawmeridians(lon_ticks, linewidth=1.0, labels=[0,0,0,1])
        m.drawstates()
        m.drawcountries()
    
        m.drawcoastlines()
        m.drawmapboundary(fill_color='aqua')
        m.fillcontinents(color='brown',lake_color='aqua')
    
        m.plot([self.startingpoint.longitude,self.endingpoint.longitude], [self.startingpoint.latitude,self.endingpoint.latitude])
    
        valign1 = "top"
        valign2 = "bottom"
        if self.endingpoint.latitude < self.startingpoint.latitude:
            valign1 = "bottom"
            valign2 = "top"
    
        plt.text(self.startingpoint.longitude, self.startingpoint.latitude, \
                 '[S] %.1f, %.1f' % (self.startingpoint.longitude, self.startingpoint.latitude), \
                 color='k', horizontalalignment="center", verticalalignment=valign1)
    
        plt.text(self.endingpoint.longitude, self.endingpoint.latitude, \
                 '[E] %.1f, %.1f' % (self.endingpoint.longitude, self.endingpoint.latitude), \
                 color='k', horizontalalignment="center", verticalalignment=valign2)
    
        plt.axes([0.05,0.18,0.9,0.54])
    
        datapoints = np.arange(self.num_x * self.num_y,dtype=np.float32).reshape(self.num_y, self.num_x)
            
        for y in xrange(0, self.num_y):
            for x in xrange(0, self.num_x):   
                datapoints[y][x] = self.materialproperties[y][x].getProperty(property) / 1000          

        u = UCVM()

        self.max_val=np.nanmax(datapoints)
        self.min_val=np.nanmin(datapoints)
        self.mean_val=np.mean(datapoints)

        BOUNDS = u.makebounds()
        TICKS = u.maketicks()

        if property == "vp":
            BOUNDS = [bound * 1.7 for bound in BOUNDS]
            TICKS = [tick * 1.7 for tick in TICKS]

        # Set default colormap and range
        colormap = basemap.cm.GMT_seis
        norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)

        umax=round(self.max_val)
        if( umax < 5 ) :
            umax=5 
        umin=round(self.min_val)

        if color_scale == "s":
            colormap = basemap.cm.GMT_seis
            norm = mcolors.Normalize(vmin=0,vmax=umax)
        elif color_scale == "s_r":
            colormap = basemap.cm.GMT_seis_r
            norm = mcolors.Normalize(vmin=0,vmax=umax)
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
        elif color_scale == 'd':
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_seis, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)  
        elif color_scale == 'd_r':
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_seis_r, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)  
        elif color_scale == 'dd':
            BOUNDS= u.makebounds(self.min_val, self.max_val, 5, self.mean_val, substep=5)
            TICKS = u.maketicks(self.min_val, self.max_val, 5)
            colormap = pycvm_cmapDiscretize(basemap.cm.GMT_globe, len(BOUNDS) - 1)
            norm = mcolors.BoundaryNorm(BOUNDS, colormap.N)
        else: 
            print "ERROR: unknown option for colorscale."
    

## MEI, TODO this is a temporary way to generate an output of a cross_section input file
        if( datafile == None ):
          meta['num_x'] = self.num_x
          meta['num_y'] = self.num_y
          meta['datapoints'] = datapoints.size
          meta['max'] = np.asscalar(self.max_val)
          meta['min'] = np.asscalar(self.min_val)
          meta['mean'] = np.asscalar(self.mean_val)
          meta['lon_list'] = self.lon_list
          meta['lat_list'] = self.lat_list
          meta['depth_list'] = self.depth_list
          if filename:
              u.export_metadata(meta,filename)
              u.export_binary(datapoints,filename)
          else:
#https://stackoverflow.com/questions/2257441/random-string-generation-with-upper-case-letters-and-digits-in-python
              rnd=''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(6))
              f = "cross_section"+rnd
              u.export_metadata(meta,f)
              u.export_binary(datapoints,f)

        img = plt.imshow(datapoints, cmap=colormap, norm=norm)
        plt.xticks([0,self.num_x/2,self.num_x], ["[S] %.3f" % self.startingpoint.longitude, \
                                                 "%.3f" % ((float(self.endingpoint.longitude) + float(self.startingpoint.longitude)) / 2), \
                                                 "[E] %.3f" % self.endingpoint.longitude])
        plt.yticks([0,self.num_y/2,self.num_y], ["%.2f" % (self.startingpoint.depth/1000), \
                                                 "%.2f" % (self.startingpoint.depth+ ((self.todepth-self.startingpoint.depth)/2)/1000), \
                                                 "%.2f" % (self.todepth / 1000)])
    
        plt.title(title)
    
        cax = plt.axes([0.1, 0.1, 0.8, 0.02])
        cbar = plt.colorbar(img, cax=cax, orientation='horizontal',ticks=TICKS,spacing='regular')
        if property != "poisson":
            cbar.set_label(property.title() + " (km/s)")
        else:
            cbar.set_label("Vp/Vs")
       
        if filename:
            plt.savefig(filename)
        else:
            plt.show() 
