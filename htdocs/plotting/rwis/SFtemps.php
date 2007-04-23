<?php
include("../../../config/settings.inc.php");
include("$rootpath/include/database.inc.php");

/** We need these vars to make this work */
$subc = isset($_GET["subc"]) ? $_GET["subc"] : "";
$dwpf = isset($_GET["dwpf"]) ? $_GET["dwpf"] : "";
$tmpf = isset($_GET["tmpf"]) ? $_GET["tmpf"] : "";
$pcpn = isset($_GET["pcpn"]) ? $_GET["pcpn"] : "";
$s0 = isset($_GET["s0"]) ? $_GET["s0"]: "";
$s1 = isset($_GET["s1"]) ? $_GET["s1"]: "";
$s2 = isset($_GET["s2"]) ? $_GET["s2"]: "";
$s3 = isset($_GET["s3"]) ? $_GET["s3"]: "";
$syear = isset($_GET["syear"]) ? $_GET["syear"] : date("Y");
$smonth = isset($_GET["smonth"]) ? $_GET["smonth"]: date("m");
$sday = isset($_GET["sday"]) ? $_GET["sday"] : date("d");
$days = isset($_GET["days"]) ? $_GET["days"]: 2;
$station = isset($_GET['station']) ? $_GET["station"] : "";
$mode = isset($_GET["mode"]) ? $_GET["mode"]: "rt";

/** Lets assemble a time period if this plot is historical */
if (strlen($days) > 0) {
  $sts = mktime(0,0,0, $smonth, $sday, $syear);
  $dbDateString = "'". strftime('%Y-%m-%d', $sts) ."'";
  $plotTitle = strftime('%a %d %b %Y', $sts) ."\n";
  for ($i=1; $i < intval($days); $i++){
    $tts = $sts + ($i * 86400);
    $dbDateString .= ",'". strftime('%Y-%m-%d', $tts) ."'";
    $plotTitle .= strftime('%a %d %b %Y', $tts) ."\n";
  }
}

$tableName = "rwis_sf";
$dbName = "iowa";
//$station = 'RAME';

//$c1 = iemdb('rwis2');

$val = "> -50";
if (isset($_GET["limit"])) $val = "between 25 and 35";

if ($mode == "rt"){
 $c1 = iemdb('rwis');
 $c0 = iemdb('access');
 $q0 = "SELECT
    valid, gvalid, max(tmpf) as tmpf, max(pday) as pcpn,
    max(dwpf) as dwpf, max(tcs0) as tcs0, max(tcs1) as tcs1,
    max(tcs2) as tcs2, max(tcs3) as tcs3, max(subc) as subc
 FROM
  (SELECT
  to_char(valid, 'mm/dd HH PM') as valid,
  newd || ':' || (case
              when minute > 39 THEN '40'::text
              WHEN minute > 19 THEN '20'::text
              ELSE '00'::text END)::text as gvalid, pday,
  CASE WHEN tmpf ". $val ." THEN tmpf ELSE NULL END as tmpf,
  CASE WHEN dwpf ". $val ." THEN dwpf ELSE NULL END as dwpf,
  CASE WHEN tsf0 ". $val ." THEN tsf0 ELSE NULL END as tcs0,
  CASE WHEN tsf1 ". $val ." THEN tsf1 ELSE NULL END as tcs1,
  CASE WHEN tsf2 ". $val ." THEN tsf2 ELSE NULL END as tcs2,
  CASE WHEN tsf3 ". $val ." THEN tsf3 ELSE NULL END as tcs3,
  CASE WHEN rwis_subf ". $val ." THEN rwis_subf ELSE NULL END as subc
 FROM
   (SELECT
      *,
      to_char(valid, 'YYYY-MM-DD HH24') as newd,
      extract(minute from valid) as minute
    FROM
      current_log
    WHERE
      station = '$station' 
    ORDER by valid ASC) as foo)  as bar
 GROUP by valid, gvalid ORDER by gvalid ASC";
 $minInterval = 20;
} else {
 $c0 = iemdb('rwis');
 $c1 = $c0;
 $tableName = "t". $syear;
 $q0 = "SELECT
    valid, gvalid, max(tmpf) as tmpf, max(pcpn) as pcpn,
    max(dwpf) as dwpf, max(tcs0) as tcs0, max(tcs1) as tcs1,
    max(tcs2) as tcs2, max(tcs3) as tcs3, max(subc) as subc
 FROM
  (SELECT 
  to_char(valid, 'mm/dd HH PM') as valid,
  newd || ':' || (case 
              when minute > 39 THEN '40'::text
              WHEN minute > 19 THEN '20'::text 
              ELSE '00'::text END)::text as gvalid, pcpn,
  CASE WHEN tmpf ". $val ." THEN tmpf ELSE NULL END as tmpf,
  CASE WHEN dwpf ". $val ." THEN dwpf ELSE NULL END as dwpf,
  CASE WHEN tfs0 ". $val ." THEN tfs0 ELSE NULL END as tcs0,
  CASE WHEN tfs1 ". $val ." THEN tfs1 ELSE NULL END as tcs1,
  CASE WHEN tfs2 ". $val ." THEN tfs2 ELSE NULL END as tcs2,
  CASE WHEN tfs3 ". $val ." THEN tfs3 ELSE NULL END as tcs3,
  CASE WHEN subf ". $val ." THEN subf ELSE NULL END as subc
 FROM 
   (SELECT 
      *, 
      to_char(valid, 'YYYY-MM-DD HH24') as newd, 
      extract(minute from valid) as minute 
    FROM 
      $tableName 
    WHERE 
      station = '$station' and 
      date(valid) IN ($dbDateString) 
    ORDER by valid ASC) as foo)  as bar 
 GROUP by valid, gvalid ORDER by gvalid ASC";
 $minInterval = 20;
}

$q1 = "SELECT * from sensors WHERE station = '". $station ."' ";

//echo $q0;
$result = pg_exec($c0, $q0);
$r1 = pg_exec($c1, $q1);

$row = @pg_fetch_array($r1, 0);
$ns0 = $row['sensor0'];
$ns1 = $row['sensor1'];
$ns2 = $row['sensor2'];
$ns3 = $row['sensor3'];

$tcs0 = array();
$tcs1 = array();
$tcs2 = array();
$tcs3 = array();
$pcpn = array();
$Asubc = array();
$Atmpf = array();
$Adwpf = array();
$freezing = array();
$times= array();

$lastp = 0;
for( $i=0; $row = @pg_fetch_array($result,$i); $i++) 
{ 
  $times[] = strtotime( substr($row["gvalid"],0,16) );
  $tcs0[] = $row["tcs0"];
  $tcs1[] = $row["tcs1"];
  $tcs2[] = $row["tcs2"];
  $tcs3[] = $row["tcs3"];
  $Asubc[] = $row["subc"];
  $Atmpf[] = $row["tmpf"];
  $Adwpf[] = $row["dwpf"];
  $p = floatval($row["pcpn"]);
  $newp = 0;
  if ($p > $lastp) { $newp = $p - $lastp; }
  if ($p < $lastp && $p > 0) {$newp = $p; }
  $pcpn[] = $newp;
  $lastp = $p;
  $freezing[] = 32; 
}
pg_close($c0);
//pg_close($c1);


include ("$rootpath/include/jpgraph/jpgraph.php");
include ("$rootpath/include/jpgraph/jpgraph_line.php");
include ("$rootpath/include/jpgraph/jpgraph_bar.php");
include ("$rootpath/include/jpgraph/jpgraph_date.php");

include ("$rootpath/include/all_locs.php");

// Create the graph. These two calls are always required
$graph = new Graph(650,550,"example1");
$graph->SetScale("datlin");
if (isset($_GET["pcpn"])) $graph->SetY2Scale("lin");
if (isset($limit))  $graph->SetScale("datlin", 25, 35);
$graph->img->SetMargin(40,55,105,105);
//$graph->xaxis->SetFont(FS_FONT1,FS_BOLD);
$graph->xaxis->SetLabelAngle(90);

//$graph->title->Set("Recent Meteogram for ". $station);
//$graph->title->SetFont(FF_FONT1,FS_BOLD,16);

$graph->yaxis->SetTitle("Temperature [F]");
if (isset($_GET["pcpn"])) {
 $graph->y2axis->SetTitle("Precipitation [inch]");
 $graph->y2axis->SetTitleMargin(40);
}
$graph->yaxis->title->SetFont(FF_FONT1,FS_BOLD,12);
//$graph->xaxis->SetTitle("Local Valid Time");
$graph->xaxis->SetTitleMargin(60);
$graph->xaxis->title->SetFont(FF_FONT1,FS_BOLD,12);
$graph->xaxis->SetPos("min");

$graph->legend->Pos(0.01, 0.01);
$graph->legend->SetLayout(LEGEND_VERT);

// Create the linear plot
$lineplot=new LinePlot($tcs0, $times);
$lineplot->SetLegend("0: ".$ns0);
$lineplot->SetColor("blue");
$lineplot->SetWeight(3);

// Create the linear plot
$lineplot2=new LinePlot($tcs1, $times);
$lineplot2->SetLegend("1: ".$ns1);
$lineplot2->SetColor("pink");
$lineplot2->SetWeight(3);

// Create the linear plot
$lineplot3=new LinePlot($tcs2, $times);
$lineplot3->SetLegend("2: ".$ns2);
$lineplot3->SetColor("gray");
$lineplot3->SetWeight(3);

// Create the linear plot
$lineplot4=new LinePlot($tcs3, $times);
$lineplot4->SetLegend("3: ".$ns3);
$lineplot4->SetColor("purple");
$lineplot4->SetWeight(3);

// Create the linear plot
$lineplot5=new LinePlot($Asubc, $times);
$lineplot5->SetLegend("Sub Surface");
$lineplot5->SetColor("black");
$lineplot5->SetWeight(3);

// Create the linear plot
$lineplot6=new LinePlot($Atmpf, $times);
$lineplot6->SetLegend("Air Temperature");
$lineplot6->SetColor("red");
$lineplot6->SetWeight(3);

// Create the linear plot
$lineplot7=new LinePlot($Adwpf, $times);
$lineplot7->SetLegend("Dew Point");
$lineplot7->SetColor("green");
$lineplot7->SetWeight(3);

$bp1=new BarPlot($pcpn, $times);
$bp1->SetLegend("Precip");
$bp1->SetFillColor("black");
$bp1->SetAbsWidth(1.0);


// Create the linear plot
$fz=new LinePlot($freezing, $times);
$fz->SetColor("blue");

// Title Box
$tx1 = new Text($cities[$station]['city'] ." \nMeteogram ");
$tx1->Pos(0.01,0.01, 'left', 'top');
$tx1->SetFont(FF_FONT1, FS_BOLD, 16);

$tx2 = new Text("Time series showing temperatures
   from the pavement sensors and 
   the sub-surface sensor ");
$tx2->Pos(0.01,0.11, 'left', 'top');
$tx2->SetFont(FF_FONT1, FS_NORMAL, 10);

include ("$rootpath/include/mlib.php");
/*
include ("$rootpath/include/currentSFOb.php");
$mySOb = currentSFOb($station);
include ("$rootpath/include/currentOb.php");
$myOb = currentOb($station);
*/
$mySOb = Array();


if ($mode == "hist"){
 $ptext = "Historical Plot for dates:\n";
 $tx3 = new Text($ptext . $plotTitle);
} else {
/*
 $tx3 = new Text("Last Ob @ ". strftime("%m/%d %I:%M %p", $mySOb['ts']) ." 
  Sensor 0: ". $mySOb['tmpf0'] ." F 
  Sensor 1: ". $mySOb['tmpf1'] ." F 
  Sensor 2: ". $mySOb['tmpf2'] ." F 
  Sensor 3: ". $mySOb['tmpf3'] ." F 
 Air  Temp: ". $myOb['tmpf'] ." F
 Dew Point: ". $myOb['dwpf'] ." F
 SubS Temp: ". $mySOb['subt'] ." F
");
*/
}
//$tx3->Pos(0.31,0.001, 'left', 'top');
//$tx3->SetFont(FF_FONT1, FS_NORMAL, 8);
//$tx3->SetColor("blue");

$graph->AddText($tx1);
$graph->AddText($tx2);
//$graph->AddText($tx3);

// Add the plot to the graph
$graph->Add($fz);
if (max($tcs0) != "" && isset($_GET["s0"]) )
  $graph->Add($lineplot);
if (max($tcs1) != "" && isset($_GET["s1"]) )
  $graph->Add($lineplot2);
if (max($tcs2) != "" && isset($_GET["s2"]) )
  $graph->Add($lineplot3);
if (max($tcs3) != "" && isset($_GET["s3"]) )
  $graph->Add($lineplot4);
if (max($Asubc) != "" && isset($_GET["subc"]) )
  $graph->Add($lineplot5);
if (max($Atmpf) != "" && isset($_GET["tmpf"]) )
  $graph->Add($lineplot6);
if (max($Adwpf) != "" && isset($_GET["dwpf"]) )
  $graph->Add($lineplot7);

if (max($pcpn) != "" && isset($_GET["pcpn"]) )
  $graph->AddY2($bp1);


// Display the graph
$graph->Stroke();
?>

