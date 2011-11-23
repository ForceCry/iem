<?php
 include("../../config/settings.inc.php");
 define("IEM_APPID", 40);
 $sortcol = isset($_GET["sortcol"]) ? $_GET["sortcol"] : "peak";
 $metar = isset($_GET["metar"]) ? $_GET['metar'] : "no";
 $sorder = isset($_GET["sorder"]) ? $_GET["sorder"] : "desc";
 $wfo = isset($_REQUEST["wfo"]) ? $_REQUEST["wfo"] : 'DMX';

 $REFRESH = "<meta http-equiv=\"refresh\" content=\"60;\">";
 $TITLE = "IEM | Obs by NWS Forecast Office";

  $THISPAGE = "current-sort";
  include("$rootpath/include/header.php"); 
  include("$rootpath/include/mlib.php"); 
  include("$rootpath/include/wfoLocs.php");
  include("$rootpath/include/forms.php");
  include("$rootpath/include/station.php");
  include("$rootpath/include/iemaccess.php");
  include("$rootpath/include/iemaccessob.php");

$iem = new IEMAccess();
$asos = $iem->getWFO($wfo);


$vals = Array("tmpf" => "Air Temperature [F]", "dwpf" => "Dew Point Temp [F]",
  "sknt" => "Wind Speed [knots]", "drct" => "Wind Direction [deg]",
  "alti" => "Altimeter [mb]", "peak" => "Today's Wind Gust [knots]",
  "peak_ts" => "Time of Peak Gust", "relh" => "Relative Humidity",
  "feel" => "Feels Like [F]", "vsby" => "Visibility [miles]",
  "ts" => "Observation Time", "phour" => "Last Hour Rainfall [inch]",
  "min_tmpf" => "Today's Low Temperature",
  "max_tmpf" => "Today's High Temperature",
  "pday" => "Today Rainfall [inch]");

?>

<?php $current_network = "By NWS WFO"; include("$rootpath/include/current_bar.inc.php"); ?>

<p>
<form method="GET" action="obs.php" name="work">
<input type="hidden" value="<?php echo $sortcol; ?>" name="sortcol">
<table border=1 cellspacing=0 cellpadding=1>
<tr>
 <th>Select WFO: <?php echo wfoSelect($wfo); ?></td>
  <th>View Options:</th>
  <td>Include METARS:
  <input value="no" type="radio" name="metar" <?php if ($metar == "no") echo  "CHECKED"; ?>> No
  <input value="yes" type="radio" name="metar" <?php if ($metar == "yes") echo
"CHECKED"; ?>> Yes
</td>
<td>Sort Order:
<select name="sorder">
  <option value="asc" <?php if ($sorder == "asc") echo "SELECTED"; ?>>Ascending
  <option value="desc" <?php if ($sorder == "desc") echo "SELECTED"; ?>>Decending
</select></td>
<td><input type="submit" value="Go!"></form></td>
</tr></table>

<?php
echo "<p>Sorted by column <b>". $vals[$sortcol] ."</b>. Timestamps displayed are the local time for
the sensor.";
?>

<form method="GET" action="<?php echo $rooturl; ?>/my/current.phtml">


<?php $uri = "obs.php?wfo=$wfo&metar=$metar&sorder=$sorder&sortcol="; ?>
<table style="width: 100%; font-size: 10pt;" cellspacing=0 cellpadding=1 border=1>
<thead>
<tr>
  <th rowspan="2">ADD:</th>
  <th rowspan="2">Station:</th>
  <th rowspan="2"><a href="<?php echo $uri; ?>ts">Ob Time</a></th>
  <th colspan="3">Temps &deg;F</th>
  <th colspan="3">&nbsp;</th>
  <th colspan="3">Wind [knots]</th>
  <th colspan="2">Precip</font></th>
<tr>
  <th>
 <a href="<?php echo $uri; ?>tmpf">Air</a>
 (<a href="<?php echo $uri; ?>max_tmpf">Hi</a> /
 <a href="<?php echo $uri; ?>min_tmpf">Lo</a>)
</th>
  <th><a href="<?php echo $uri; ?>dwpf">Dewp</a></th>
  <th><a href="<?php echo $uri; ?>feel">Feels Like</a></th>
  <th><a href="<?php echo $uri; ?>relh">RH %</a></th>
  <th><a href="<?php echo $uri; ?>alti">Alti</a></th>
  <th><a href="<?php echo $uri; ?>vsby">Vsby</a></th>
  <th><a href="<?php echo $uri; ?>sknt">Speed</a></th>
  <th><a href="<?php echo $uri; ?>drct">Direction</a></th>
  <th><a href="<?php echo $uri; ?>peak">Gust</a>
    @ <a href="<?php echo $uri; ?>peak_ts">Time</a></th>
  <th><a href="<?php echo $uri; ?>phour">Last Hour</a></th>
  <th><a href="<?php echo $uri; ?>pday">Today</a></th>
</tr></thead>
<tbody>  
<?php
function aSortBySecondIndex($multiArray, $secondIndex) {
  global $sorder;
  while (list($firstIndex, $val) = each($multiArray)){
    if ($val == 0) continue;
    $indexMap[$firstIndex] = $multiArray[$firstIndex][$secondIndex];
  }
  if ($sorder == "asc")
        asort($indexMap);
  else
        arsort($indexMap);
        while (list($firstIndex, ) = each($indexMap))
                if (is_numeric($firstIndex))
                        $sortedArray[] = $multiArray[$firstIndex];
                else $sortedArray[$firstIndex] = $multiArray[$firstIndex];
        return $sortedArray;
}

  $mydata = Array();
  while (list($key, $iemob) = each($asos) ){
    $mydata[$key] = $iemob->db;
    $mydata[$key]["sped"] = $mydata[$key]["sknt"] * 1.15078;
    $mydata[$key]["relh"] = relh(f2c($mydata[$key]["tmpf"]), f2c($mydata[$key]["dwpf"]) );
    if ($mydata[$key]["relh"] < 5)
    {
      $mydata[$key]["relh"] = "M";
      $mydata[$key]["dewpf"] = "M";
      if ($sortcol == "feel" || $sortcol == "dwpf" || $sortcol == "relh") {
          $mydata[$key] = 0;
          continue;
      }
    }
    if ($mydata[$key]["tmpf"] < -60)
    {
      $mydata[$key]["tmpf"] = "M";
      if ($sortcol == "tmpf" || $sortcol == "feel" || $sortcol == "dwpf" || $sortcol == "relh") {
          $mydata[$key] = 0;
          continue;
      }
    }
    if ($mydata[$key]["alti"] < -60)
    {
      $mydata[$key]["alti"] = "M";
      if ($sortcol == "alti") {
          $mydata[$key] = 0;
          continue;
      }
    }
    if ($mydata[$key]["vsby"] < 0)
    {
      $mydata[$key]["vsby"] = "M";
      if ($sortcol == "vsby") {
          $mydata[$key] = 0;
          continue;
      }
    }


    $mydata[$key]["feel"] = feels_like($mydata[$key]["tmpf"],  $mydata[$key]["relh"], $mydata[$key]["sped"]);

    if ($mydata[$key]["max_gust"] > $mydata[$key]["max_sknt"]){
      $mydata[$key]["peak"] = $mydata[$key]["max_gust"];
      $mydata[$key]["peak_ts"] = strtotime(substr( $mydata[$key]["lmax_gust_ts"],0,16) );
    } else {
      $mydata[$key]["peak"] = $mydata[$key]["max_sknt"];
      $mydata[$key]["peak_ts"] = 0;
      if ($mydata[$key]["max_sknt_ts"] > 0)
      {
        $mydata[$key]["peak_ts"] = strtotime(substr( $mydata[$key]["lmax_sknt_ts"],0,16) );
      }
    }

  }

  $finalA = Array();
  $finalA = aSortBySecondIndex($mydata, $sortcol);
  $now = time();
  $i = 0;
  while (list ($key, $val) = each ($finalA))  {
    $i++;

    $parts = $finalA[$key];

    echo "<tr";
    if ($i % 2 == 0)  echo " bgcolor='#eeeeee'";  
    echo "><td><input type=\"checkbox\" name=\"st[]\" value=\"".$key."\"></td>";

    $tdiff = $now - $parts["ts"];
    $moreinfo = sprintf("%s/sites/site.php?station=%s&network=%s", $rooturl, $key, $parts["network"]);
    echo "<td>". $parts["sname"] . " (<a href=\"$moreinfo\">". $key ."</a>,". $parts["network"] .")</td>";
    echo "<td ";
    if ($tdiff > 10000){
      $fmt = "%d %b %I:%M %p";
      echo 'bgcolor="red"';
    } else if ($tdiff > 7200){
      $fmt = "%I:%M %p";
      echo 'bgcolor="orange"';
    } else if ($tdiff > 3600){
      $fmt = "%I:%M %p";
      echo 'bgcolor="green"';
    } else {
      $fmt = "%I:%M %p";
    }

    echo ">". strftime($fmt, $asos[$key]->lts) ."</td>
     <td align='center'>". round($parts["tmpf"],0) ."(<font color=\"#ff0000\">". round($parts["max_tmpf"],0) ."</font>/<font color=\"#0000ff\">". round($parts["min_tmpf"],0) ."</font>)</td>
     <td>". round($parts["dwpf"],0) ."</td>
     <td>". round($parts["feel"],0) ."</td>
	    <td>". $parts["relh"] ."</td>
	    <td>". $parts["alti"] ."</td>
	    <td>". $parts["vsby"] ."</td>
             <td>". round($parts["sknt"],0) ;
            if (strlen($parts["gust"] != 0)){
              echo "G". round($parts["gust"],0);
            } echo "</td>";
            echo "<td>". $parts["drct"] ."</td>
	    <td>". round($parts["peak"],0) ." @ ". strftime("%I:%M %p", $parts["peak_ts"]) ."</td>
            <td>". $parts["phour"] ."</td>
            <td>". $parts["pday"] ."</td>
	    </tr>\n";
         if ($metar == "yes") {
            echo "<tr";
            if ($i % 2 == 0)  echo " bgcolor='#eeeeee'";
            echo ">";
            echo "<td colspan=14 align=\"CENTER\">
             <font color=\"brown\">". $parts["raw"] ."</font></td>
             </tr>\n";
         }
   }

?>
</tbody>
</table>

<input type="submit" value="Add to Favorites">
<input type="reset" value="Reset">

</form></div>


<?php include("$rootpath/include/footer.php"); ?>