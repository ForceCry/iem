<?php 
include("../../config/settings.inc.php");
$TITLE = "IEM | ISU Soil Moisture Plots";
$THISPAGE="networks-agclimate";
include("$rootpath/include/header.php"); 
include("$rootpath/include/forms.php"); 
include("$rootpath/include/imagemaps.php"); 

$now = time();
$d2 = time() - 3 * 86400;
$station = isset($_GET["station"]) ? $_GET["station"] : "CAMI4";
$year1 = isset($_REQUEST['year1']) ? intval($_REQUEST['year1']): date("Y", $d2);
$month1 = isset($_REQUEST['month1']) ? intval($_REQUEST['month1']): date("m", $d2);
$day1 = isset($_REQUEST['day1']) ? intval($_REQUEST['day1']): date("d", $d2);
$hour1 = isset($_REQUEST['hour1']) ? intval($_REQUEST['hour1']): 0;
$year2 = isset($_REQUEST['year2']) ? intval($_REQUEST['year2']): date("Y", $now);
$month2 = isset($_REQUEST['month2']) ? intval($_REQUEST['month2']): date("m", $now);
$day2 = isset($_REQUEST['day2']) ? intval($_REQUEST['day2']): date("d", $now);
$hour2 = isset($_REQUEST['hour2']) ? intval($_REQUEST['hour2']): date("H", $now);

?>

Back to <a href="/agclimate/">ISU Ag Climate</a> Homepage.<p>

<h3>Soil Moisture and Precipitation Timeseries</h3>

<p>This application plots a timeseries of soil moisture and precipitation from
a ISU Soil Moisture station of your choice.  Please select a start and end time
and click the 'Make Plot' button below.

<form name="selector" method="GET" name='getter'>

<table>
<thead><tr><th>Station</th><td></td><th>Year</th><th>Month</th><th>Day</th><th>Hour</th></tr></thead>

<tbody>
<tr><th rowspan='2'><?php echo networkSelect("ISUSM", $station); ?></th>
<td>Start Time</td>
	<td><?php echo yearSelect2(2012, $year1, "year1"); ?></td>
	<td><?php echo monthSelect($month1, "month1"); ?></td>
	<td><?php echo daySelect2($day1, "day1"); ?></td>
	<td><?php echo hourSelect($hour1, "hour1"); ?></td></tr>
<tr>
<td>End Time</td>
	<td><?php echo yearSelect2(2012, $year2, "year2"); ?></td>
	<td><?php echo monthSelect($month2, "month2"); ?></td>
	<td><?php echo daySelect2($day2, "day2"); ?></td>
	<td><?php echo hourSelect($hour2, "hour2"); ?></td></tr>

</tbody>
</table>

<input type="submit" value="Make Plot">
</form>


<p><img src="<?php echo sprintf("smts.py?station=%s&year1=%s&year2=%s&month1=%s&month2=%s&day1=%s&day2=%s&hour1=%s&hour2=%s", 
		$station, $year1, $year2, $month1, $month2, $day1, $day2, 
		$hour1, $hour2); ?>">

<p><strong>Plot Description:</strong>

<?php include("$rootpath/include/footer.php"); ?>
