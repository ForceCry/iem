<html>
<head>
<?php
  include("../../config/settings.inc.php");
  $station = isset($_GET['station']) ? $_GET["station"] : 'SKCI4';
  $min = isset($_GET["min"]) ? $_GET["min"] : 1;
  include("$rootpath/include/snet_locs.php");
  include("$rootpath/include/imagemaps.php");
 $secs = intval($min) * 60;
?>
  <title>IEM | KIMT SchoolNet | <?php echo $cities["KIMT"][$station]["short"]; ?></title>
  <meta http-equiv="refresh" content="<?php echo $secs; ?>; URL=kcci_fe.php?min=<?php echo $min; ?>&station=<?php echo $station; ?>">

</head>
<body bgcolor="#96aae7">

<center>
<form method="POST" action="kcci_fe.php" name="st">
<?php
 
  echo "SchoolNet Site: ";
echo "<select  onChange=\"location=this.form.station.options[this.form.station.selectedIndex].value\" name=\"station\">\n";

$Scities = $cities["KIMT"];
while( list($key, $val) = each($Scities) ){
  echo "<option value=\"$rooturl/content/kcci_fe.php?min=".$min."&station=". $key ."\"";
  if ($station == $key){
        echo " SELECTED ";
  }
  echo " >". $val["city"] ."\n";
}

echo "</select>\n";

?>
</form>
<p>
<?php
  echo "<img src=\"kcci.php?station=".$station ."\">\n";
?>

<?php if (! isset($mode) ){ ?>
<br>Refresh Every: 
<form name="refresh" action="kcci_fe.php">
<?php
  $mins = Array(1, 5, 10, 20);
  while (list($key, $val) = each($mins) ){
    echo "<input type=\"radio\" name=\"min\" value=\"". $val ."\" ";
    if ($min == $val){
      echo "CHECKED";
    }
    echo "> ". $val ." min";
  }
?>
<input type="hidden" value="<?php echo $station; ?>" name="station">
<input type="submit" value="Refresh">
</form>
<?php } ?>

</center>

</html>
