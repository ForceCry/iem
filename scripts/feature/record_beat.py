import iemdb, sys

COOP = iemdb.connect('coop', bypass=True)
ccursor = COOP.cursor()

ccursor.execute("""
 select sday, high, low, day, snow from alldata_ia where station = '%s' ORDER by day ASC
""" %( sys.argv[1],))
records = {}
running = 0
for row in ccursor:
    old = records.get(row[0], -99)
    #if running > 0 and row[3] > 0:
    #    print row, lastrow, running
    #if row[2] > old:
    #    print row, old
    if row[1] >= old:
        records[row[0]] = row[1]
        running += 1
    else:
        running = 0
    lastrow = row
    if running > 4:
         print row, running
    # if (row[1] - old) > 14:
    #     print row, old
