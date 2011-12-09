"""
Create an analysis of LSR snowfall reports
"""

import sys, os, numpy
import iemplot

import mx.DateTime, random
now = mx.DateTime.now()
import iemdb
POSTGIS = iemdb.connect('postgis', bypass=True)
pcursor = POSTGIS.cursor()

vals = []
valmask = []
lats = []
lons = []
pcursor.execute("""SELECT state, 
      max(magnitude) as val, x(geom) as lon, y(geom) as lat
      from lsrs_2011 WHERE type in ('S') and magnitude >= 0 and 
      valid > now() - '12 hours'::interval
      GROUP by state, lon, lat""")
for row in pcursor:
  vals.append( row[1] )
  lats.append( row[3] )
  lons.append( row[2] )
  valmask.append( row[0] in ['IA',] )

if len(vals) < 2:
  vals = [1., .02, .03]
  valmask = [False, False, False]
  lons = [-90.1,-90.,-85.]
  lats = [41.,41.1,50.]

# Now, we need to add in zeros, lets say we are looking at a .25 degree box
buffer = 1.0
for lat in numpy.arange(iemplot.IA_SOUTH, iemplot.IA_NORTH, buffer):
  for lon in numpy.arange(iemplot.IA_WEST, iemplot.IA_EAST, buffer):
    found = False
    for j in range(len(lats)):
      if (lats[j] > (lat-(buffer/2.)) and lats[j] < (lat+(buffer/2.)) and
         lons[j] > (lon-(buffer/2.)) and lons[j] < (lon+(buffer/2.)) ):
        found = True
    if not found:
      lats.append( lat )
      lons.append( lon )
      valmask.append( False )
      vals.append( 0 )

cfg = {
 'wkColorMap': 'WhiteBlueGreenYellowRed',
 'nglSpreadColorStart': 2,
 'nglSpreadColorEnd'  : -1,
 '_valuemask'         : valmask,
 '_title'             : "Local Storm Report Snowfall Total Analysis",
 '_valid'             : "Reports past 12 hours: "+ now.strftime("%d %b %Y %I:%M %p"),
 '_showvalues'        : True,
 '_format'            : '%.1f',
 '_MaskZero'          : True,
 'lbTitleString'      : "[in]",
}
# Generates tmp.ps
tmpfp = iemplot.simple_contour(lons, lats, vals, cfg)
pqstr = "plot c 000000000000 lsr_snowfall.png bogus png"
thumbpqstr = "plot c 000000000000 lsr_snowfall_thumb.png bogus png"
iemplot.postprocess(tmpfp,pqstr, thumb=True, thumbpqstr=thumbpqstr)
