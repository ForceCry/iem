
# http://www.clarus-system.com/SubShowObs.jsp?subId=2008112400&file=20081125_0200.csv

import access
import mesonet
import iemdb
IEM = iemdb.connect('iem', bypass=True)
icursor = IEM.cursor()
import mx.DateTime
import urllib2
import csv
import sys

# Figure out necessary timestamp for URI call
m = mx.DateTime.now().minute / 20
gmt = mx.DateTime.gmt() + mx.DateTime.RelativeDateTime(minute=(20*m))
#url = "http://www.clarus-system.com/SubShowObs.jsp?subId=2008112400&file=%s.csv" % (gmt.strftime("%Y%m%d_%H%M"),)
url = "http://www.clarus-system.com/SubShowObs.jsp?subId=2011111100&file=%s.csv" % (
                                        gmt.strftime("%Y%m%d_%H%M"),)
#print url
req = urllib2.Request(url)
#try:
data = urllib2.urlopen(req)
#except:
#  sys.exit(0)

# Process the dataset into dicts
obs = {}
r = csv.DictReader( data )
for row in r:
  if not row.has_key('ClarusSiteID'):
    sys.exit()
  if (row['ClarusSiteID'] == None):
    continue
  sid = "CL%s" % (row['ClarusSiteID'],)
  if (not obs.has_key(sid)):
    if (row['ClarusContribID'] == "18"):
      obs[sid] = access.Ob(sid, 'IN_RWIS')
    if (row['ClarusContribID'] == "17"):
      obs[sid] = access.Ob(sid, 'IL_RWIS')
    if (row['ClarusContribID'] == "44"):
      obs[sid] = access.Ob(sid, 'SD_RWIS')
    try:
      ts = mx.DateTime.strptime(row['Timestamp'][:16], '%Y-%m-%d %H:%M')
    except:
      continue
    obs[sid].setObTimeGMT( ts )
  if (row['ObsTypeName'] == 'essDewpointTemp'):
    obs[sid].data['dwpf'] = mesonet.c2f( float(row['Observation']) )
  elif (row['ObsTypeName'] == 'essAirTemperature'):
    obs[sid].data['tmpf'] = mesonet.c2f( float(row['Observation']) )
  elif (row['ObsTypeName'] == 'essVisibility'):
    obs[sid].data['vsby'] = float(row['Observation']) / 1609.344
  elif (row['ObsTypeName'] == 'windSensorAvgSpeed'):
    obs[sid].data['sknt'] = float(row['Observation']) * 2.0
  elif (row['ObsTypeName'] == 'windSensorAvgDirection'):
    obs[sid].data['drct'] = float(row['Observation'])
  elif (row['ObsTypeName'] == 'windSensorGustSpeed'):
    obs[sid].data['gust'] = float(row['Observation']) * 2.0
  elif (row['ObsTypeName'] == 'windSensorGustDirection'):
    obs[sid].data['max_sknt_drct'] = float(row['Observation']) 
  elif (row['ObsTypeName'] == 'essSurfaceTemperature'):
    obs[sid].data['tsf%s' % (row['ClarusSensorIndex'],)] = mesonet.c2f( float(row['Observation']) )

for id in obs.keys():
  obs[id].updateDatabase(cursor=icursor)
  
IEM.commit()
