
import mx.DateTime, re, pg
mydb = pg.connect("squaw", "iemdb")

data = open("/tmp/squaw.txt", 'r').read()

tokens = re.findall("USGS\t([0-9]*)\t(....-..-.. ..:..)\t([CSDT]+)\t([0-9]*)", data)

for ob in tokens:
	sql = "SELECT * from real_flow WHERE valid = '%s'" % (ob[1],)
	rs = mydb.query(sql).dictresult()
	if len(rs) > 0:
		continue
	if ob[3] != '':
		sql = "INSERT into real_flow(gauge_id, valid, cfs) VALUES (%s, '%s', %s)" \
			% (ob[0], ob[1], ob[3])
		mydb.query(sql)
