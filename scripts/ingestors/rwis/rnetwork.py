import sys
import re
import mx.DateTime
import pg
import os
import csv
import rwis
import access
import network
import mesonet
import iemdb
IEM = iemdb.connect('iem', bypass=True)

st = network.Table("IA_RWIS")

class rnetwork:

    def __init__(self, AT_FILENAME, SF_FILENAME):
        """
        Initialize our parsers and such
        """
        self.obs = {}
        csvfile = open(AT_FILENAME)
        for row in csv.DictReader(csvfile):
            sid = int( row["Rpuid"] )
            self.obs[ sid ] = rwis.RWISOb()
            self.obs[ sid ].add_atdata( row )
            self.obs[ sid ].sname = st.sts[ self.obs[sid].stationID ]['name']
        csvfile.close()

        csvfile = open(SF_FILENAME)
        for row in csv.DictReader(csvfile):
            sid = int( row["Rpuid"] )
            if not self.obs.has_key( sid ):
                self.obs[ sid ] = rwis.RWISOb()
            self.obs[ sid ].add_sfdata( row )
            self.obs[ sid ].sname = st.sts[ self.obs[sid].stationID ]['name']
        csvfile.close()

    def checkOffline(self, network, thres):
        """
        Check how many sites are offline, in case we want to avoid emails
        """
        return False

    def iemtracker(self):
      """
      Check the observations against IEM Tracker to see if we need to squawk
      """
      try:
          import tracker
      except:
          print "Could not connect to Portfolio Database, continuing"
          return  
      dontmail = self.checkOffline('IA_RWIS', 300)
      thres = mx.DateTime.gmt() - mx.DateTime.RelativeDateTime(hours=3)
      track = tracker.Engine()
      for id in self.obs.keys():
          sid = self.obs[id].stationID
          if self.obs[id].gmt_ts > thres:
              track.checkStation(sid, self.obs[id], "IA_RWIS", 
                                   "iarwis", dontmail)
          else: # Observation is old!
              track.doAlert(sid, self.obs[id], "IA_RWIS", 
                              "iarwis", dontmail)
      track.send()


    def genMETAR(self, fp):
        """
        Write METAR information out to a file pointer
        """
        metarTime = mx.DateTime.gmt().strftime("%d%H%M")
        thres = mx.DateTime.gmt() - mx.DateTime.RelativeDateTime(hours=1)
        fp.write("\001\015\015\012001\n")
        fp.write("SAUS43 KDMX "+metarTime+"\015\015\012METAR\015\015\012")
        for id in self.obs.keys():
            sid =  self.obs[id].stationID
            if self.obs[id].gmt_ts < thres:
                continue
            if sid in ["RIOI4","ROSI4","RSMI4",'RMCI4']:
                continue
            self.obs[id].printMETAR(fp) 

        fp.write("\015\015\012\003")

    def genMETAR2(self, fp):
        """
        Write METAR information out to a file pointer
        """
        metarTime = mx.DateTime.gmt().strftime("%d%H%M")
        thres = mx.DateTime.gmt() - mx.DateTime.RelativeDateTime(hours=1)
        fp.write("\001\015\015\012001\n")
        fp.write("SAUS43 KDMX "+metarTime+"\015\015\012METAR\015\015\012")
        for id in self.obs.keys():
            sid =  self.obs[id].stationID
            if self.obs[id].gmt_ts < thres:
                continue
            if sid in ["RIOI4","ROSI4","RSMI4",'RMCI4']:
                continue
            self.obs[id].printMETAR2(fp) 

        fp.write("\015\015\012\003")

    def currentWriteCDFNWS(self,fp):
        """
        Write out obs to a CSV file for the NWS to use
        """
        for id in self.obs.keys():
            self.obs[id].printCDF(fp)

    def updateIEMAccess(self):
        """
        Commit the parsed data to the database, finally!
        """
        icursor = IEM.cursor()

        thres = mx.DateTime.gmt() - mx.DateTime.RelativeDateTime(hours=2)
        for id in self.obs.keys():
            ob = self.obs[id]
            if ob.gmt_ts < thres:
                continue
            if ob.error > 0:
                continue
            iem = access.Ob( ob.stationID, "IA_RWIS")
            iem.setObTimeGMT( ob.gmt_ts )
            iem.data['tmpf'] = ob.tmpf
            iem.data['dwpf'] = ob.dwpf
            iem.data['drct'] = ob.drct
            iem.data['sknt'] = ob.sknt
            iem.data['gust'] = ob.gust
            iem.data['vsby'] = ob.vsby
            iem.data['pday'] = ob.pDay
            iem.data['tsf0'] = ob.sfdata[0]['tmpf']
            iem.data['tsf1'] = ob.sfdata[1]['tmpf']
            iem.data['tsf2'] = ob.sfdata[2]['tmpf']
            iem.data['tsf3'] = ob.sfdata[3]['tmpf']
            iem.data['scond0'] = ob.sfdata[0]['dry']
            iem.data['scond1'] = ob.sfdata[1]['dry']
            iem.data['scond2'] = ob.sfdata[2]['dry']
            iem.data['scond3'] = ob.sfdata[3]['dry']
            iem.data['rwis_subf'] = ob.subT
            iem.updateDatabase( cursor=icursor )
            del(iem)
            
        icursor.close()
        IEM.commit()
