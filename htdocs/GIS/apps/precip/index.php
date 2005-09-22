<?php 
        $page = "gis";
        $TITLE = "IEM | Precipitation Analysis";
include("/mesonet/php/include/header.php"); 
?>
<b>Nav:</b> <a href="/GIS/">GIS</a> > IEM Precip Analysis

<p>
<h3 class="heading">IEM Precip Analysis</h3></dib>
<div class="text">
<br>
<table border=0 cellpadding=2 cellspacing=0>
<tr>
  <td colspan=2>
<p>This web-based GIS application allows the dynamic overlay of
<b>current</b> precipitation products for Iowa. Observations from automated 
stations can be overlayed with NEXRAD WSR-88D estimations. 

  </td>
</tr>
<tr bgcolor="#EEEEEE">
  <td align="center">
<div align="center"><b>No Java</b></div><br>
<form method=GET action="/cgi-bin/mapserv/mapserv">
<input type="hidden" name="map" value="/home/httpd/html/GIS/apps/precip/precip_nj.map">
<input type="hidden" name="layer" value="rtntp">
<input type="submit" value="Initialize">
</form>
  </td>
</tr>

<tr>
 <td colspan="2">
<h3 class="subtitle">Data Sources:</h3>
<p>Currently, automated precipitation observations from the
ASOS, AWOS and SchoolNet Networks are included in the application.  NEXRAD 
estimations are generated by combining and gridding the 7 NEXRAD sites with
Iowa coverage onto a 2km grid.  The grids are updated every 15 minutes.
Currently, I do not have an automated way to import the timestamps into
the mapserver application.  Hopefully, I can figure something out in the
future.

<br><br>The observations are updated a little after the top of the hour. 
For example, if you were looking at the image at :31 after, the 1 hour 
observed total would be valid for the previous hour.  Updates usually occur
at about :07 after.

<p><h3 class="subtitle">Notes:</h3>
<p class="story">The NEXRAD Storm Total (STP) grid is somewhat problematic, 
since individual sites will reset the STP values at different times.  For a wide
spread rainfall event, the STP grid <i>should</i> be okay.  As with any 
dataset, discretion should be used.

<br><br>The projection of the NEXRAD image onto the mapserver application is
not completely true.  Care was taken to line up geographic locations, but 
spatial errors exist toward the edge of the image.  These errors should not 
exceed 0.5 km, which is well within the uncertainty of NEXRAD grid itself.

 </td>
</tr>

</table></div>



<?php include("/mesonet/php/include/footer.php"); ?>

