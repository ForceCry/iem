from mpl_toolkits.basemap import Basemap, cm
import matplotlib
import matplotlib.pyplot as plt
from osgeo import ogr
from shapely.wkb import loads
from numpy import asarray
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import pylab
import math
import iemplot
import iemdb
import Image
import mx.DateTime
POSTGIS = iemdb.connect('postgis', bypass=True)
pcursor = POSTGIS.cursor()

from iem import plot
maue = plot.maue(15)
bins = [1,2,3,4,5,7,10,15,20,25,30,35,40,50,75,100]

def get_color(val, minvalue, maxvalue):
    if val < bins[0]:
        return "None"
    for i in range(1,len(bins)):
        if val < bins[i]:
            return maue(i-1)
    return maue(14)



fig = plt.figure(num=None, figsize=(10.24,7.68))
#fig = plt.figure(num=None, figsize=(3.55,2.9))
# Set the axes instance
ax = plt.axes([0.01,0,0.9,1], axisbg=(0.4471,0.6235,0.8117))
ak_ax = plt.axes([0.01,0.0,0.25,0.25], axisbg=(0.4471,0.6235,0.8117), anchor='SW')
hi_ax = plt.axes([0.48,0.0,0.2,0.2], axisbg=(0.4471,0.6235,0.8117), anchor='SW') 

# Set up the map
m = Basemap(projection='lcc', 
             urcrnrlat=47.7, llcrnrlat=23.08, urcrnrlon=-62.5, llcrnrlon=-120, 
             #urcrnrlat=44.7, llcrnrlat=38.08, urcrnrlon=-86.5, llcrnrlon=-102, 
             lon_0=-98.7, lat_0=39, lat_1=33, lat_2=45,
             resolution='l', ax=ax)
m.fillcontinents(color='0.7',zorder=0)

akmap = Basemap(projection='cyl', urcrnrlat=78.1, llcrnrlat=48.08, urcrnrlon=-129.0,
             llcrnrlon=-179.5,
             resolution='l', ax=ak_ax)
akmap.fillcontinents(color='0.7',zorder=0)
himap = Basemap(projection='cyl', urcrnrlat=22.5, llcrnrlat=18.5, urcrnrlon=-154.0,
             llcrnrlon=-161.0,
             resolution='l', ax=hi_ax)
himap.fillcontinents(color='0.7',zorder=0)

m.drawstates()
m.drawcountries()
#akmap.drawstates()
himap.drawstates()

source = ogr.Open("PG:host=iemdb dbname=postgis user=nobody")
data = source.ExecuteSQL("""
 ---select n.ugc, foo.data, ST_Simplify(n.geom,0.01) from nws_ugc n 
 ---LEFT OUTER JOIN (select ugc, count(*) as data from warnings 
 ---                 where phenomena in ('BZ') and significance = 'W' 
 ---                 and gtype = 'C' GROUP by ugc) as foo 
 ---ON (n.ugc = foo.ugc) WHERE n.polygon_class = 'Z' 
 ---ORDER by data DESC NULLS LAST
 
 select n.ugc, foo.data, ST_Simplify(n.geom,0.01) from nws_ugc n 
 LEFT JOIN (select ugc, count(*) as data from warnings 
                  where phenomena in ('BZ') and significance = 'W' 
                  and gtype = 'C' GROUP by ugc) as foo 
 ON (n.ugc = foo.ugc) 
 ORDER by data ASC NULLS FIRST
 
""")
maxV = 22
patches = []
akpatches = []
hipatches = []
while 1:
    feature = data.GetNextFeature()
    #print dir(feature)
    if not feature:
        break
    cnt = feature.GetField('data')
    ugc = feature.GetField('ugc')
    if ugc is None:
        continue
    if not maxV and cnt and cnt > maxV:
        maxV = int(cnt + 1.0)
        print maxV
    if cnt is None or float(cnt) == 0:
        c = 'w'
    else:
        c = get_color(cnt, 0,100)
    geom = loads(feature.GetGeometryRef().ExportToWkb())
    print ugc, cnt, c
    for polygon in geom:
        if polygon.exterior is None:
            continue
        a = asarray(polygon.exterior)
        if ugc[:2] == 'AK':
            x,y = akmap(a[:,0], a[:,1])
            a = zip(x,y)
            p = Polygon(a,fc=c,ec=None,zorder=2, lw=.1)
            akpatches.append(p)
            pass
        elif ugc[:2] == 'HI':
            x,y = himap(a[:,0], a[:,1])
            a = zip(x,y)
            p = Polygon(a,fc=c,ec=None,zorder=2, lw=.1)
            hipatches.append(p)
        else:
            x,y = m(a[:,0], a[:,1])
            a = zip(x,y)
            p = Polygon(a,fc=c,ec=None,zorder=2, lw=.1)
            patches.append(p)


ax.add_collection(PatchCollection(patches,match_original=True))
ak_ax.add_collection( PatchCollection(akpatches,match_original=True) )
hi_ax.add_collection( PatchCollection(hipatches,match_original=True) )

import numpy
import matplotlib.patheffects as PathEffects

axaa = plt.axes([0.92, 0.1, 0.07, 0.8], frameon=False,
                      yticks=[], xticks=[])
colors = []
for i in range(len(bins)):
    colors.append( rgb2hex(maue(i)) )
    txt = axaa.text(0.5, i, "%s" % (bins[i],), ha='center', va='center',
                          color='w')
    txt.set_path_effects([PathEffects.withStroke(linewidth=2,
                                                     foreground="k")])
axaa.barh(numpy.arange(len(bins)), [1]*len(bins), height=1,
                color=maue(range(len(bins))),
                ec='None')


ax.text(0.17, 1.1, '1 Oct 2005 - 10 Feb 2013 Blizzard Warnings', transform=ax.transAxes,
     size=13,
    horizontalalignment='left', verticalalignment='center')

#ax.text(0.17, 1.005, 'Map Generated: %s' % (mx.DateTime.now().strftime("%d %B %Y %H:%M %p %Z"),), transform=ax.transAxes,
#     size=9,
#    horizontalalignment='left', verticalalignment='bottom')

# Logo!
logo = Image.open('../../htdocs/images/logo_small.png')
ax3 = plt.axes([0.05,0.87,0.1,0.1], frameon=False, axisbg=(0.4471,0.6235,0.8117), yticks=[], xticks=[])
ax3.imshow(logo)

#plt.text(0.08, 0.035,'Iowa State University', size='small', color='#222d7d',
#     horizontalalignment='center',
#     verticalalignment='center',
#     transform = ax.transAxes)

axaa.text(-2., 0.5, 'Count', transform=axaa.transAxes,
    size='medium', color='k', horizontalalignment='center',
    rotation='vertical', verticalalignment='center')



fig.savefig('test.png')
#iemplot.makefeature('test')
