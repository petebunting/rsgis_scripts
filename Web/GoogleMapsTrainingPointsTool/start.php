<!--
     Start page to GoogleMapsTrainingPointsTool
     
     Dan Clewley (clewley@usc.edu)
     19/03/2013
     Copyright 2013 Daniel Clewley.
-->

<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <style type="text/css">
            div {text-align:center}
        </style>

       <title>
        Web based training point generation
	    </title>
    </head>
    <body>
        Welcome web based interface for generating training points</br>
        Each point is saved by clicking the <i>Save+Next</i> button, to exit press to save current point and then close the browser window.</br>
        To revisit the previous point click the previous button (not the back button on your browser).</br>
        Points may be classified in sequence or in a random order.</br>     
        To start, click <i>Start</i>.</br></br>
        <form name="dataSelection" action="map.php" method="get">
        Random order for points
        <select name="random">
        <option value="yes" selected=selected >yes</option>
        <option value="no">no</option>
         &nbsp;<input type='submit' id='Start' name='Start' onclick='decide()' value='Start'>
         </form>
    </select>

    </body>
</html>

