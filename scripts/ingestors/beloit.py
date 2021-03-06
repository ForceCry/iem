"""
 Ingest Beloit Data
"""

import mx.DateTime
import mesonet
import access
import iemdb
IEM = iemdb.connect('iem')
icursor = IEM.cursor()

dyfile = open('/mnt/home/mesonet/ot/ot0005/incoming/Beloit/BeloitDaily.dat', 
              'r').readlines()
lastline = dyfile[-1]
tokens = lastline.split(",")
year = int(tokens[1])
doy = int(tokens[2])
ts = mx.DateTime.DateTime(year,1,1) + mx.DateTime.RelativeDateTime(days=(doy-1))
high = mesonet.c2f( float(tokens[3]) )
low = mesonet.c2f( float(tokens[4]) )
pday = float(tokens[5]) / 25.4
icursor.execute("""UPDATE summary_%s s SET max_tmpf = %s, min_tmpf = %s, 
    pday = %s FROM stations t WHERE t.id = 'OT0009' and 
    t.iemid = s.iemid and day = '%s'""" % (ts.year, high, low, pday, 
                                           ts.strftime("%Y-%m-%d")))

hrfile = open('/mnt/home/mesonet/ot/ot0005/incoming/Beloit/BeloitHourly.dat',
              'r').readlines()

lastline = hrfile[-1]
tokens = lastline.split(",")
year = int(tokens[1])
doy = int(tokens[2])
hour = int(tokens[3]) / 100
ts = mx.DateTime.DateTime(year,1,1) + mx.DateTime.RelativeDateTime(days=(doy-1),hour=hour)

tmpf = mesonet.c2f( float(tokens[5]) )
relh = float(tokens[6])
if relh > 100: relh = 100
if relh < 0: relh = 0
srad = float(tokens[7])
if srad < 0: srad = 0
sknt = float(tokens[8]) * 2.0
drct = tokens[9]
phour = float(tokens[10]) / 25.4
c1tmpf = mesonet.c2f( float(tokens[11]) )
mslp = tokens[12]
reftemp = tokens[13]
voltage = tokens[14]

ts = ts + mx.DateTime.RelativeDateTime(hours=6)

iemob = access.Ob("OT0009", "OT")
iemob.setObTimeGMT(ts)
iemob.data['tmpf'] = tmpf
iemob.data['dwpf'] = mesonet.dwpf(tmpf, relh)
iemob.data['relh'] = relh
iemob.data['sknt'] = sknt
iemob.data['drct'] = float(drct)
iemob.data['phour'] = phour
iemob.data['mslp'] = mslp
iemob.data['c1tmpf'] = c1tmpf
iemob.data['srad'] = srad
iemob.updateDatabase(cursor=icursor)

icursor.close()
IEM.commit()

