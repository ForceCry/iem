import time
import osgeo.gdal as gdal
import random
import osgeo.gdal_array
from osgeo.gdalconst import *
import numpy, mx.DateTime, os, shutil, urllib2, sys

def run(sts):
    """
    Generate max dBZ composite for a given UTC date
    """
    ets = sts + mx.DateTime.RelativeDateTime(days=1)
    interval = mx.DateTime.RelativeDateTime(minutes=5)

    # Load the color table
    n0r = gdal.Open('../../htdocs/docs/nexrad_composites/reflect_ramp.png', 0)
    n0rct = n0r.GetRasterBand(1).GetRasterColorTable().Clone()
  
    # Loop over our archived files and do what is necessary
    maxn0r = None
    now = sts
    while now < ets:
        fp = now.strftime("/mesonet/ARCHIVE/data/%Y/%m/%d/GIS/uscomp/n0r_%Y%m%d%H%M.png")
        if (not os.path.isfile(fp)):
            print "MISSING:", fp
            now += interval
            continue
        n0r = gdal.Open(fp, 0)
        n0rd = numpy.ravel( n0r.ReadAsArray() )
        if maxn0r is None:
            maxn0r = n0rd
        maxn0r = numpy.where( n0rd > maxn0r, n0rd, maxn0r)

        now += interval


    out_driver = gdal.GetDriverByName("gtiff")
    outdataset = out_driver.Create('max.tiff', n0r.RasterXSize, n0r.RasterYSize, n0r.RasterCount, GDT_Byte)
    # Set output color table to match input
    outdataset.GetRasterBand(1).SetRasterColorTable( n0rct )
    outdataset.GetRasterBand(1).WriteArray( numpy.resize(maxn0r, (n0r.RasterYSize, n0r.RasterXSize))  )
    del outdataset

    os.system("convert max.tiff max.png")
    # Insert into LDM
    cmd = "/home/ldm/bin/pqinsert -p 'plot a %s0000 bogus GIS/uscomp/max_n0r_0z0z_%s.png png' max.png" % (
                                            sts.strftime("%Y%m%d"), sts.strftime("%Y%m%d") )
    os.system(cmd)

    # Create tmp world file
    out = open('/tmp/tmpwld%s.wld' % (sts.strftime("%Y%m%d"),), 'w')
    out.write("""   0.010000000000%s
   0.00000
   0.00000
  -0.01000000000000%s
-126.000000
  50.0000""" % (random.randint(0,1000), random.randint(0,1000) ) )
    out.close()
  
    # Insert world file as well
    cmd = "/home/ldm/bin/pqinsert -p 'plot a %s0000 bogus GIS/uscomp/max_n0r_0z0z_%s.wld wld' /tmp/tmpwld%s.wld" % (
         sts.strftime("%Y%m%d"), sts.strftime("%Y%m%d"),  sts.strftime("%Y%m%d") )
    os.system(cmd)

    # cleanup
    os.remove("max.tiff")
    os.remove("max.png")
    os.remove( '/tmp/tmpwld%s.wld' % (sts.strftime("%Y%m%d"),) )
  
    # Sleep for a bit
    time.sleep(60)
  
    # Iowa
    png = urllib2.urlopen("http://iemvs105.local/GIS/radmap.php?layers[]=uscounties&layers[]=nexrad_tc&ts=%s" % (
                                                                        sts.strftime("%Y%m%d%H%M"),))
    o = open('tmp.png', 'wb')
    o.write( png.read() )
    o.close()
    cmd = "/home/ldm/bin/pqinsert -p 'plot ac %s0000 summary/max_n0r_0z0z_comprad.png comprad/max_n0r_0z0z_%s.png png' tmp.png" % (
                                                                    sts.strftime("%Y%m%d"), sts.strftime("%Y%m%d") )
    os.system(cmd)

    # US
    png = urllib2.urlopen("http://iemvs105.local/GIS/radmap.php?sector=conus&layers[]=uscounties&layers[]=nexrad_tc&ts=%s" % (
                                                                        sts.strftime("%Y%m%d%H%M"),))
    o = open('tmp.png', 'wb')
    o.write( png.read() )
    o.close()
    cmd = "/home/ldm/bin/pqinsert -p 'plot ac %s0000 summary/max_n0r_0z0z_usrad.png usrad/max_n0r_0z0z_%s.png png' tmp.png" % (
                                                                        sts.strftime("%Y%m%d"), sts.strftime("%Y%m%d") )
    os.system(cmd)
    os.remove("tmp.png")

"""
s = mx.DateTime.DateTime(2008,6,6)
e = mx.DateTime.DateTime(2008,6,7)
now = s
while (now < e):
  print now
  run(now)
  now += mx.DateTime.RelativeDateTime(days=1)
"""

ts = mx.DateTime.now() + mx.DateTime.RelativeDateTime(hour=0,minute=0)
run( ts )


