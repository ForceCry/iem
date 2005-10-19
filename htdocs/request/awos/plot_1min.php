<?php
include("../../../config/settings.inc.php");
include("$rootpath/include/database.inc.php");

$sqlStr = "SELECT station, ";
for ($i=0; $i< $num_vars;$i++){
  $sqlStr .= $vars[$i] ." as var".$i.", ";
}

$sqlStr .= "to_char(valid, 'YYYY-MM-DD HH24:MI') as dvalid from ".$table ;
$sqlStr .= " WHERE valid >= '".$sqlTS1."' and valid <= '".$sqlTS2 ."' ";
$sqlStr .= " and extract(minute from valid)::int % ".$sampleStr[$sample] ." = 0 ";
$sqlStr .= " and station = '". $station ."' ORDER by valid ASC";

echo $sqlStr;

$connection = iemdb("awos");

$query1 = "SET TIME ZONE 'GMT'";

$result = pg_exec($connection, $query1);
$rs =  pg_exec($connection, $sqlStr);

pg_close($connection);

$dataA = Array();
$xlabel = Array();

for ($j=0; $j<$num_vars; $j++){
  $dataA[$j] = Array();
}


for( $i=0; $row = @pg_fetch_array($rs,$i); $i++){
  $xlabel[$i] = substr($row["dvalid"], 5, 14);
  for ($j=0; $j<$num_vars; $j++){
   $dataA[$j][$i] = $row["var".$j];
  }
} // End of for looper
 

// Create the graph. These two calls are always required
$graph = new Graph(600,400,"example3");
$graph->SetScale("textlin");
$graph->img->SetMargin(40,20,50,100);

$graph->xaxis->SetFont(FF_FONT1,FS_BOLD);
$graph->xaxis->SetTickLabels($xlabel);
$graph->xaxis->SetLabelAngle(90);

//$graph->yaxis->scale->ticks->Set(5,1);
//$graph->yaxis->scale->ticks->SetPrecision(0);

$graph->title->Set("Dynamic AWOS Plot for ". $Wcities[$station]["city"]);
$graph->subtitle->Set("Plot valid between: ".$sqlTS1 ." & ". $sqlTS2 );
$graph->title->SetFont(FF_FONT1,FS_BOLD,16);
//$graph->yaxis->SetTitle("");
$graph->yaxis->title->SetFont(FF_FONT1,FS_BOLD,12);
$graph->xaxis->SetTitle("Valid GMT");
$graph->xaxis->SetTitleMargin(70);
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD,12);

$ints = $i % 60 ;
$graph->xaxis->SetTextLabelInterval($ints);
$graph->legend->Pos(0.01, 0.01, "right", "top");
$graph->yscale->SetGrace(10);

$colors = Array("red", "blue", "green");

$lp = Array();

for ($j=0;$j<$num_vars;$j++){
  // Create the linear plot
  $lp[$j]=new LinePlot($dataA[$j]);
  $lp[$j]->SetColor($colors[$j]);
  $lp[$j]->SetLegend($vars[$j]);

  // Add the plot to the graph
  $graph->Add($lp[$j]);
}

// Display the graph
$fp = "/tmp/jpgraph_". $station ."_". time() .".png";
$graph->Stroke("/mesonet/www/html/". $fp);

echo "<p><img src=\"". $fp ."\">\n";

?>
