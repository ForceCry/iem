<?php
$connection = pg_connect("localhost","5432","scan");

$table = "scan2001_hourly";

$queryData = "c1tmp, c2tmp, c3tmp, c4tmp, c5tmp, srha";
$y2label = "Temperature [C]";

if ( strlen($station) == 0){
  $station = "2031";
}

if ( strlen($date) == 0){
	$date = "Yesterday";
}

$query2 = "SELECT ". $queryData .", to_char(valid, 'yymmdd/HH24') as tvalid from ". $table ." WHERE 
	station = '".$station."' and date(valid) >= ('". $date ."'::date - '1 days'::interval)  ORDER by tvalid ASC LIMIT 1200";

$result = pg_exec($connection, $query2);

$ydata1 = array();
$ydata2 = array();
$ydata3 = array();
$ydata4 = array();
$ydata5 = array();
$ydataSR = array();

$xlabel= array();

for( $i=0; $row = @pg_fetch_array($result,$i); $i++) 
{ 
  $ydata1[$i]  = $row["c1tmp"];
  $ydata2[$i]  = $row["c2tmp"];
  $ydata3[$i] = $row["c3tmp"];
  $ydata4[$i] = $row["c4tmp"];
  $ydata5[$i] = $row["c5tmp"];
  $ydataSR[$i] = $row["srha"];
  $xlabel[$i] = $row["tvalid"];
}

pg_close($connection);

include ("../../include/scanLoc.php");
include ("../dev15/jpgraph.php");
include ("../dev15/jpgraph_line.php");

// Create the graph. These two calls are always required
$graph = new Graph(1600,450,"example1");
$graph->SetScale("textlin");
$graph->SetY2Scale("lin", 0, 900);
$graph->img->SetMargin(45,50,55,90);
//$graph->xaxis->SetFont(FONT1,FS_BOLD);
$graph->xaxis->SetTickLabels($xlabel);
$graph->xaxis->SetLabelAngle(90);
$graph->xaxis->SetPos("min");
$graph->title->Set("Solar Rad & Soil Temps for ".$sites[$station]["city"]." SCAN Site");

$graph->y2axis->scale->ticks->Set(100,25);
$graph->y2axis->scale->ticks->SetPrecision(0);

$graph->xaxis->SetTextTickInterval(24);

$graph->title->SetFont(FF_FONT1,FS_BOLD,12);
$graph->y2axis->SetTitle("Solar Radiation [Watts m**-2]");
$graph->yaxis->title->SetFont(FF_FONT1,FS_BOLD,12);
$graph->xaxis->SetTitle("Local Valid Time");
$graph->yaxis->SetTitle( $y2label );
$graph->y2axis->title->SetFont(FF_FONT1,FS_BOLD,12);
$graph->yaxis->SetTitleMargin(35);
$graph->y2axis->SetTitleMargin(35);
$graph->xaxis->SetTitleMargin(55);
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD,12);

//$graph->y2axis->SetColor("blue");
$graph->y2axis->SetColor("red");

// Create the linear plot
$lineplot=new LinePlot($ydataSR);
$lineplot->SetColor("red");
$lineplot->SetLegend("Solar Rad");

// Create the linear plot
$lineplot1=new LinePlot($ydata1);
$lineplot1->SetColor("green");
$lineplot1->SetLegend("2 in");
$lineplot1->SetWeight(2);

// Create the linear plot
$lineplot2=new LinePlot($ydata2);
$lineplot2->SetColor("aquamarine4");
$lineplot2->SetLegend("4 in");
$lineplot2->SetWeight(2);

// Create the linear plot
$lineplot3=new LinePlot($ydata3);
$lineplot3->SetColor("chocolate4");
$lineplot3->SetLegend("8 in");
$lineplot3->SetStyle("dashed");
$lineplot3->SetWeight(2);

// Create the linear plot
$lineplot4=new LinePlot($ydata4);
$lineplot4->SetColor("blue");
$lineplot4->SetLegend("20 in");
$lineplot4->SetWeight(2);

// Create the linear plot
$lineplot5=new LinePlot($ydata5);
$lineplot5->SetColor("black");
$lineplot5->SetLegend("40 in");
$lineplot5->SetStyle("dotted");
$lineplot5->SetWeight(3);

$graph->legend->SetLayout(LEGEND_HOR);
$graph->legend->Pos(0.10, 0.06, "right", "top");


// Add the plot to the graph
$graph->Add($lineplot1);
$graph->Add($lineplot2);
$graph->Add($lineplot3);
$graph->Add($lineplot4);
$graph->Add($lineplot5);
$graph->AddY2($lineplot);

// Display the graph
$graph->Stroke();
