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

// echo ($data[count($data)-1][8]);

for ($x = 50; $x >= 0; $x--) {

    $time = $data[count($data)-1-$x][1];

    $batteryTemp = $data[count($data)-1-$x][17];

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
    <script src="/nice/canvasjs.min.js"></script>
    <script src="/nice/jquery-3.6.4.min.js"></script>
    <script>
        window.onload = function () {
            var dps = []; //<?php echo json_encode($dataPoints, JSON_NUMERIC_CHECK); ?>;
            var chart = new CanvasJS.Chart("chartContainer", {
                title :{
                    text: "Throttle 0v-5v"
                },
                axisY: {
                    title: "Throttle",
                    valueFormatString: "#0.00v",
                },
                axisX: {
                    title: "Time",
                },
                data: [{
                    type: "spline",
                    dataPoints: dps
                }]
            });

            var updateInterval = 350;
            var dataLength = 50; // number of dataPoints visible at any point
            var xVal = 0;
            var yVal = 100; 
            var data = [];
            
            async function updateChart(count) {

                count = count || 1;
                
                // Use AJAX to fetch new data from the server
                var newData = await $.get("fetch_data.php");

                data = JSON.parse(newData);

                console.log(data);

                for (var j = 0; j < count; j++) {
                    yVal = data[j]["y"];
                    xVal = data[j]["x"];
                    dps.push({
                        x: xVal,
                        y: yVal
                    });
                }
            
                if (dps.length > dataLength) {
                    dps.shift();
                }

                // console.log(dps);
                
                // Render the updated chart
                chart.render();
            };
            
            // updateChart(dataLength);
            setInterval(function(){updateChart()}, updateInterval);
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
</body>
</html>
