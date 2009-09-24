# Generate analysis of precipitation

import sys, os, random
sys.path.append("../lib/")
import iemplot

import mx.DateTime
now = mx.DateTime.now()

from pyIEM import iemdb
i = iemdb.iemdb()
iem = i['iem']

# Compute normal from the climate database
sql = """
select station, network,
  x(geom) as lon, y(geom) as lat, 
  sum(pday) as rainfall
from summary 
WHERE day = 'TODAY' 
and (network ~* 'ASOS' or network = 'AWOS')
and pday >= 0 and pday < 30
GROUP by station, lon, lat, network
"""

lats = []
lons = []
vals = []
valmask = []
rs = iem.query(sql).dictresult()
for i in range(len(rs)):
  lats.append( rs[i]['lat'] )
  lons.append( rs[i]['lon'] + (random.random() * 0.01))
  vals.append( rs[i]['rainfall'] )
  valmask.append(  (rs[i]['network'] in ['AWOS','IA_ASOS']) )

cfg = {
 'wkColorMap': 'BlAqGrYeOrRe',
 'nglSpreadColorStart': -1,
 'nglSpreadColorEnd'  : 2,
 '_showvalues'        : True,
 '_format'            : '%.2f',
 '_title'             : "Iowa ASOS/AWOS Rainfall Reports",
 '_valid'             : "%s" % (now.strftime("%d %b %Y"), ),
 'lbTitleString'      : "[inch]",
 'pmLabelBarHeightF'  : 0.6,
 'pmLabelBarWidthF'   : 0.1,
 'lbLabelFontHeightF' : 0.025,
 '_valuemask'         : valmask
}
# Generates tmp.ps
iemplot.simple_contour(lons, lats, vals, cfg)

os.system("convert -rotate -90 -trim -border 5 -bordercolor '#fff' -resize 900x700 -density 120 +repage tmp.ps tmp.png")
os.system("/home/ldm/bin/pqinsert -p 'plot c 000000000000 summary/today_prec.png bogus png' tmp.png")
if os.environ["USER"] == "akrherz":
  os.system("xv tmp.png")
os.remove("tmp.png")
os.remove("tmp.ps")
