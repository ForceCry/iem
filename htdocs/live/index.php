<?php
include("../../config/settings.inc.php");
include("$rootpath/include/google_keys.php");
?>
<html>
<head>
<link rel="stylesheet" type="text/css" href="http://extjs.cachefly.net/ext-3.1.1/resources/css/ext-all.css"/>
<script type="text/javascript" src="http://extjs.cachefly.net/ext-3.1.1/adapter/ext/ext-base.js"></script>
<script type="text/javascript" src="http://extjs.cachefly.net/ext-3.1.1/ext-all.js"></script>
<script src="http://maps.google.com/maps?file=api&amp;v=2.x&amp;key='. $GOOGLEKEYS[$rooturl]["any"] .'" type="text/javascript"></script>
<script src="http://openlayers.org/dev/OpenLayers.js"></script>
<script type="text/javascript" src="GeoExt.js"></script>
<script type="text/javascript" src="static.js?v=2"></script>
<title>IEM Live</title>
</head>
<body>
<div id="themap"></div>
</body>
</html>