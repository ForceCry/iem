<?php 
/*
 * My purpose in life is to produce pics
 */
include("../../config/settings.inc.php");
include("$rootpath/include/database.inc.php");
include("setup.php");

$dir = isset($_GET["dir"]) ? $_GET["dir"]: "";

$filename='/mnt/mesonet/share/pics/'.$station.'/'.$station.'.jpg'; 
$puri='pics/'.$station.'/'.$station.'.jpg';

if ($dir != ""){
 $filename='/mnt/mesonet/share/pics/'.$station.'/'.$station.'_'.$dir.'.jpg';
 $puri='pics/'.$station.'/'.$station.'_'.$dir.'.jpg';
}
if (! file_exists($filename)){
	$puri = sprintf('%s/images/nophoto.png', $rooturl);
}

$THISPAGE = "iem-sites";
$TITLE = "IEM | Site Photos";
include("$rootpath/include/header.php"); 

 $current = "pics"; 
 include("sidebar.php"); 


function printtd($instr,$selected,$station){
  global $network;
  $filename='/mnt/mesonet/share/pics/'.$station.'/'.$station.'_'.$instr.'.jpg';
  if (file_exists($filename)){ 
    if ($instr == $selected)
     {
       echo '<TD align="center" style="background: #ee0;">'.$instr.'</TD>';
       echo "\n";
     }
    else
     {
      echo '<TD align="center"><a href="pics.php?network='.$network.'&station='.$station.'&dir='.$instr.'">'.$instr.'</a></TD>';
      echo "\n";
     }
    }
  else
    {
     echo '<TD align="center">'.$instr.'</TD>';
     echo "\n";
    }
}



?>

<h3>Directional Photos</h3>

<p>This application shows you photos of the observation site if they are
available.  In general, the IEM only has photos for some of the sites in 
Iowa...</p>

<p><a href="pics.php?network=<?php echo $network; ?>&station=<?php echo $station; ?>">Site Photo</a>

<table>
 <tr><?php 
 	printtd("NW",$dir,$station);
 	printtd("N",$dir,$station);
 	printtd("NE",$dir,$station)?></tr>
 <tr><?php 
 	printtd("W",$dir,$station);
 	echo '<TD class="hlink"><IMG class="pics" border="3" SRC="'.$puri.'"  
                    alt="'.$station.' , '.$dir.'" /></td>';
    printtd("E",$dir,$station);?></tr>
  <tr><?php printtd("SW",$dir,$station);
  	printtd("S",$dir,$station);
  	printtd("SE",$dir,$station)?></tr>
</table>
<?php
$filename='/mnt/mesonet/share/pics/'.$station.'/'.$station.'_span.jpg';
$puri='pics/'.$station.'/'.$station.'_span.jpg';
$lfilename='/mnt/mesonet/share/pics/'.$station.'/'.$station.'_pan.jpg';
$pluri='pics/'.$station.'/'.$station.'_pan.jpg';
if (file_exists($filename))
{
  echo "<h3>Panoramic Shot</h3><img src=\"$puri\"><br /><a href=\"$pluri\">Full resolution version</a>";
}
if (file_exists("/mnt/mesonet/share/pics/$station/HEADER.html")){
  echo "<p><strong>". file_get_contents("/mnt/mesonet/share/pics/$station/HEADER.html") ."</strong>";
}

?>
<?php include("$rootpath/include/footer.php"); ?>
