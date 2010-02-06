# Something to parse the mess we get from NCDC each month
# Better than nothing, though....

import re
import mx.DateTime
import os

DBHOST = "iemdb"
if os.environ["USER"] == "akrherz":
  DBHOST = "localhost"

P1_RE = re.compile(r"""
(?P<wban>[0-9]{5})
(?P<faaid>[0-9A-Z]{4})\s
(?P<id3>[0-9A-Z]{3})
(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})
(?P<hr>[0-9]{2})(?P<mi>[0-9]{2})
(?P<gmt_hr>[0-9]{2})(?P<gmt_mi>[0-9]{2})\s+
((?P<vis1_coef>\d+\.\d*)|(?P<vis1_coef_miss>M))\s+(?P<vis1_nd>[NMD ])\s+
((?P<vis2_coef>\d+\.\d*)|(?P<vis2_coef_miss>[M ]))\s+(?P<vis2_nd>[NMD ])\s+
...............\s+
((?P<drct>\d+)|(?P<drct_miss>M))\s+
((?P<sknt>\d+)|(?P<sknt_miss>M))\s+
((?P<gust_drct>\d+)|(?P<gust_drct_miss>M))\s+
((?P<gust_sknt>\d+)|(?P<gust_sknt_miss>M))\s+
(....)\s
(...)
""", re.VERBOSE)

p1_examples = [
"14943KSUX SUX2010010100000600   0.104 N                             318     2   318    3      M                 ",
"14943KSUX SUX2010013123590559   0.115 N                              96     8   102   10      M                 ",
"94989KAMW AMW2010010106261226   0.087 N                             318     9   321   11                        ",
"14933KDSM DSM2010010101380738   0.098 N                             306     9   312    9    31 60+              ",
"94989KAMW AMW2010012112281828    M    M                              80     6    72    9                        ",
"94989KAMW AMW2010012112271827  70000.00                                80     6    82    8                      ",
]

p1_answers = [
 {'year': 2010, 'month': 1, 'day': 1 }
]

P2_RE = re.compile(r"""
(?P<wban>[0-9]{5})
(?P<faaid>[0-9A-Z]{4})\s
(?P<id3>[0-9A-Z]{3})
(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<day>[0-9]{2})
(?P<hr>[0-9]{2})(?P<mi>[0-9]{2})
(?P<gmt_hr>[0-9]{2})(?P<gmt_mi>[0-9]{2})\s\s
(?P<ptype>[A-Z0-9\?\-\+]{1,2})\s+
\[?((?P<unk>\d+)|\s+(?P<unk_miss>M))\s+\]?\s+
(?P<precip>\d+\.\d*)............\s+
(?P<unk2>\d*)\s+
((?P<pres1>\d+\.\d*)|(?P<pres1_miss>[M ]))\s+
((?P<pres2>\d+\.\d*)|(?P<pres2_miss>[M ]))\s+
((?P<pres3>\d+\.\d*)|(?P<pres3_miss>[M ]))\s+
((?P<tmpf>\-?\d+)|(?P<tmpf_miss>M))\s+
((?P<dwpf>\-?\d+)|(?P<dwpf_miss>M))\s+
""", re.VERBOSE)


p2_examples = [
"14943KSUX SUX2010010100000600  NP  0000     0.00             39981   29.200  29.200  29.205    -2   -7          ",
"14933KDSM DSM2010010101380738  NP [0000  ]  0.00             39991   29.336  29.331  29.330     3   -5          ",
"94982KDVN DVN2010010101350735  NP  0000     0.00             39942   29.508  29.500            -1   -6          ",
"14943KSUX SUX2010013123050505  NP    M      0.00             39988   29.013  29.012  29.018    13    6          ",
"14943KSUX SUX2010013109471547  ?0 [  M   ]  0.00             39988   29.087  29.086  29.092    16   10          ",
"94989KAMW AMW2010010613201920  S   0000     0.01             40002   29.197  29.191             9    5          ",
]

def p2_parser( ln ):
    """
    Handle the parsing of a line found in the 6506 report, return QC dict
    """
    m = P2_RE.match( ln )
    if m is None:
        print "P2_FAIL:|%s|" % (ln,)
        return None
    d = m.groupdict()

    ret = {}
    # localtime, CST
    ret['ts'] = mx.DateTime.DateTime( int(d['year']), int(d['month']), 
                int(d['day']), int(d['hr']), int(d['mi']) )
    for k in d.keys():
        ret[k] = d[k]
    """
    for v in ['tmpf', 'dwpf']:
        if d['%s_miss' % (v,)]:
            ret[v] = "Null"
        else:
            ret[v] = int( d[v] )

    for v in ['pres1', 'pres2', 'pres3', 'precip']:
        if d['%s_miss' % (v,)]:
            ret[v] = "Null"
        else:
            ret[v] = float( d[v] )
    """
    return ret

def p1_parser( ln ):
    """
    Handle the parsing of a line found in the 6505 report, return QC dict
    """
    m = P1_RE.match( ln )
    if m is None:
        print "P1_FAIL:|%s|" % (ln,)
        return None
    d = m.groupdict()

    ret = {}
    # localtime, CST
    ret['ts'] = mx.DateTime.DateTime( int(d['year']), int(d['month']), 
                int(d['day']), int(d['hr']), int(d['mi']) )
    for k in d.keys():
        ret[k] = d[k]
    """
    if d['vis1_coef_miss']:
        ret['vis1_coef'] = "Null"
    else:
        ret['vis1_coef'] = float( d['vis1_coef'] )

    ret['vis1_nd'] = d['vis1_nd']

    if d['vis2_coef_miss']:
        ret['vis2_coef'] = "Null"
    else:
        ret['vis2_coef'] = float( d['vis2_coef'] )

    ret['vis2_nd'] = d['vis2_nd']

    for v in ['sknt', 'drct', 'gust_drct', 'gust_sknt']:
        if d['%s_miss' % (v,)]:
            ret[v] = "Null"
        else:
            ret[v] = int( d[v] )
    """
    return ret


def test():
    for ex in p1_examples:
      m = p1_parser( ex )

    for ex in p2_examples:
      m = p2_parser( ex )

def runner(station, monthts):
    """
    Parse a month's worth of data please
    """

    # Our final amount of data
    data = {}

    # We have two files to worry about
    page1 = open('data/%s/64050K%s%s%02i.dat' % (station,
            station, monthts.year, monthts.month), 'r')
    page2 = open('data/%s/64060K%s%s%02i.dat' % (station,
            station, monthts.year, monthts.month), 'r')

    for ln in page1:
      d = p1_parser( ln )
      data[ d['ts'] ] = d
    for ln in page2:
      d = p2_parser( ln )
      if d is None:
        continue
      if not data.has_key( d['ts'] ):
        data[ d['ts'] ] = {}
      for k in d.keys():
        data[ d['ts'] ][ k ] = d[k]

    out = open('dbinsert.sql', 'w')
    out.write("""DELETE from t%s_1minute WHERE station = '%s' and 
               valid BETWEEN '%s 00:00-0600' and '%s 00:00-0600';\n""" % (
         monthts.year, station, monthts.strftime("%Y-%m-%d"),
(monthts + mx.DateTime.RelativeDateTime(months=1)).strftime("%Y-%m-%d") ))
    out.write("COPY t%s_1minute FROM stdin WITH NULL as 'Null';\n" % (
         monthts.year,))

    # Loop over the data we got please
    for ts in data.keys():
        ln = ""
        data[ts]['station'] = station
        data[ts]['valid'] = ts.strftime("%Y-%m-%d %H:%M:00-0600")
        for col in ('station', 'valid', 'vis1_coeff', 'vis1_nd', 
            'vis2_coeff', 'vis2_nd', 'drct', 'sknt','gust_drct', 
            'gust_sknt', 'ptype', 'precip', 'pres1', 'pres2', 'pres3', 
            'tmpf','dwpf'):
            ln += "%s\t" % (data[ts].get(col) or 'Null',)
        out.write(ln[:-1]+"\n")
    out.write("\.\n")
    out.close()

    os.system("psql -f dbinsert.sql -h %s asos" % (DBHOST,))
    print "Station: %s processed %s entries" % (station, len(data.keys()))
 

runner("AMW", mx.DateTime.DateTime(2010,1,1))
#test()
"""
           Table "public.t2010_1minute"
   Column   |           Type           | Modifiers 
------------+--------------------------+-----------
 station    | character(3)             | 
 valid      | timestamp with time zone | 
 vis1_coeff | real                     | 
 vis1_nd    | character(1)             | 
 vis2_coeff | real                     | 
 vis2_nd    | character(1)             | 
 drct       | smallint                 | 
 sknt       | smallint                 | 
 gust_drct  | smallint                 | 
 gust_sknt  | smallint                 | 
 ptype      | character(2)             | 
 precip     | real                     | 
 pres1      | real                     | 
 pres2      | real                     | 
 pres3      | real                     | 
 tmpf       | smallint                 | 
 dwpf       | smallint                 | 
"""
