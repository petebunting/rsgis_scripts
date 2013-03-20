<?php
    
    /*
     * A page to call the python script 'createCSV.py' to export CSV from database
     * And return CSV file.
     * 
     * Part of GoogleMapsTrainingPointsTool
     * Dan Clewley (clewley@usc.edu)
     * 19/03/2013
     * Copyright 2013 Daniel Clewley.
     */

    
    $command = "python createCSV.py";
    $tempshellfile = tempnam('downloads/', 'run_');
    $tempshell = fopen($tempshellfile, 'w');
    fwrite($tempshell, $command);
    $outfiles = exec('sh '. $tempshellfile);
    $elements = explode(',', $outfiles);
    if(isset($elements[0]) and $elements[0] != '')
    {
            $outfile = $elements[0];
            $outCSVFile= "downloads/" . $outfile;
            // Redirect to file
            header( 'Location: ' . $outCSVFile ) ;
            exit;
    }
    else
    {
            echo "There was a problem exporting the points from the database";
    }
?>
