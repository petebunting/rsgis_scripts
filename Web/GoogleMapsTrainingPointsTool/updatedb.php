<?php

    /*
     * A page to update database with class and redirect to the next
     * page.
     * 
     * Part of GoogleMapsTrainingPointsTool
     * Dan Clewley (clewley@usc.edu)
     * 19/03/2013
     * Copyright 2013 Daniel Clewley.
     */

	if(isset($_GET['id']))
	{
        // Conect to database
        $con = mysql_connect('localhost','USERNAME','PASS');;
        if (!$con)
        {
          die('Could not connect: ' . mysql_error());
        }
	
	    mysql_select_db("DATABASE", $con);
	    
	    $sqlQuery = "UPDATE Points SET class = '{$_POST['class']}' WHERE ID = {$_GET['id']}";

        $result = mysql_query($sqlQuery);
        
        // Set up link for next map page
        if(isset($_GET['random']))
        {
            $mappage="map.php?random=yes&previousID={$_GET['id']}";
        }
        else
        {
            $mappage="map.php?previousID={$_GET['id']}";
        }

		echo $mappage;
        
        mysql_close($con);
        
        // Redirect to map for next point
        header( 'Location: ' . $mappage) ;
	}
	
    else
    {
        echo "ERROR: No ID Provided - could not update";
    }

?>
