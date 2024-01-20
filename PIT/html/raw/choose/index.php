<a href="/" class="LINK">Page to Home Page</a><br>

<?php
// Define the directory path
$directory = '/home/pit/2024/';
$answer = 0;
if(isset($_POST['submit']))
{
    $csvFiles = glob($directory . '*.data.csv');
    
    $answer=$_POST['answer'];
    if(!($answer > 0)){
        $answer = 0;
    }
    foreach($csvFiles as $csvFile){
        echo $csvFile, '<br>';
    }
    echo '<br>';

    try {
        echo "Choseing: $answer.data.csv";
        $file = $answer;
        $csvData = file("/home/pit/2024/$file.data.csv");
    } catch (Exception $e) {
        echo 'Error: ' . $e->getMessage();
    }
}
if(!($answer > 0)){
    $answer = 0;
}
try {
    // Parse CSV data
    $data = array_map('str_getcsv', $csvData);

    // Remove header row if it exists
    $header = array_shift($data);

    // Reverse the data array to display new data at the top
    $data = array_reverse($data);

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

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Choose Data</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<br>


<form method="post" action="/raw/choose/">
    <input type="string" name="answer">
    <input type="submit" name="submit" value="Submit">
</form>



<h2>CSV Data</h2>

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
