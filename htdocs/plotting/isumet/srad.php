<?php
include("../../../config/settings.inc.php");

$year = isset($_GET["year"]) ? $_GET["year"] : date("Y");
$month = isset($_GET["month"]) ? $_GET["month"] : date("m");
$day = isset($_GET["day"]) ? $_GET["day"] : date("d");
$station = isset($_REQUEST['station']) ? $_REQUEST['station']: null;

if (strlen($year) == 4 && strlen($month) > 0 && strlen($day) > 0 ){
  $myTime = strtotime($year."-".$month."-".$day);
} else {
  $myTime = strtotime( date("Y-m-d") );
}

$wA = mktime(0,0,0, 8, 4, 2002);
$wLabel = "1min Instantaneous Wind Speed";
if ($wA > $myTime){
 $wLabel = "Instant Wind Speed";
}

$titleDate = strftime("%b %d, %Y", $myTime);

$dirRef = strftime("%Y/%m/%d", $myTime);

$srad = array();
$uvindex = array();
$valid = array();

if ($station == null){
	$fcontents = file("/mesonet/ARCHIVE/data/$dirRef/text/ot/ot0002.dat");
	while (list ($line_num, $line) = each ($fcontents)) {
  		$valid[] = strtotime( substr($line, 0, 26) );
  		$parts = preg_split ("/\s+/", $line);
		$mph[] = intval($parts[8]);
		$drct[] = intval($parts[9]);
		
	} // End of while
} else {
	$fcontents = file("/mesonet/ARCHIVE/data/$dirRef/text/ot/ot0010.dat");
	/*
	 * month, day, year, hour, minute, outside temp, hi outside temp, lo outside
       temp, outside humidity, wind speed, wind direction, wind gust speed, time
 		of gust, pressure, daily_precip, monthly_rain, yearly_rain, inside
 		temp, inside humidity, solar radiation, UV index
	 */
	while (list ($line_num, $line) = each ($fcontents)) {
		$tokens = explode(' ', $line);
		if (sizeof($tokens) != 21){
			continue;
		}
  		$tstring = sprintf("%s %s", $dirRef, $tokens[3]);
  		$valid[] = strtotime($tstring);
  		$srad[] = floatval($tokens[19]);
  		$uvindex[] = floatval($tokens[20]);
 	} // End of while
	
}

include ("$rootpath/include/jpgraph/jpgraph.php");
include ("$rootpath/include/jpgraph/jpgraph_line.php");
include ("$rootpath/include/jpgraph/jpgraph_scatter.php");
include ("$rootpath/include/jpgraph/jpgraph_date.php");

// Create the graph. These two calls are always required
$graph = new Graph(600,300,"example1");
$graph->SetScale("datelin");
$graph->SetY2Scale("lin");
$graph->img->SetMargin(55,40,55,60);

//$graph->yaxis->scale->ticks->SetPrecision(1);
$graph->title->Set("Solar Radiation & UV Index");
$graph->subtitle->Set($titleDate );

$graph->legend->SetLayout(LEGEND_HOR);
$graph->legend->Pos(0.01,0.08);
$graph->xaxis->SetLabelAngle(90);
$graph->yaxis->scale->ticks->Set(90,15);
//$graph->yaxis->scale->ticks->SetPrecision(0);
//$graph->yaxis->scale->ticks->SetPrecision(0);

$graph->yaxis->SetColor("blue");
$graph->y2axis->SetColor("red");

$graph->title->SetFont(FF_FONT1,FS_BOLD,14);

$graph->yaxis->SetTitle("Solar Radiation");
$graph->y2axis->SetTitle("UV Index");

$graph->yaxis->title->SetFont(FF_FONT1,FS_BOLD,12);
$graph->xaxis->SetTitle("Valid Local Time");
$graph->xaxis->SetTitleMargin(30);
$graph->yaxis->SetTitleMargin(30);
//$graph->y2axis->SetTitleMargin(28);
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD,12);
$graph->xaxis->SetPos("min");

// Create the linear plot
$lineplot=new LinePlot($srad, $valid);
$lineplot->SetLegend("Solar Radiation");
$lineplot->SetColor("blue");

$lineplot2=new LinePlot($uvindex, $valid);
$lineplot2->SetLegend("UV Index");
$lineplot2->SetColor("red");


$graph->Add($lineplot);
$graph->AddY2($lineplot2);

$graph->Stroke();
?>