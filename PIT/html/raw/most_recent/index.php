<?php
try {
    // Define the directory path
    $directory = '/home/pit/2024/';

    // why
    // Get a list of CSV files in the directory
    $csvFiles = glob($directory . '*.data.csv');

    // Sort the files by modification time in descending order
    array_multisort(array_map('filemtime', $csvFiles), SORT_DESC, $csvFiles);

    // Select the most recent CSV file
    $latestCsvFile = reset($csvFiles);

    // Open the selected CSV file
    $csvData = file($latestCsvFile);
    // $csvData = file("/home/pit/2024/4.data.csv");

    // Parse CSV data
    $data = array_map('str_getcsv', $csvData);

    // Remove header row if it exists
    $header = array_shift($data);

    // Reverse the data array to display new data at the top
    $data = array_reverse($data);

    // Limit to the most recent 100 entries
    $data = array_slice($data, 0, 150);

    // Get the most up-to-date info for each column that is not blank
    $latestInfo = [];
    foreach ($header as $index => $columnName) {
        $latestInfo[$columnName] = '';
        foreach ($data as $row) {
            if (!empty($row[$index])) {
                $latestInfo[$columnName] = $row[$index];
                break;
            }
        }
    }

} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}

// Auto-refresh the page every 10 seconds
$refreshInterval = 10;
header("refresh:$refreshInterval");

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CSV Data</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>

 <a href="/" class="LINK">Page to Home Page</a>

<h2>Recent Data</h2>

<table border="1">
    <tr>
        <?php foreach ($header as $columnName): ?>
            <th><?= $columnName ?></th>
        <?php endforeach; ?>
    </tr>

    <tr>
        <?php foreach ($latestInfo as $value): ?>
            <td><?= $value ?></td>
        <?php endforeach; ?>
    </tr>

    <?php foreach ($data as $row): ?>
        <tr>
            <?php foreach ($row as $value): ?>
                <td><?= $value ?></td>
            <?php endforeach; ?>
        </tr>
    <?php endforeach; ?>

</table>

</body>
</html>
