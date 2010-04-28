#!/bin/csh
#		UDX_overlay.csh
# Script that generates a RADAR image of UDX
# 17 Feb 2003	Use GIF driver

source /mesonet/nawips/Gemenviron


set h_date=`date -u --date "1 hour ago" +%Y%m%d_%H`

set yy=`date -u +%y`
set YY=`date -u +%Y`
set mm=`date -u +%m`
set dd=`date -u +%d`
set date=${yy}${mm}${dd}
set dateY=${YY}${mm}${dd}
set hh=`date -u +%H`

rm OAX_radar.gif* >& /dev/null

set DEVICE1="GIF|UDX_radar.gif|800;600"

setenv DATA_DIR /mesonet/data/nexrad/NIDS/UDX/N0R
set grid=${DATA_DIR}/N0R_${dateY}_${hh}00

if (! -e ${grid} ) then
	set grid=${DATA_DIR}/N0R_${dateY}_${hh}01
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${dateY}_${hh}02
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${dateY}_${hh}03
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${dateY}_${hh}04
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${dateY}_${hh}05
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${dateY}_${hh}06
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${h_date}59
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${h_date}58
endif

if (! -e ${grid} ) then
        set grid=${DATA_DIR}/N0R_${h_date}57
endif

set PROJ=RAD
set TITLE="Mesonet with Rapid City NEXRAD"

# if (! -e ${grid} ) then
#	set grid=
#	set PROJ=LCC
#	set TITLE="Mesonet with NEXRAD missing"
#endif

$GEMEXE/sfmap << EOF > /tmp/UDX_overlay_sfmap.out
#	GAREA	= 40.25;-97;43.75;-90
#	AREA	= 40.25;-97;43.75;-90
	AREA	= rap+
	GAREA	= rap+
	DATTIM  = ${date}/${hh}00
	GLEVEL	= 0
	GVCORD   = NONE
	SFPARM   = skyc:.6;tmpf<120;wsym:1.2:2;alti;;dwpf<120;;;;brbk:1:1:231
	COLORS   = 32;2;32;0;4;32
	SFFILE   = /mesonet/data/gempak/sao/${date}_sao.gem
	LINE     = 4/1/1
	TEXT     = 1/1
	DEVICE   = ${DEVICE1}
	SATFIL   = 
	RADFIL   = ${grid}
	PROJ     = ${PROJ}
	CLEAR    = yes
	PANEL	= 0
	TITLE	= 32/-1/~ ${TITLE}
	SCALE	= 0
	GVECT   =
	WIND    = 
	LATLON	= 0
	HILO     =  
	HLSYM    =  
	CLRBAR   = 0
	CONTUR   = 3/3
	SKIP     = 0
	CINT	= 
	FINT	=  
	FLINE    = 24-12--1 
	LUTFIL   = /mesonet/TABLES/radar.tbl
	STNPLT   =  
	MAP     = 25//1 + 25//2
        \$mapfil =HICNUS.NWS + hipowo.cia
	list
	run

	exit
EOF

gpend

if (-e UDX_radar.gif) then
	#cp UDX_radar.gif ~/current/
	#mv UDX_radar.gif WEB/
 /home/ldm/bin/pqinsert -p "plot c 000000000000 UDX_radar.gif bogus gif" UDX_radar.gif >& /dev/null
endif