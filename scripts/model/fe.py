
import sys
sys.path.insert(0, "../lib")
import network
table = network.Table( ['AWOS', 'IA_ASOS'] )

import mx.DateTime
import ingest

sts = mx.DateTime.DateTime(2011,2,27,12,0)
ets = mx.DateTime.DateTime(2011,2,27,18,0)
interval = mx.DateTime.RelativeDateTime(hours=6)

now = sts
while now < ets:
  print now
  for id in table.sts.keys():
    ingest.run("GFS", "K"+id, table.sts[id]['lon'], table.sts[id]['lat'], now)
  for id in table.sts.keys():
    ingest.run("NAM", "K"+id, table.sts[id]['lon'], table.sts[id]['lat'], now)
  now += interval
