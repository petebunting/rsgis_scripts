<!DOCTYPE html>
<!--
     Main map page to GoogleMapsTrainingPointsTool
     
     Requires:
     - OpenLayers (http://www.openlayers.org/)
        If OpenLayers is not in the same directory in the 
        folder OpenLayers, need to change some paths
     - MySQL database containing sample points, these can
        be loaded with loadpoints_gensql.sql
     
     The example here uses Forest / NonForest classes.
     These should be changed as required.
     
     Dan Clewley (clewley@usc.edu)
     19/03/2013
     Copyright 2013 Daniel Clewley.
-->
<?php

    // Conect to database
    $con = mysql_connect('localhost','USERNAME','PASS');
	if (!$con)
	{
	  die('Could not connect: ' . mysql_error());
	}
	
	mysql_select_db("DATABASE", $con);
	
	if(isset($_GET['id']))
	{
	    $sqlQuery = "SELECT * FROM `Points` WHERE ID = {$_GET['id']} LIMIT 1;";
    
        $result = mysql_query($sqlQuery);
        $row = mysql_fetch_row($result);
        
        $pointID = $row[0];
        $pointLat = $row[1];
        $pointLon = $row[2];
        $class = $row[3];
        
        if(isset($_GET['previousID']))
        {
            if(isset($_GET['random']))
            {
                $prevPage="map.php?random=yes&id={$previousID}";
                $nextPage="updatedb.php?id={$pointID}&random=yes";
            }
            else
            {
                $prevPage="map.php?id={$_GET['previousID']}";
                $nextPage="updatedb.php?id={$pointID}";
            }
        }
        else
		{
			$prevPage="start.php";
			$nextPage="updatedb.php?id={$pointID}";
		}
	}
	
    // Get point location from database
    else if(isset($_GET['random']) && $_GET['random'] == 'yes')
    {
        $sqlQuery = "SELECT * FROM `Points` WHERE class = '' ORDER BY RAND() LIMIT 1;";
    
        $result = mysql_query($sqlQuery);
        $row = mysql_fetch_row($result);
        
        $pointID = $row[0];
        $pointLat = $row[1];
        $pointLon = $row[2];

        // Set previous page
        if(isset($_GET['previousID']))
        {
            $prevPage="map.php?random=yes&id={$_GET['previousID']}";
        }
        else{$prevPage="start.php?random=yes";}
        $nextPage="updatedb.php?random=yes&id={$pointID}";
    
    } 
    else if(isset($_GET['previousID']))
    {
        $sqlQuery = "SELECT * FROM `Points` WHERE class = '' AND ID > {$_GET['previousID']} ORDER BY ID ASC LIMIT 1;";
    
        $result = mysql_query($sqlQuery);
        $row = mysql_fetch_row($result);
        
        $pointID = $row[0];
        $pointLat = $row[1];
        $pointLon = $row[2];
        
        // Set previous page
        $prevPage="map.php?id={$_GET['previousID']}";
        $nextPage="updatedb.php?id={$pointID}";
    }
    else
    {
        $sqlQuery = "SELECT * FROM `Points` WHERE class = '' ORDER BY ID ASC LIMIT 1;";
    
        $result = mysql_query($sqlQuery);
        $row = mysql_fetch_row($result);
        
        $pointID = $row[0];
        $pointLat = $row[1];
        $pointLon = $row[2];
        
        // Set previous page
        $prevPage="start.php";
        $nextPage="updatedb.php?id={$pointID}";
    }
    
    mysql_close($con)

?>


<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <title>
            <?php echo "Training - Point {$pointID}"; ?>
        </title>



		<style type="text/css">
			#map {
			width: 100%;
			height: 500px;
			border: 1px solid gray;
			}
			 div {
			 text-align:center;
			 text-size:20;
			 }
		</style>


        <link rel="stylesheet" href="./OpenLayers/theme/default/style.css" type="text/css">
        <link rel="stylesheet" href="./OpenLayers/theme/default/google.css" type="text/css">
        <link rel="stylesheet" href="./OpenLayers/examples/style.css" type="text/css">
         <script src="http://maps.google.com/maps/api/js?v=3&amp;sensor=false"></script>
        <script src="./OpenLayers/lib/OpenLayers.js"></script>
        <script type="text/javascript">
var map;

function init() {
    <?php
        // Point location - transform to map coordinate system
        echo "var pointLocation = new OpenLayers.LonLat({$pointLon},{$pointLat}).transform('EPSG:4326','EPSG:3857');";
    ?>
    // Set up map
    map = new OpenLayers.Map('map', {
        allOverlays: true,
        zoom: 17
        });
    map.addControl(new OpenLayers.Control.LayerSwitcher());
    
    var gsat = new OpenLayers.Layer.Google(
    "Google Satellite",
    {type: google.maps.MapTypeId.SATELLITE, numZoomLevels: 22}
    );
    var gphy = new OpenLayers.Layer.Google(
    "Google Physical",
    {type: google.maps.MapTypeId.TERRAIN, visibility: false}
    );
    var gmap = new OpenLayers.Layer.Google(
    "Google Streets", // the default
    {numZoomLevels: 20, visibility: false}
    );
    var ghyb = new OpenLayers.Layer.Google(
    "Google Hybrid",
    {type: google.maps.MapTypeId.HYBRID, numZoomLevels: 22, visibility: false}
    );
    
    map.addLayers([gsat, gphy, gmap, ghyb]);
        
    var markers = new OpenLayers.Layer.Markers( "Markers" );
    
    var size = new OpenLayers.Size(20,20);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var icon = new OpenLayers.Icon('./OpenLayers/img/marker.png',size,offset);
    markers.addMarker(new OpenLayers.Marker(pointLocation,icon));

    map.addLayer(markers);
    map.setCenter(pointLocation);
    
}
    

        </script>
    </head>
    <body onload="init()">
        <div id="map" class="smallmap"></div>
		<div>        
        <?php
        
            // Buttons to classify
            echo '<form name="getdata" action="' . $nextPage . '" method="post">';
            echo '<INPUT TYPE="BUTTON" VALUE="Previous" ONCLICK="window.location.href=\''.$prevPage.'\'">';
            if(isset($class))
            {
                // If already classified - set checked to previous class
                if($class == 'NonForest')
                {
                    echo '<input type="radio" name="class" value="NonForest" checked>Non-Forest &nbsp;';
                    echo '<input type="radio" name="class" value="Forest">Forest &nbsp;';
                    echo '<input type="radio" name="class" value="">Skip &nbsp;';
                }
                else if($class == 'Forest')
                {
                    echo '<input type="radio" name="class" value="NonForest">Non-Forest&nbsp;';
                    echo '<input type="radio" name="class" value="Forest" checked>Forest&nbsp;';
                    echo '<input type="radio" name="class" value="">Skip &nbsp;';
                }
     	       else
        	    {
            	    echo '<input type="radio" name="class" value="NonForest">Non-Forest &nbsp;';
                	echo '<input type="radio" name="class" value="Forest">Forest &nbsp;';
                	echo '<input type="radio" name="class" value="" checked>Skip &nbsp;';
            	}

       		}
            else
            {
                echo '<input type="radio" name="class" value="NonForest">Non-Forest &nbsp;';
                echo '<input type="radio" name="class" value="Forest">Forest &nbsp;';
                echo '<input type="radio" name="class" value="" checked>Skip &nbsp;';
            }

            echo "<input type='submit' id='Next' name='SaveNext' onclick='decide()' value='Save + Next'>";
            echo "</form>";
        
        ?>
       </div> 
        
    </body>
</html>
