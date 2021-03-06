"""
 Grid the climodat data onto a midwest grid for IEMRE
"""
import sys
import netCDF4
import numpy
import mx.DateTime
import iemdb
import mesonet
import Ngl
import iemre
import network
import random
import mesonet
from psycopg2.extras import DictCursor

COOP = iemdb.connect('coop', bypass=True)
ccursor = COOP.cursor(cursor_factory=DictCursor)

nt = network.Table(('IACLIMATE', 'ILCLIMATE', 'INCLIMATE',
         'OHCLIMATE','MICLIMATE','KYCLIMATE','WICLIMATE','MNCLIMATE',
         'SDCLIMATE','NDCLIMATE','NECLIMATE','KSCLIMATE','MOCLIMATE'))
locs = nt.sts

def generic_gridder(rs, idx):
    """
    Generic gridding algorithm for easy variables
    """
    lats = []
    lons = []
    vals = []
    for row in rs:
        stid = row['station']
        if row[idx] is not None and locs.has_key(stid):
            lats.append(  locs[stid]['lat'] + (random.random() * 0.01) )
            lons.append(  locs[stid]['lon'] )
            vals.append( row[idx]  )
    if len(vals) < 4:
        print "Only %s observations found for %s, won't grid" % (len(vals),
               idx)
        return None
    grid = Ngl.natgrid(lons, lats, vals, iemre.XAXIS, iemre.YAXIS)
    if grid is not None:
        return grid.transpose()
    else:
        return None


def grid_day(nc, ts):
    """
    I proctor the gridding of data on an hourly basis
    @param ts Timestamp of the analysis, we'll consider a 20 minute window
    """
    offset = int((ts - (ts + mx.DateTime.RelativeDateTime(month=1,day=1,hour=0))).days)


    sql = """SELECT * from alldata WHERE day = '%s' and
             substr(station,3,4) != '0000' """ % (
         ts.strftime("%Y-%m-%d"), )
    ccursor.execute( sql )
    if ccursor.rowcount > 4:
        res = generic_gridder(ccursor, 'high')
        if res is not None:
            nc.variables['high_tmpk'][offset] = iemre.f2k(res)
        ccursor.scroll(0, mode='absolute')
        res = generic_gridder(ccursor, 'low')
        if res is not None:
            nc.variables['low_tmpk'][offset] = iemre.f2k(res)
        ccursor.scroll(0, mode='absolute')
        res = generic_gridder(ccursor, 'precip')
        if res is not None:
            nc.variables['p01d'][offset] = res * 25.4
    else:
        print "%s has %02i entries, FAIL" % (ts.strftime("%Y-%m-%d"), 
            len(rs))

def main(ts):

    # Load up our netcdf file!
    nc = netCDF4.Dataset("/mnt/mesonet/data/iemre/%s_mw_daily.nc" % (ts.year,), 'a')
    grid_day(nc , ts)
    nc.close()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        ts = mx.DateTime.DateTime( int(sys.argv[1]),int(sys.argv[2]),
                           int(sys.argv[3]) )
    else:
        ts = mx.DateTime.now() - mx.DateTime.RelativeDateTime(days=1,hour=0,minute=0, second=0)
    main(ts)
