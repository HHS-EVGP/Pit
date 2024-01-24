<?php
$directory = '/home/pit/2024/';
// Get a list of CSV files in the directory
$csvFiles = glob($directory . '*.data.csv');
// Sort the files by modification time in descending order
array_multisort(array_map('filemtime', $csvFiles), SORT_DESC, $csvFiles);
// Select the most recent CSV file
$latestCsvFile = reset($csvFiles);

$data = array_map('str_getcsv', file($latestCsvFile));
$dataPoints = array();

// Your existing code to extract data points from $data
for ($x = 0; $x >= 0; $x--) {

    $time = $data[count($data)-1-$x][1];

    $batteryTemp = $data[count($data)-1-$x][17];

    if (!(empty($batteryTemp) == 1)) {
        // Add data points to the array
        $dataPoints[] = array("x" => $time, "y" => floatval($batteryTemp));
        // echo $batteryTemp;
        // echo " ";
    }
}

// Return the data as JSON
echo json_encode($dataPoints, JSON_NUMERIC_CHECK);
?>
