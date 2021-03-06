#!/bin/csh

# Assign variables to download the data to
set INCOMING="/mesonet/data/incoming/rwis/"
set ARCHIVE="/mesonet/ARCHIVE/raw/rwis/"
set FTPPASS="`cat /home/mesonet/rwis_ftp_password.txt`"

set LOCAL_FILE="${INCOMING}/rwis.txt"
set LOCAL_FILE2="${INCOMING}/rwis_sf.txt"

set GTS="`date -u +'%Y%m%d%H%M'`"
set TS=`date -u +%d%H%M`
set mm=`date +'%M'`

# Get rwis atmospheric file!
wget --timeout=60 -q -O ${LOCAL_FILE} ftp://rwis:${FTPPASS}@165.206.203.34/ExpApAirData.txt
/home/ldm/bin/pqinsert -p "plot ac $GTS rwis.txt raw/rwis/${GTS}at.txt txt" ${LOCAL_FILE} >& /dev/null

# Get rwis surface file!
wget --timeout=60 -q -O ${LOCAL_FILE2} ftp://rwis:${FTPPASS}@165.206.203.34/ExpSfData.txt
/home/ldm/bin/pqinsert -p "plot ac $GTS rwis_sf.txt raw/rwis/${GTS}sf.txt txt" ${LOCAL_FILE2} >& /dev/null

# AWOS file :)
#wget --timeout=60 -q -O /mesonet/data/incoming/AWOS.DAT ftp://rwis:${FTPPASS}@165.206.203.34/AWOS.DAT
#/home/ldm/bin/pqinsert -p "plot ac $GTS awos.txt raw/awos/${GTS}.txt txt" /mesonet/data/incoming/AWOS.DAT >& /dev/null

# New AWOS File
wget --timeout=60 -q -O /mesonet/data/incoming/iaawos_metar.txt ftp://rwis:${FTPPASS}@165.206.203.34/METAR.txt

# Process AWOS METAR file
python awosMETAR.py

# Actually ingest the data
python rawProcess.py

# Create a GEMPAK surface file...
python genSFFIL.py

# Send Down to LDM
/home/ldm/bin/pqinsert -l /dev/null rwis.csv

# Process The sf file as well.
./run_rwisSF.csh 

cd /mesonet/data/metar

mv rwis.sao IArwis${TS}.sao
mv rwis2.sao IA.rwis${TS}.sao
/home/ldm/bin/pqinsert IArwis${TS}.sao >& /dev/null
#if (`echo ${mm} | cut -c 2` == 6) then
/home/ldm/bin/pqinsert IA.rwis${TS}.sao >& /dev/null
#endif
rm IArwis${TS}.sao IA.rwis${TS}.sao

# Do mini and portable stuff
cd /mesonet/data/incoming/rwis
wget -nd -m -q "ftp://rwis:${FTPPASS}@165.206.203.34/*.csv"
/home/ldm/bin/pqinsert -p "plot ac $GTS rwis_traffic.txt raw/rwis/${GTS}traffic.txt txt" TrafficFile.csv >& /dev/null
/home/ldm/bin/pqinsert -p "plot ac $GTS rwis_probe.txt raw/rwis/${GTS}probe.txt txt" DeepTempProbeFile.csv >& /dev/null
cd /mesonet/www/apps/iemwebsite/scripts/ingestors/rwis
python mini_portable.py
python process_traffic.py
python process_soil.py
