import mx.DateTime
import constants

def go(mydb, stationID,updateAll=False):
    """
    Generate the monthly averages, but only do as much as necessary
    """
    if updateAll:
        s = constants.startts(stationID)
    else:
        s = constants._ENDTS - mx.DateTime.RelativeDateTime(years=1)
    e = constants._ENDTS
    interval = mx.DateTime.RelativeDateTime(months=+1)

    now = s
    db = {}
    while (now < e):
        db[now] = {}
        now += interval

    rs = mydb.query("""SELECT year, month, avg(high) as avg_high, 
        avg(low) as avg_low, sum(precip) as rain, 
        sum( CASE WHEN precip >= 0.01 THEN 1 ELSE 0 END ) as rcount, 
        sum( CASE WHEN snow >= 0.01 THEN 1 ELSE 0 END ) as scount from %s 
        WHERE station = '%s' and day >= '%s-01-01' GROUP by year, month""" % (
            constants.get_table(stationID), stationID, s.year ) ).dictresult()

    for i in range(len(rs)):
        ts = mx.DateTime.DateTime( int(rs[i]["year"]), int(rs[i]["month"]), 1)
        sql = """UPDATE r_monthly SET avg_high = %s, avg_low = %s, 
     rain = %s, rain_days = %s, snow_days = %s 
     WHERE station = '%s' and monthdate = '%s' """ % (rs[i]["avg_high"], 
        rs[i]["avg_low"], rs[i]["rain"], rs[i]["rcount"], 
        rs[i]['scount'], stationID, ts.strftime("%Y-%m-%d") ) 
        mydb.query(sql)


def safePrint(val, cols, prec):
  fmt = "%%%s.%sf" % (cols, prec)
  fmt2 = "%%%ss" % (cols,)
  if (val == "M"):
    return fmt2 % val
  return fmt % val

def write(mydb, out, out2, out3, out4, station):
    s = constants.startts(station)
    e = constants._ENDTS
    YRCNT = constants.yrcnt(station)
    YEARS = e.year - s.year + 1
    interval = mx.DateTime.RelativeDateTime(months=+1)

    now = s
    db = {}
    while (now < e):
        db[now] = {"avg_high": "M", "avg_low": "M", "rain": "M"}
        now += interval

    rs = mydb.query("SELECT * from r_monthly WHERE station = '%s'" % (
                    station,) ).dictresult()

    for i in range(len(rs)):
        ts = mx.DateTime.strptime(rs[i]["monthdate"], "%Y-%m-%d")
        if ts < constants._ARCHIVEENDTS:
            db[ts] = rs[i]


    out.write("""# Monthly Average High Temperatures [F]
YEAR   JAN   FEB   MAR   APR   MAY   JUN   JUL   AUG   SEP   OCT   NOV   DEC   ANN
""")

    moTot = {}
    for mo in range(1,13):
        moTot[mo] = 0
    yrCnt = 0
    yrAvg = 0
    for yr in range(constants.startyear(station), constants._ENDYEAR):
        yrCnt += 1
        out.write("%4i" % (yr,) )
        yrSum = 0
        for mo in range(1, 13):
            ts = mx.DateTime.DateTime(yr, mo, 1)
            if (ts < constants._ARCHIVEENDTS):
                moTot[mo] += int(db[ts]["avg_high"])
                yrSum += int(db[ts]["avg_high"])
            out.write( safePrint( db[ts]["avg_high"], 6, 0) )
        if yr != constants._ARCHIVEENDTS.year:
            yrAvg += float(yrSum) / 12.0
            out.write("%6.0f\n" % ( float(yrSum) / 12.0, ) )
        else:
            out.write("      \n")

    out.write("MEAN")
    for mo in range(1,13):
        moAvg = moTot[mo] / float( YRCNT[mo])
        out.write("%6.0f" % (moAvg,) )

    out.write("%6.0f\n" % (yrAvg / (float(YEARS)),) )
  


    out2.write("""# Monthly Average Low Temperatures [F]
YEAR   JAN   FEB   MAR   APR   MAY   JUN   JUL   AUG   SEP   OCT   NOV   DEC   ANN
""")

    moTot = {}
    for mo in range(1,13):
        moTot[mo] = 0
    yrCnt = 0
    yrAvg = 0
    for yr in range(constants.startyear(station), constants._ENDYEAR):
        yrCnt += 1
        out2.write("%4i" % (yr,) )
        yrSum = 0
        for mo in range(1, 13):
            ts = mx.DateTime.DateTime(yr, mo, 1)
            if (ts < constants._ARCHIVEENDTS):
                moTot[mo] += int(db[ts]["avg_low"])
                yrSum += int(db[ts]["avg_low"])
            out2.write( safePrint( db[ts]["avg_low"], 6, 0) )
        if yr != constants._ARCHIVEENDTS.year:
            yrAvg += float(yrSum) / 12.0
            out2.write("%6.0f\n" % ( float(yrSum) / 12.0, ) )
        else:
            out2.write("     M\n")

    out2.write("MEAN")
    for mo in range(1,13):
        moAvg = moTot[mo] / float( YRCNT[mo])
        out2.write("%6.0f" % (moAvg,) )

    out2.write("%6.0f\n" % (yrAvg / float(YEARS),) )
  
    out3.write("""# Monthly Average Temperatures [F] (High + low)/2
YEAR   JAN   FEB   MAR   APR   MAY   JUN   JUL   AUG   SEP   OCT   NOV   DEC   ANN
""")

    moTot = {}
    for mo in range(1,13):
        moTot[mo] = 0
    yrCnt = 0
    yrAvg = 0
    for yr in range(constants.startyear(station), constants._ENDYEAR):
        yrCnt += 1
        out3.write("%4i" % (yr,) )
        yrSum = 0
        for mo in range(1, 13):
            ts = mx.DateTime.DateTime(yr, mo, 1)
            if (ts >= constants._ARCHIVEENDTS):
                out.write("%6s" % ("M",))
                continue
            v = (float(db[ts]["avg_high"]) + float(db[ts]["avg_low"])) / 2.0
            if (ts < constants._ARCHIVEENDTS):
                moTot[mo] += v
                yrSum += v
            out3.write("%6.0f" % ( v, ) )
        if yr != constants._ARCHIVEENDTS.year:
            yrAvg += float(yrSum) / 12.0
            out3.write("%6.0f\n" % ( float(yrSum) / 12.0, ) )
        else:
            out3.write("     M\n")

    out3.write("MEAN")
    for mo in range(1,13):
        moAvg = moTot[mo] / float( YRCNT[mo] )
        out3.write("%6.0f" % (moAvg,) )

    out3.write("%6.0f\n" % (yrAvg / float(yrCnt),) )

    out4.write("""# Monthly Liquid Precip Totals [inches] (snow is melted)
YEAR   JAN   FEB   MAR   APR   MAY   JUN   JUL   AUG   SEP   OCT   NOV   DEC   ANN\n""")

    moTot = {}
    for mo in range(1,13):
        moTot[mo] = 0
    yrCnt = 0
    yrAvg = 0
    for yr in range(constants.startyear(station), constants._ENDYEAR):
        yrCnt += 1
        out4.write("%4i" % (yr,) )
        yrSum = 0
        for mo in range(1, 13):
            ts = mx.DateTime.DateTime(yr, mo, 1)
            if (ts < constants._ARCHIVEENDTS):
                moTot[mo] += db[ts]["rain"]
                yrSum += db[ts]["rain"]
            out4.write( safePrint( db[ts]["rain"], 6, 2) )
        yrAvg += float(yrSum) 
        out4.write("%6.2f\n" % ( float(yrSum), ) )
   
    out4.write("MEAN")
    for mo in range(1,13):
        moAvg = moTot[mo] / float( YRCNT[mo] )
        out4.write("%6.2f" % (moAvg,) )

    out4.write("%6.2f\n" % (yrAvg / float(YEARS -1) ,) )
