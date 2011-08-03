# Tired of all the junk precip data from the ISUAG network

import sys
sys.path.insert(0, "../iemre")
import constants
import mx.DateTime
import netCDF3
import numpy
from pyIEM import iemdb
i = iemdb.iemdb()
isuag = i['isuag']
mesosite = i['mesosite']

SKIP = ['A134759', # Lewis
        'A133259',
        'A135849', #Muscatine
        'A135879', #Nashua
        'A134309', #Kanawha
]

sts = {}
rs = mesosite.query("SELECT id, x(geom) as lon, y(geom) as lat, name from stations WHERE network = 'ISUAG'").dictresult()
for i in range(len(rs)):
    sts[ rs[i]['id'] ] = rs[i]

def fix_daily(ts):
    """
    Instead of using the IEMRE value, we should total up the hourly
    data, so to confuse people less
    """
    # Find ISUAG Data
    rs = isuag.query("""SELECT sum(c900) as rain, station from hourly 
	WHERE date(valid) = '%s' GROUP by station""" % (ts.strftime("%Y-%m-%d"),)).dictresult()
    for i in range(len(rs)):
        stid = rs[i]['station']
        if stid in SKIP:
          continue
        rain = rs[i]['rain']
        # Fix it
        sql = """UPDATE daily SET c90 = %.2f, c90_f = 'e' WHERE valid = '%s'
              and station = '%s'""" % (rain, ts.strftime("%Y-%m-%d"),
              stid)
        isuag.query(sql)

def fix_hourly(ts):

    """
    Fix the hourly precipitation values, just hard code the stupid IEMRE value
    """
    nc = netCDF3.Dataset("/mnt/mesonet/data/iemre/%s_hourly.nc" % (ts.year,),'r')
    p01m = nc.variables['p01m']
    offset = int((ts - (ts + mx.DateTime.RelativeDateTime(month=1,day=1,hour=0))).hours)
    # Find ISUAG Data
    rs = isuag.query("SELECT * from hourly WHERE valid = '%s+00'" % (ts.strftime("%Y-%m-%d"),)).dictresult()
    for i in range(len(rs)):
        stid = rs[i]['station']
        if stid in SKIP:
          continue
        lat = sts[ stid ]['lat']
        lon = sts[ stid ]['lon']
        # Lookup IEMRE data
        ix,jy = constants.find_ij(lon, lat)
        estimate = 0.
        if not numpy.ma.is_masked( p01m[offset,jy,ix] ):
            estimate = p01m[offset,jy,ix] / 25.4
        if estimate > 100:
            estimate = 0
            print "Missing Estimate", ts
        if rs[i]['c900'] > 0 or estimate > 0:
            print "HR %s %-20.20s %5.2f %s %5.2f" % (stid, sts[stid]['name'],
                  rs[i]['c900'], rs[i]['c900_f'], estimate)
        # Fix it
        sql = """UPDATE hourly SET c900 = %.2f, c900_f = 'e' 
              WHERE valid = '%s+00'
              and station = '%s'""" % (estimate, ts.strftime("%Y-%m-%d %H:%M"),
              stid)
        isuag.query(sql)
    nc.close()

if __name__ == "__main__":
    if len(sys.argv) == 4:
        ts = mx.DateTime.DateTime( int(sys.argv[1]),int(sys.argv[2]),
                           int(sys.argv[3]) )
    else:
        ts = mx.DateTime.gmt() + mx.DateTime.RelativeDateTime(days=-1,hour=0,minute=0,second=0)
    for hr in range(24):
        now = ts + mx.DateTime.RelativeDateTime(hours=hr)
        fix_hourly( now.gmtime() )
    fix_daily(ts)
