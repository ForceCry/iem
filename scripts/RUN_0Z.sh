# Jobs run at 00 UTC
cd 00z
python awos_rtp.py

cd ../ingestors
python elnino.py

cd ../summary
python max_reflect.py

# Rerun today
cd ../dbutil
python rwis2archive.py 1
python snet2archive.py

cd ../iemre
python stage4_12z_adjust.py

cd ../cscap
# at 0z, -6 days is available, hopefully!
python download_narr.py $(date -u --date '6 days ago' +'%Y %m %d')
cd ../coop
python narr_solarrad.py $(date -u --date '7 days ago' +'%Y %m %d')