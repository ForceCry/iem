#!/bin/sh

MS_MAPFILE=/var/www/data/wms/us/obs.map
export MS_MAPFILE

/var/www/cgi-bin/mapserv/mapserv
