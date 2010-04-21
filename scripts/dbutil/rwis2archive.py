
from pyIEM import iemdb
import mx.DateTime, sys, traceback
i = iemdb.iemdb()
rwis = i['rwis']
iemdb = i['iem']

# Hack it for today, just fuss with iowa
if (len(sys.argv) > 1):
  ts = mx.DateTime.now()
else:
  ts = mx.DateTime.now() - mx.DateTime.RelativeDateTime(days=1)

# Delete any obs from yesterday
sql = "DELETE from t%s WHERE date(valid) = '%s'" % (ts.year, 
       ts.strftime("%Y-%m-%d") )
rwis.query(sql)

# Get obs from Access
sql = """SELECT * from current_log WHERE date(valid) = '%s' 
      and network = 'IA_RWIS'""" % (
      ts.strftime("%Y-%m-%d"), )
rs = iemdb.query(sql).dictresult()

for i in range(len(rs)):
  sql = """INSERT into t%s (station, valid, tmpf, dwpf, drct, sknt, tfs0,
    tfs1, tfs2, tfs3, subf, gust, tfs0_text, tfs1_text, tfs2_text, tfs3_text,
    pcpn, vsby)
    values('%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s','%s','%s','%s',%s,%s
    )""" % (
   ts.year,rs[i]['station'], rs[i]['valid'], (rs[i]['tmpf']), 
  (rs[i]['dwpf']), (rs[i]['drct']), (rs[i]['sknt']),
   rs[i]['tsf0'],
   rs[i]['tsf1'],
   rs[i]['tsf2'],
   rs[i]['tsf3'],
   rs[i]['rwis_subf'],
   rs[i]['gust'],
  (rs[i]['scond0'] or "Null"), 
  (rs[i]['scond1'] or "Null"), 
  (rs[i]['scond2'] or "Null"), 
  (rs[i]['scond3'] or "Null"), 
   rs[i]['pday'],
   rs[i]['vsby']
   )
  try:
    rwis.query(sql)
  except:
    print sql
    traceback.print_exc(file=sys.stdout)
