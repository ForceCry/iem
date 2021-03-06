import iemdb
import mx.DateTime
import numpy
ASOS = iemdb.connect('asos', bypass=True)
acursor = ASOS.cursor()
#acursor.execute("SET TIME ZONE 'CDT6CST'")
stemps = []
sdrct = []
ssknt = []
sdwpf = []
pres1 = []
sgust = []
sprec = numpy.zeros( (3000,), 'f')

acursor.execute("""
 SELECT extract(epoch from (valid at time zone 'CDT')), tmpf, dwpf, drct, 
  sknt, pres1, gust_sknt, precip,
  valid at time zone 'CDT' from t2012_1minute WHERE station = 'LWD'
 and valid BETWEEN '2012-08-25 00:00-05' and '2012-08-26 23:59-05' 
 ORDER by valid ASC
""")
tot = 0
for row in acursor:
        #sgust.append( row[6] * 1.15)
        offset = row[8].hour * 60 + row[8].minute
        if row[8].day == 26:
            offset += 1440
        if row[7] > 0:
          print offset, row[8], row[7]
          tot += row[7]
        sprec[offset] = float(row[7] or 0) 
        
print tot

acc = numpy.zeros( (3000,), 'f')
rate15 = numpy.zeros( (3000,), 'f')
rate60 = numpy.zeros( (3000,), 'f')
svalid = [0]*3000
for i in range(3000):
    acc[i] = acc[i-1] + sprec[i]
    rate15[i] = numpy.sum(sprec[i-14:i+1]) * 4
    rate60[i] = numpy.sum(sprec[i-59:i+1])
    svalid[i] =  mx.DateTime.DateTime(2012,8,25, 0) + mx.DateTime.RelativeDateTime(minutes=i)

print acc[818:843]
#print rate60[818:912]
#for i in range(818,912):
#    print "%s,%.0f,%s" % (i, svalid[i], svalid[i])
#    print mx.DateTime.DateTime(2012,8,4, 0) + mx.DateTime.RelativeDateTime(minutes=i)

# Figure out ticks
sts = mx.DateTime.DateTime(2012,8,25, 13, 30)
ets = mx.DateTime.DateTime(2012,8,26, 14, 30)
interval = mx.DateTime.RelativeDateTime(minutes=240)
now = sts
xticks = []
xlabels = []
xlabels2 = []
while now <= ets:
    fmt = "%-I:%M %p"
    #if now == sts or now.hour == 0:
    #    fmt = "%-I %p\n%-d %B"
    
    #if now == sts or (now.minute == 0 and now.hour % 1 == 0 ):
    xticks.append( int(now) )
    xlabels.append( now.strftime(fmt))
    xlabels2.append( now.strftime(fmt))
    now += interval

import matplotlib.pyplot as plt
import matplotlib.font_manager 
prop = matplotlib.font_manager.FontProperties(size=12) 

fig = plt.figure()


ax = fig.add_subplot(111)
print numpy.shape(svalid)
print numpy.shape(acc)
print numpy.max(rate60)
ax.plot(svalid, acc, color='b', label="Accumulation")
ax.plot(svalid, sprec * 60, color='black', label="Hourly Rate over 1min")
ax.plot(svalid, rate15, color='g', label="Hourly Rate over 15min", linewidth=2)
#ax.plot(svalid, rate60, color='r', label="Actual Hourly Rate")
ax.set_xticks(xticks)
ax.set_ylabel("Precipitation [inch or inch/hour]")
ax.set_xticklabels(xlabels2)
ax.grid(True)
ax.set_xlim(min(xticks), max(xticks))
ax.legend(loc=2, prop=prop, ncol=2)
ax.set_ylim(0,12)
ax.set_xlabel("25-26 August 2012 (CDT)")
ax.set_title("25-26 August 2012 Lamoni, IA (KLWD) One Minute Rainfall\n8.07 inches total")
#ax.set_ylim(0,361)
#ax.set_yticks((0,90,180,270,360))
#ax.set_yticklabels(('North','East','South','West','North'))

"""
fig = plt.figure(figsize=(7.0,9.3))
ax = fig.add_subplot(311)
ax.set_title("Binghamton,NY (KBGM) ASOS [7 Sep 2011]")
ax.scatter(svalid, sdrct, color='b')
ax.set_xticks(xticks)
ax.set_ylabel("Wind Direction")
ax.set_xticklabels(xlabels2)
ax.grid(True)
ax.set_xlim(min(xticks), max(xticks))
ax.set_ylim(0,361)
ax.set_yticks((0,90,180,270,360))
ax.set_yticklabels(('North','East','South','West','North'))


ax = fig.add_subplot(312)
ax.plot(svalid, ssknt, color='b', label="Speed")
ax.plot(svalid, sgust, color='r', label="Gust")
ax.set_xticks(xticks)
ax.set_ylabel("5 Second Wind Speed [mph]")
ax.set_xticklabels(xlabels2)
ax.grid(True)
ax.set_xlim(min(xticks), max(xticks))
ax.set_ylim(0,80)
ax.legend(loc=3,ncol=2)
#ax.set_ylim(0,361)
#ax.set_yticks((0,90,180,270,360))
#ax.set_yticklabels(('North','East','South','West','North'))


ax2 = fig.add_subplot(413)
#ax2.scatter(valid, temps)
ax2.plot(svalid, stemps, color='r', label="Temperature")
ax2.plot(svalid, sdwpf, color='b', label="Dew Point")
ax2.set_xticks(xticks)
ax2.set_xticklabels(xlabels2)
ax2.grid(True)
ax2.legend(loc=4, prop=prop)
ax2.set_xlim(min(xticks), max(xticks))
ax2.set_ylim(30,100)
ax2.set_ylabel("Temperature $^{\circ}\mathrm{F}$")
#ax2.set_xlabel("CDT")


ax3 = fig.add_subplot(313)
#ax2.scatter(valid, temps)
ax3.plot(svalid, pres1, color='r')
#ax3.plot(svalid, sdwpf, color='b', label="Dew Point")
ax3.set_xticks(xticks)
ax3.set_xticklabels(xlabels)
ax3.grid(True)
ax3.set_xlim(min(xticks), max(xticks))
ax3.set_ylabel("Pressure [inches]")
ax3.set_xlabel("EDT")
"""
fig.savefig('test.ps')
import iemplot
iemplot.makefeature('test')
