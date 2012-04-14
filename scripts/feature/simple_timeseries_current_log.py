import iemdb, datetime, iemtz
IEM = iemdb.connect('iem', bypass=True)
icursor = IEM.cursor()
ASOS = iemdb.connect('asos', bypass=True)
acursor = ASOS.cursor()

sts = datetime.datetime(2012,4,10,0, tzinfo=iemtz.Central)
ets = datetime.datetime(2012,4,10,12,1, tzinfo=iemtz.Central)
dt = datetime.timedelta(hours=2)
now = sts
xticks = []
xticklabels = []
while now < ets:
  xticks.append( now )
  xticklabels.append( now.strftime("%-I %p") )
  now += dt

def get2(station):
  times = []
  vals = []
  acursor.execute("""
  SELECT valid, tmpf from t2012_1minute WHERE 
  station = '%s' and valid >= '2012-04-10 00:00' and 
  valid < '2012-04-10 12:00' ORDER by valid ASC
  """ % (station,))
  for row in acursor:
    times.append( row[0])
    vals.append( row[1] )
  return times, vals


def get(station, network):
  times = []
  vals = []
  icursor.execute("""
  SELECT valid, tmpf from current_log c JOIN stations s on (s.iemid = c.iemid)
  and s.network = '%s' and s.id = '%s' and valid >= '2012-04-10 00:00' and 
  valid < '2012-04-10 12:00' ORDER by valid ASC
  """ % (network, station))
  for row in icursor:
    times.append( row[0])
    vals.append( row[1] )
  return times, vals

import iemplot
import matplotlib.pyplot as plt
import matplotlib.font_manager
prop = matplotlib.font_manager.FontProperties(size=12)


fig = plt.figure()
ax = fig.add_subplot(111)

times, vals = get2("AMW")
ax.plot(times, vals, label="Ames Airport (1min) %.0f" % (min(vals),))

times, vals = get("AMW", "IA_ASOS")
ax.plot(times, vals, label="Ames Airport %.0f" % (min(vals),))

times, vals = get("RAMI4", "IA_RWIS")
ax.plot(times, vals, label="Ames RWIS %.0f" % (min(vals),))

times, vals = get("OT0002", "OT")
ax.plot(times, vals, label="ISU Agronomy Hall %.0f" % (min(vals),))
times, vals = get("OT0009", "OT")
ax.plot(times, vals, label="Beliot Center %.0f" % (min(vals),))
times, vals = get("SAMI4", "KCCI")
ax.plot(times, vals, label="St Cecilia SchoolNet %.0f" % (min(vals),))

ax.plot([xticks[2],xticks[4]], [28,28], label="Ames NWS COOP 28")
ax.set_xticks( xticks )
ax.set_xticklabels( xticklabels )
ax.grid(True)
ax.legend(loc=2, ncol=2, prop=prop)
ax.set_title("10 April 2012 Ames Area Temperature Timeseries")
ax.set_ylabel("Air Temperature $^{\circ}\mathrm{F}$")

fig.savefig('test.ps')
iemplot.makefeature('test')