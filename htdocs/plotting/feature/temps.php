<?php
include("../../../config/settings.inc.php");
include("$rootpath/include/database.inc.php");
include("$rootpath/include/mlib.php");


$times = Array();
$tmpf = Array();
$sknt = Array();
$vsby = Array();

$dbconn = iemdb('access');
$sql = "SELECT extract(EPOCH from valid) as epoch, tmpf, dwpf, sknt, vsby
  from current_log WHERE station = 'SDA' and valid > '2009-02-09' and dwpf > -99 ORDER by valid ASC";
$rs = pg_query($dbconn, $sql);

for ($i=0;  $row=@pg_fetch_array($rs,$i); $i++)
{
  $times[] = $row["epoch"];
  $tmpf[] = $row["tmpf"];
  $sknt[] = $row["sknt"] * 1.15;
  $vsby[] = $row["vsby"];
}

include ("$rootpath/include/jpgraph/jpgraph.php");
include ("$rootpath/include/jpgraph/jpgraph_line.php");
include ("$rootpath/include/jpgraph/jpgraph_date.php");


// Create the graph. These two calls are always required
$graph = new Graph(320,300,"example1");
$graph->SetScale("datlin");
$graph->SetY2Scale("lin");
$graph->img->SetMargin(40,40,50,85);

$graph->xaxis->SetLabelAngle(90);
$graph->xaxis->SetLabelFormatString("Md h A", true);
//$graph->xaxis->scale->SetDateFormat("M d h A");
$graph->xaxis->SetPos("min");

$graph->y2axis->SetTitleMargin(20);
$graph->y2axis->SetColor("blue");
$graph->y2axis->title->SetColor("blue");
$graph->xaxis->SetTitleMargin(70);

$graph->yaxis->title->SetFont(FF_FONT2,FS_BOLD,16);
$graph->y2axis->title->SetFont(FF_FONT2,FS_BOLD,16);
$graph->xaxis->title->SetFont(FF_FONT2,FS_BOLD,16);
//$graph->xaxis->SetTitle("Valid Local Time");
$graph->yaxis->SetTitle("Temp [F] or Wind [MPH]");
$graph->y2axis->SetTitle("Visibility [mile]");
//$graph->tabtitle->Set('Recent Comparison');
$graph->title->Set('Spencer [KSPW] Time Series');

  $graph->tabtitle->SetFont(FF_FONT1,FS_BOLD,16);
  $graph->SetColor('wheat');

  $graph->legend->SetLayout(LEGEND_HOR);
  $graph->legend->SetPos(0.01,0.07, 'right', 'top');
//  $graph->legend->SetLineSpacing(3);

  $graph->ygrid->SetFill(true,'#EFEFEF@0.5','#BBCCEE@0.5');
  $graph->ygrid->Show();
  $graph->xgrid->Show();


// Create the linear plot
$lineplot=new LinePlot($vsby, $times);
$lineplot->SetLegend("Visibility");
$lineplot->SetColor("blue");
$graph->AddY2($lineplot);

// Create the linear plot
$lineplot2=new LinePlot($tmpf,$times);
$lineplot2->SetLegend("Air Temp");
$lineplot2->SetColor("red");
$graph->Add($lineplot2);

$lineplot3=new LinePlot($sknt,$times);
$lineplot3->SetLegend("Wind Speed");
$lineplot3->SetColor("black");
$graph->Add($lineplot3);

// Add the plot to the graph

// Display the graph
$graph->Stroke();
?>
