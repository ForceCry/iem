<?php $TITLE = "IEM | COOP Extremes Plots";
include("/mesonet/php/include/header.php"); ?>

<div class="text">
<B>Navigation:</B>
<a href="http://mesonet.agron.iastate.edu/">IEM</a> &nbsp;>&nbsp;
<a href="/climate/">Climatology</a> &nbsp;>&nbsp;
<B>COOP Daily Extremes</B>

<BR>
<p>Using the NWS COOP dataset, the IEM has calculated daily
temperature extremes.  You can create a annual plot of this dataset for a
station of your choice.</p> 

<?php include("../../include/COOPstations.php"); ?>

<form method="GET" action="extremes_fe.php">

<table>
<tr>
  <th class="subtitle">Station</th>
  <th class="subtitle">Variable</th>
  <td></td>
</tr>

<tr>
<td>
<SELECT name="station">
<?php
	for(reset($cities); $key = key($cities); next($cities))
	{
		print("<option value=\"" . $cities[$key]["id"] ."\"");
                if ($cities[$key]["id"] == $station) print(" SELECTED ");

		print(">" . $cities[$key]["city"] . "\n");
	}
?>
</SELECT>
</td>
<td>
<SELECT name="var">
  <option value="high" <?php if ($var == "high") echo " SELECTED "; ?>>High Temp
  <option value="low" <?php if ($var == "low") echo " SELECTED "; ?>>Low Temp
</SELECT>
</td>
<td>
<input type="SUBMIT" value="Make Plot">

</form>
</td>

</tr></table>

<?php

  if (strlen($station) > 0 ){
    echo "<img src=\"extremes.php?var=". $var ."&station=". $station ."\">\n";
  }
?></div>

<?php include("/mesonet/php/include/footer.php"); ?>
