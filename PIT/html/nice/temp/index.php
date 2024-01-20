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

foreach ($data as $row) {
    // echo $row[1];
    $time = $row[1];
    $batteryTemp = $row[8]; // Change the index according to your CSV structure

    if (!(empty($batteryTemp) == 1)) {
        // Add data points to the array
        $dataPoints[] = array("x" => $time, "y" => floatval($batteryTemp));
        // echo $batteryTemp;
        // echo " ";
    }
}

?>
<!-- time,counter,IMU_Accel_x,IMU_Accel_y,IMU_Accel_z,IMU_Gyro_x,IMU_Gyro_y,IMU_Gyro_z,Battery_1,Battery_2,Brake_Pedal,ca_AmpHrs,ca_Voltage,ca_Current,ca_Speed,ca_Miles,motor_temp,control_info -->
<!DOCTYPE html>
<html lang="en">
<head>
    <script>
        window.onload = function () {
            var chart = new CanvasJS.Chart("chartContainer", {
                animationEnabled: true,
                title: {
                    text: "Battery Temperature Over Time"
                },
                axisY: {
                    title: "Temperature",
                    valueFormatString: "#0.00°",
                },
                axisX: {
                    title: "Time",
                },
                data: [{
                    type: "spline",
                    markerSize: 5,
                    dataPoints: <?php echo json_encode($dataPoints, JSON_NUMERIC_CHECK); ?>
                }]
            });

            chart.render();
        }
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Temp</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <a href="/" class="LINK">Page to Home Page</a>
    <div id="chartContainer" style="height: 370px; width: 100%;"></div>
    <script src="/nice/canvasjs.min.js"></script>

</body>
</html>
