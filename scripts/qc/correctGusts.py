# 11 Feb 2005	Fix update of summary table

import mx.DateTime
import iemdb
IEM = iemdb.connect('iem')
icursor = IEM.cursor()

today = mx.DateTime.now()
sql = """update summary_%s s SET max_gust = 0 
    FROM stations t WHERE t.iemid = s.iemid and day = 'TODAY' and max_gust_ts < '%s 00:05' and
    t.network in ('KCCI','KIMT','KELO')""" % (
    today.year, today.strftime("%Y-%m-%d"),)
icursor.execute(sql)
icursor.close()
IEM.close()
