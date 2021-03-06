# Download AWOS METAR data directly, yummmm

import urllib2
import mx.DateTime

from metar import Metar

import access
from pyIEM import iemdb
i = iemdb.iemdb()
iemaccess = i['iem']

sites = ['KBNW',]

def dosite(id):
    """
    Process data for a given site
    """
    req = urllib2.Request("http://my.iwapi.com:8080/WXWeb/METAR?icao=%s" % (id,))
    try:
        data = urllib2.urlopen(req, timeout=15).read()
    except:
        if mx.DateTime.now().minute == 0:
            print 'IWAPI AWOS Download Fail for:', id
        return
        
    mtr = Metar.Metar(data)
    if mtr.time is None:
        return
    iemid = mtr.station_id[-3:]
    gts = mx.DateTime.DateTime( mtr.time.year, mtr.time.month,
                  mtr.time.day, mtr.time.hour, mtr.time.minute)
    iem = access.Ob(iemid, 'AWOS')
    iem.setObTimeGMT(gts)
    iem.load_and_compare(iemaccess)
    
    iem.data['raw'] = data
    if mtr.temp is not None:
        iem.data['tmpf'] = mtr.temp.value("F")
    if mtr.dewpt is not None:
        iem.data['dwpf'] = mtr.dewpt.value("F")
    if mtr.wind_speed is not None:
        iem.data['sknt'] = mtr.wind_speed.value("KT")
    if mtr.wind_gust is not None:
        iem.data['gust'] = mtr.wind_gust.value("KT")
    if mtr.wind_dir is not None:
        iem.data['drct'] = mtr.wind_dir.value()
    if mtr.vis is not None:
        iem.data['vsby'] = mtr.vis.value("SM")
    if mtr.press is not None:
        iem.data['alti'] = mtr.press.value("IN")
    iem.data['phour'] = 0
    if mtr.precip_1hr is not None:
        iem.data['phour'] = mtr.precip_1hr.value("IN")
    # Do something with sky coverage
    for i in range(len(mtr.sky)):
        (c,h,b) = mtr.sky[i]
        iem.data['skyc%s' % (i+1)] = c
        if h is not None:
            iem.data['skyl%s' % (i+1)] = h.value("FT")


    iem.updateDatabase(iemaccess)

for site in sites:
    dosite(site)
